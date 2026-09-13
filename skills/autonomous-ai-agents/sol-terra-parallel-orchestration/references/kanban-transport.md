# Kanban transport contract

Kanban is an optional durable execution transport inside the **Parallel** topology. It is independent of the project consultation tier and the Assured overlay. It does not create a third topology or turn a worker self-report into project acceptance proof. For a Kanban-native project/integration orchestration, its graph is the lifecycle authority; the detailed plan file is attached trace/evidence, not a second status ledger.

Use this transport when a logical task benefits from restart survival, a named profile with persistent memory, human comment/block/unblock interaction, repeated implementation/review runs, scheduled or long-lived work, or a durable audit trail. Use `delegate_task` for bounded same-session RPC work whose result must return directly to the current controller context.

## 1. Universal transport boundary

- Direct is controller-owned and creates no Kanban execution cards.
- A Parallel plan may use `delegate_task`, Kanban, or both for different logical tasks.
- One logical task attempt has exactly one active transport owner.
- For a Kanban-native project/integration orchestration, the board graph (cards, links, runs, events, comments, and attachments) is the durable lifecycle authority. The trace artifact records readback snapshots and detailed evidence only.
- Card `done` or `review` makes a handoff available for controller verification; only an explicit final-synthesis card may accept project completion.
- Kanban review, committee advice, worker self-report, goal-mode judgment, or board consensus never replaces deterministic checks, Sol verification, external-effect readback, or required Codex/Claude consultation coverage.
- Only Sol creates plan-owned cards and dependencies. Plan workers may not create child cards, invoke auto-decompose/swarm for their own scope, or broaden the task graph.
- Card/archive/delete operations never erase the plan's task, attempt, evidence, or consultation history.

## 2. Capability and ownership preflight

Before selecting Kanban for any task, record and verify:

| Capability | Required proof | Failure action |
|---|---|---|
| Orchestrator board tools | Active Sol profile exposes `kanban_list`, `kanban_create`, and required orchestration tools through the supported tool schema | Use `delegate_task` when safe or mark Kanban `BLOCKED` |
| Board | Exact board slug exists and resolves to the expected project DB/workspace root | Create an explicitly authorized named board or block; never guess |
| Dispatcher | Gateway is running, `kanban.dispatch_in_gateway` is enabled, and the gateway-embedded singleton dispatcher/claim path is verified | Keep cards non-executable or block; never start a competing standalone daemon |
| Profile | Assignee is an exact current profile name from the live profile catalog | Block; never invent or autocorrect a profile |
| Worker route | Record actual profile model/provider/reasoning/toolsets and any explicit per-task overrides | Remove unsupported override or block; never silently change global profile config |
| Skills | Every pinned task skill is installed and enabled for the assignee | Correct before creation or block |
| Workspace | Kind, absolute path/project, ownership, persistence, and cleanup are explicit | Choose a safe workspace or block |
| Dependencies | Every parent card ID is recorded and every parent plan task exists | Create parents first; do not create the child ready and link later |
| Notifications | Subscription/receipt behavior is known when user wakeup is required | Record no-notification fallback; notification failure does not equal task failure |
| Board guard | Current process is not one of the delegated child contexts prohibited from mutating Kanban | Return to the top-level Sol session; never bypass the guard |

Configuration, process, or schema readback is evidence only for the active installation. Do not claim every Hermes installation exposes a particular board route, dispatcher event, model override, or notification path.

## 3. Board and project isolation

Use a dedicated named board for an unrelated project or repository. The board is the hard queue/workspace/database isolation boundary. A tenant is only a soft namespace within a board and never substitutes for a board when projects should remain segregated.

Record:

```text
board_slug: <validated slug>
board_identity: <database/path or supported board readback>
tenant: <value or none>
project_id: <board project link or none>
default_workdir: <absolute persistent root or none>
```

Rules:

- Never link tasks across boards.
- Never infer the board from a stale dashboard selection; pass or read back the intended slug.
- A plan-owned card may not be deleted while its attempt is active, under review, needed for rollback, or carrying unintegrated evidence. Archive only after Sol records terminal reconciliation and durable evidence locations.
- If a card is missing, archived, or deleted unexpectedly, freeze dependents and reconcile from root/card identities plus board event/run history. Do not recreate blindly.

## 4. Stable identity and idempotent creation

Every plan-owned Kanban work item uses:

```text
plan_id: <stable plan ID>
plan_task_id: <stable task ID>
work_id: w:<plan-id>:<task-id>
attempt_id: <work-id>@a<N>
transport: kanban
idempotency_key: <plan-id>:<task-id>:<creation-attempt>
board_slug: <board>
card_id: <returned and read-back task ID>
run_id: <native task-run ID when exposed>
assignee: <validated profile>
workspace: <kind + path/project>
```

`work_id` remains stable across retries, reassignment, and transport handoff. `attempt_id` is one fenced worker owner; record every same-card Kanban retry as a new attempt mapped to its native run, even though the card's original creation idempotency key remains unchanged. A replacement card or a move to a new transport has a fresh idempotency key. A material change to objective, scope, acceptance, owner boundary, or side-effect authority creates a new linked `work_id`, not a disguised retry.

Card creation procedure for a non-trivial Kanban project/integration:

1. Create or reuse a controller-owned bootstrap root with deterministic identity and `goal_mode=false` before any execution dispatch; record its returned card ID/key and attach the detailed trace artifact.
2. Validate the entire atomic registry, then create parent cards first and record each returned ID/key in the root comment and trace snapshot.
3. Create a child with all parent IDs in the original create call. Do not create it executable and link dependencies afterward.
4. Pass board, assignee, self-contained acceptance/evidence body, workspace, skills, runtime/retry budget, and idempotency key explicitly.
5. Read back the exact card and verify title/body identity, assignee, parents, board, workspace, status, skills, and idempotency mapping before proceeding.
6. Include a distinct fan-in final-synthesis card; the bootstrap root seals graph creation only and is not project completion.
7. After a partial fan-out failure or controller restart, list/read back existing mappings and create only the missing cards.
8. A conflicting existing card for the same plan identity blocks the lane until Sol reconciles it.

## 5. Card body contract

Every card body is self-contained and contains:

```text
WORK ID / PLAN ID / TASK ID / REVISION / ATTEMPT
w:<plan-id>:<task-id> / <plan> / <task> / <revision> / <work-id>@a<N>

TRANSPORT
Kanban; board <slug>; card <id>; run <id or pending>; assignee <profile>; workspace <kind/path/project>

LIFECYCLE
The card is the Kanban authority. Map card/run events to `planned`, `ready`, `dispatched`, `running`, `handoff_pending`, `verified`, `blocked`, `failed`, `cancel_requested`, `cancelled`, `unknown`, or `superseded`. Card `review`/`done` is only `handoff_pending`; Sol alone records `verified` after independent checks.

OBJECTIVE
<one coherent outcome>

AUTHORITATIVE CONTEXT
<requirements, decisions, exact paths/URLs/handles, current state>

DEPENDENCIES
<plan IDs and parent card IDs with verified handoffs>

OWNERSHIP
May read: <exact resources>
May modify: <exact resources>
Must not modify: <siblings, global config, credentials, unrelated paths>

DELIVERABLE / ACCEPTANCE / VERIFICATION
<artifact or external effect>
- <binary acceptance criteria>
Verification: <exact commands/readbacks>

LIFECYCLE
Call `kanban_show` first. Use heartbeats for long work. Finish with review request, complete, or block through Kanban tools. Do not shell out to board CLI from a worker.

SCOPE FENCE
Do not create plan child cards, auto-decompose, invoke swarm, or broaden scope. Comment discovered work and block when Sol must re-plan.

OUTPUT EVIDENCE
Summary; changed files/resources; tests/queries; artifacts/attachments; decisions; residual risk; cleanup state.
```

Do not include secrets, raw credentials, unrelated private transcripts, or sensitive raw logs in card bodies, comments, metadata, or attachments.

## 6. Workspace contract

### Scratch

Use `scratch` only for isolated disposable work. Required deliverables must be declared through the Kanban artifact/attachment mechanism before completion because undeclared scratch content is deleted. A missing required artifact prevents acceptance.

### Persistent directory

Use `dir:<absolute-path>` only for an explicitly trusted shared persistent directory. Relative paths are invalid. Record which other workers or processes can mutate it; serialize conflicting work.

### Worktree

Coding tasks default to a verified isolated worktree/project workspace when parallel edits are possible. Record base commit, branch/worktree identity, expected files, integration owner, cleanup/retention state, and whether a PR or patch exists. A worktree being preserved is not proof its changes were accepted.

No two active task attempts may mutate the same worktree, branch, generated artifact, external record set, or device. Board separation does not make overlapping filesystem ownership safe.

## 7. Worker and model contract

A Kanban assignee is a verified Hermes profile, not automatically a Terra `delegate_task` child. Record the actual profile model/provider/reasoning/toolsets. Call it a Terra worker only when the active profile route proves that fact.

Per-task model/provider/reasoning or skill overrides are allowed only when:

- the plan explicitly records them;
- the active Kanban schema supports them;
- the target profile/provider/model is valid;
- they do not silently change global profile configuration; and
- the task body and receipt record the effective route.

The worker owns only its card execution. Sol owns decomposition, new cards, transport changes, consultation assignment, integration, and final completion.

goal_mode is off by default. Enable it only for an open-ended card with explicit binary acceptance criteria, bounded turn budget, reachable judge behavior, and a planned sticky-block outcome on exhaustion. Goal-mode judgment is advisory transport control, not Sol verification.

## 8. State mapping

| Kanban state/event | Controller verification phase | Controller obligation |
|---|---|---|
| `triage` | `planned` / blocked-unplanned | Do not allow auto-specification to redefine a plan-owned card; Sol specifies or cancels it |
| `todo` with open parents | dependency-gated `planned` | Verify parent mapping and wait |
| `ready` | `ready` | Verify assignee, dispatcher, workspace, and single-owner fence |
| `running` / claimed | `running` | Record run ID/profile/PID when exposed; maintain ownership fence |
| `review` | `handoff_pending` | Inspect worker handoff; board reviewer is optional transport review only |
| `done` | `handoff_pending` | Independently verify artifact/effects; never auto-accept final synthesis |
| `blocked` / scheduled | `blocked` | Inspect reason/comments; obtain user input, fix capability, or re-plan |
| `request_changes` | `failed` or focused repair-ready | Create/record a focused attempt; preserve reviewer and prior-run evidence |
| `timed_out` / crashed / stale / protocol violation / spawn failed / gave up | `failed` or `unknown` | Inspect runs/events; decide reclaim, reassign, repair, transport handoff, or abort |
| `reclaimed` | `cancelled` after fence/readback | Prove the prior worker is no longer authoritative before successor dispatch |
| archived | terminal evidence retained | Archive only after final-synthesis reconciliation and durable artifact retention |
| deleted/missing | `unknown` / abort candidate | Freeze dependents and reconcile; deletion is never completion |

Board state may move independently because a human or dispatcher can act. Sol must read back the card before every promotion, handoff, acceptance, archive, or transport change.

## 9. Retry, reassignment, and handoff fencing

Before any successor attempt:

1. Inspect card state, comments, events, and complete run history.
2. Determine whether the prior worker still has a live claim/process or may have produced external effects.
3. Reclaim/cancel/terminate through the supported operator path and verify the prior owner is no longer authoritative.
4. Read back all potentially mutated resources and preserve partial artifacts/evidence.
5. Increment the plan attempt and assign a new transport identity/idempotency key when creating a replacement card or moving transports.
6. Revalidate dependencies, scope, Assured state, consultation fingerprint eligibility, workspace ownership, and cleanup.
7. Record why work is reassigned, reclaimed, retried, or handed to another transport.

Reassignment on the same card creates a new run but does not erase earlier runs. If the logical scope or acceptance contract changes, create a new plan attempt/card rather than rewriting history. Never dispatch `delegate_task` as a backup while a Kanban worker may still be active.

## 10. Review and consultation separation

Kanban `review`, `kanban_request_review`, a reviewer profile, or `kanban_request_changes` is an implementation-quality workflow. It may support Sol's spec/quality verification but never satisfies the project-level external CLI gate.

Required Codex/Claude consultation tasks remain governed by `consultation-coverage.md`: deterministic checks first, exact candidate fingerprint, read-only bounded calls, independent Sol disposition, and tier-specific fallback/waiver rules. A Kanban profile named `codexc` or `claude` is not proof that the external CLI ran.

## 11. Assured Kanban controls

When Assured applies, add:

- immutable plan/card/workspace/candidate identities;
- board and event/run-history retention until final completion/rollback;
- exact external pre-state and post-state readbacks;
- cancellation/reclaim proof before retry or transport handoff;
- card/attachment/worktree cleanup and archive obligations;
- required CLI fingerprints tied to the accepted artifact;
- explicit user-visible residual risk for missing board evidence, uncertain effects, or waived review; and
- no archive/delete until rollback, cleanup, and audit evidence are complete.

Kanban durability is not a backup of external state. Database presence does not prove a worker's filesystem artifact, external mutation, or remote service state.

## 12. Notifications and human input

Notification subscription is optional operational convenience. Record whether task completion/block events can wake the originating session. A missing subscription or delivery failure does not change card acceptance; provide a dashboard/CLI follow-up path without polling from a model turn.

Workers must use durable comments plus `kanban_block` for human decisions rather than `clarify`. Sol reads the full thread after unblock and revalidates scope before resuming.

## 12.5 Durable guidance and immediate change

Kanban comments are a durable handoff surface, not a documented active-turn steering transport. A controller may append a short, scope-preserving comment tagged `durable-guidance` and read it back, but must report its delivery outcome as `not-live` unless a later worker handoff proves it consumed that comment. Do not claim an in-flight worker saw the comment.

If an active worker must change behavior immediately, or if the proposed instruction changes scope, ownership, acceptance, external effects, or authority:

1. append a concise comment stating the reason and requested containment;
2. reclaim or otherwise cancel through the supported Kanban operator path;
3. inspect card state, events, and run history until the prior owner is terminally fenced;
4. read back every resource it may have changed; and
5. record a new `attempt_id` mapped to the successor run for unchanged scope, or create a new linked work item/card with a fresh idempotency key for material scope change.

A reclaim receipt alone does not prove safety or termination. Never call this workflow "live steering".

## 13. Completion and retention

A Kanban task handoff becomes eligible for project synthesis only after Sol:

- reads back the exact card, board, assignee, attempt/run history, parents, workspace, comments, metadata, and declared artifacts;
- verifies the deliverable and every acceptance criterion independently;
- confirms no overlapping or still-running owner exists;
- reads back every material external effect;
- completes required Codex/Claude coverage and matching fingerprints;
- integrates the output with dependent work;
- closes rollback, cleanup, worktree, capability, and archive obligations; and
- records the final-synthesis decision and durable evidence paths on the board.

Archive only after these checks. Do not delete plan-owned cards as routine cleanup; archival preserves the audit trail. If retention policy later removes board events or workspaces, the Sol plan must already contain the required immutable evidence handles.

## Verification checklist

- [ ] Kanban is selected only inside Parallel and the transport decision is recorded independently of tier/Assured.
- [ ] Direct has no Kanban execution card.
- [ ] Each logical attempt has one active transport owner and a stable plan↔card mapping.
- [ ] Board, dispatcher, toolset, profile, route, skills, workspace, and notification capabilities were read back.
- [ ] A dedicated named board is used when project isolation requires it; tenant is not mistaken for hard isolation.
- [ ] Parents were supplied at card creation and every create was reconciled by idempotency key/readback.
- [ ] Auto-decompose, swarm, worker child-card creation, and goal mode are disabled unless explicitly planned and verified.
- [ ] Workspace persistence and scratch artifact retention are explicit.
- [ ] Card body contains scope, dependencies, ownership, acceptance, verification, lifecycle, and no-scope-expansion contracts.
- [ ] Board state is the lifecycle authority; trace snapshots reconcile it without writing a competing status.
- [ ] Retry, reclaim, reassignment, and transport handoff preserve run history and prove the prior owner is fenced.
- [ ] Board review does not replace mandatory external CLI consultation.
- [ ] Assured work retains board/run/artifact identities, rollback, cleanup, fingerprints, and external readbacks.
- [ ] Sol independently verified every accepted card and archived only after terminal reconciliation.
