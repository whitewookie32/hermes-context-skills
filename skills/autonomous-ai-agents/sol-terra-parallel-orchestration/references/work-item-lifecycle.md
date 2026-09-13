# Work Item Identity, Lifecycle, and Steering

Use this reference whenever Parallel work is dispatched through `delegate_task` or Kanban. It provides one portable contract over their different native surfaces; it does not invent a new scheduler, queue, or terminal transport.

## 1. Stable identity

Mint a stable work identity before dispatch:

```text
plan_id: <stable plan/project identifier>
task_id: <stable atomic task identifier>
work_id: w:<plan-id>:<task-id>
attempt_id: <work-id>@a<N>
```

Rules:

- `work_id` names one atomic objective and remains unchanged across retries, reassignment, and transport changes.
- `attempt_id` names one fenced execution owner. Increment `N` for every successor after a prior dispatched or running owner becomes terminal or is proved no longer authoritative.
- A material change to objective, scope, ownership, acceptance, or side-effect authority creates a new `work_id`, linked to the predecessor as a revision or follow-up. Do not disguise scope growth as a retry.
- IDs are opaque, bounded identifiers. They contain no credentials, raw prompts, private paths, user content, or provider session tokens.
- Record the native identity under the attempt: `delegation_id` plus `subagent_id` for `delegate_task`; `board`, `card_id`, and `run_id` for Kanban. Native identity is evidence, not a replacement for `work_id`.

The controller's work record is a reconciliation index. For a Kanban lane, the board remains the lifecycle authority; the controller only maps board events to this portable contract. For a delegated lane, the supported delegation response and completion event are the runtime authority; the trace records controller verification after that event.

## 2. Portable lifecycle

Use these states exactly in plan/task records:

| State | Meaning | Authority to enter |
|---|---|---|
| `planned` | Scoped but not yet dispatchable. | Controller plan |
| `ready` | Dependencies, ownership, and routing gates are verified. | Controller pre-flight |
| `dispatched` | The transport accepted the attempt and native identity was recorded. | Dispatch/card-create receipt |
| `running` | Native runtime reports the exact owner active. | Delegation status or Kanban running/claim readback |
| `handoff_pending` | Worker produced a terminal handoff; controller verification is still required. | Delegation completion or Kanban `review`/`done` readback |
| `verified` | Controller independently verified every acceptance criterion and effect. | Controller evidence only |
| `blocked` | A specific prerequisite, capability, or user decision prevents safe progress. | Native block or controller evidence |
| `failed` | The attempt/runtime/verification failed. | Native failure or controller evidence |
| `cancel_requested` | Cancellation/reclaim was requested, but termination is not yet proved. | Supported control-action receipt |
| `cancelled` | The prior owner is terminally stopped/reclaimed and partial effects are reconciled. | Native terminal event plus readback |
| `unknown` | Process/session loss leaves possible side effects unprovable. Never treat as success. | Runtime crash/restart evidence |
| `superseded` | A terminal earlier attempt was replaced by a separately recorded successor. | Controller reconciliation |

Permitted flow:

```text
planned -> ready -> dispatched -> running -> handoff_pending -> verified
                         |            |             |
                         v            v             v
                    blocked/failed  blocked/failed  blocked/failed
                         |            |
                         v            v
                 cancel_requested -> cancelled

Any dispatched or running attempt may become unknown after a process/session loss.
A successor begins as the same work_id with a new attempt_id only after fencing,
readback, and dependency/ownership revalidation.
```

Do not move a completed state backwards or overwrite a failed handoff. A `blocked -> ready` return is allowed only when no owner was dispatched; otherwise create a successor attempt. `unknown` freezes dependents until the controller reads back every possibly affected resource and either documents a successor or aborts. `verified`, `cancelled`, `failed`, `unknown`, and `superseded` preserve their historical record.

Every transition records:

```text
timestamp | work_id | attempt_id | predecessor -> successor | actor
native transport identity | reason | evidence handle | resource fingerprint or N/A
```

A worker claim, a successful subprocess exit, or a card state alone cannot enter `verified`.

## 3. Dispatch and handoff rules

Before `ready -> dispatched`, record the self-contained brief, immutable or current input identifiers, scope/ownership fence, selected transport, native-id placeholder, acceptance checks, and output contract.

After dispatch, record the returned transport identity immediately. Never start the same attempt in another transport. For a transport handoff or retry:

1. inspect the current native state, logs/events, and run history;
2. prove the prior owner is terminally fenced or classify it `unknown`;
3. read back every resource it could have changed;
4. preserve handoff/artifact evidence without copying raw transcripts or secrets;
5. create the successor `attempt_id`, native identity, and idempotency mapping; and
6. revalidate dependencies, ownership, input freshness, and acceptance before dispatch.

A final worker summary maps to `handoff_pending`, never `verified`. The controller then verifies named artifacts/diffs, exact checks, external readbacks, and required consultation/fingerprint evidence before accepting the attempt.

## 4. Live steering

### `delegate_task`: supported active-turn steering

Use live steering only when `delegate_task(action="list")` identifies the exact active `subagent_id` and reports it accepts steering. Send one bounded, scope-preserving instruction through:

```text
delegate_task(action="steer", subagent_id="<id>", message="<bounded instruction>")
```

Permitted steering clarifies priority, evidence, a constraint already in the brief, or a narrow in-scope approach. It must not add a new deliverable, resource, side effect, approval, provider/tool permission, worker, or external target.

For each request, record a steering entry:

```text
work_id | attempt_id | steer_sequence | redacted intent | target subagent_id |
requested_at | transport response | delivery outcome | controller disposition
```

`queued` means accepted for later delivery, not that the worker saw or followed it. Do not claim success until the completion evidence shows that it landed; a `missed_steer`, `pending_steer`, rejected request, or terminal-race result is not successful steering. Do not poll, inspect private transcripts, or busy-wait for delivery. If it misses, evaluate the original handoff normally and create a successor attempt only when the changed instruction remains necessary.

If the requested change widens scope or must take effect immediately but cannot be delivered, request stop through the supported control action, classify the attempt `cancel_requested`, fence/reconcile it, and re-plan. Steering is never a way to bypass acceptance, ownership, or safety gates.

### Kanban: durable guidance, not live steering

Kanban exposes durable comments, blocks, reclaims, runs, and task state. It does **not** provide an equivalent documented live-turn injection contract. Therefore:

- add a bounded `guidance` comment for a future/restarted worker only when it preserves the current card's scope;
- read back the comment/card, but do not claim an active worker received it;
- use `kanban_block` for an unresolved decision or `kanban_comment` plus `reclaim` when in-flight behavior must change immediately;
- verify reclaim/termination through card state, events, and run history before any successor;
- record the next run as a new attempt. Reuse the existing card only for unchanged scope; create a new card/idempotency key when scope or acceptance changed materially.

Never call durable guidance "steering" in evidence or user-facing status.

## 5. Checkpoints and durable context

A checkpoint contains only what a fresh worker needs to continue safely:

- work and attempt IDs; objective; scope; dependencies; ownership; and acceptance;
- immutable candidate/input fingerprints or concise authoritative references;
- verified decisions, completed checks, artifact paths/handles, and external readbacks;
- native transport identities, transition entries, and a concise failure/block reason;
- unresolved decision plus its owner.

Do not checkpoint raw reasoning, unbounded tool logs, private transcripts, credentials, tokens, `.env` content, or a full parent conversation. A missing native session/thread is a controlled fresh-context restart: rehydrate from the checkpoint, revalidate current resources, and start a new attempt rather than reconstructing hidden context.

## 6. Verification checklist

- [ ] Every active or completed leaf has a stable `work_id` and one current `attempt_id`.
- [ ] Native transport IDs are recorded immediately after dispatch/card creation.
- [ ] No work attempt has two active transport owners.
- [ ] Every lifecycle transition has actor, reason, time, and real evidence.
- [ ] Worker terminal state maps to `handoff_pending`, not `verified`.
- [ ] A successor attempt follows prior-owner fencing and external/resource readback.
- [ ] `delegate_task` steering is exact-child, active-turn, scope-preserving, and delivery-qualified.
- [ ] Kanban comments are labeled durable guidance; immediate changes use block/reclaim and readback.
- [ ] Checkpoints are minimal, attributable, and secret-free.
