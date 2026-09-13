# Parallel mode

Parallel is the execution topology for independent, isolatable, independently verifiable work. The controller decomposes the objective into a dependency DAG, assigns exactly one execution transport to each logical attempt, sends complete leaf briefs, verifies every result, and re-plans after completed work. Parallel is not a safety tier and is not a license to fill capacity; transport, consultation, and Assured controls are selected independently.

Use this reference with `runtime-contract.md` for delegation behavior, `kanban-transport.md` for durable board execution, `consultation-coverage.md` for required external review, and `assured-controls.md` when any assurance trigger is present.

## 1. Eligibility and the break-even invariant

Parallel is eligible only when every proposed leaf satisfies all of these conditions:

1. **Independent outcome:** the leaf has one concrete deliverable that can be accepted without an unfinished sibling.
2. **Explicit inputs:** authoritative inputs and verified prerequisites are named; no parent-only context is required.
3. **Disjoint mutation:** no two active leaves write the same mutable path, record, account, device, branch, process, or environment. Shared read-only inputs must be stable, snapshotted, or explicitly versioned.
4. **Independent verification:** one acceptance check can decide the leaf's result and failure impact without guessing at sibling intent.
5. **Bounded brief:** the leaf can receive a self-contained task card with exact permissions and exclusions.
6. **Useful downstream effect:** completion unlocks a named task, integration check, or decision.

The **break-even invariant** is:

```text
parallel benefit = serial work avoided
                   - coordination overhead
                   - controller verification overhead
                   - expected integration and repair cost

Parallel is admissible only when parallel benefit > 0.
```

Estimate the terms from the actual task cards and dependency structure, using relative work units or explicit evidence rather than fixed duration targets. If the terms cannot be estimated with a defensible basis, choose Direct. If the result is equal to or below zero, keep the work serial. A capacity slot is never a benefit by itself.

The invariant must also hold at the wave level: a ready wave must contain at least two independent leaves whose combined avoided serial work exceeds the cost and risk of dispatching, consolidating, verifying, and repairing that wave. A long indivisible operation remains Direct even if it could technically be wrapped as several commands.

## 2. Plan and decomposition

Before the first dispatch, create or update the active plan with a descriptive revision heading, topology `Parallel`, consultation tier, assurance state, requirement traceability, task registry, DAG, resource ownership, wave schedule, acceptance checks, and completion gate.

Recursively decompose from the objective to the minimum independently verifiable leaves. A leaf is atomic only if it has:

- exactly one concrete outcome and one owner;
- authoritative inputs and a named artifact or observable side effect;
- no hidden prerequisite or unlisted internal deliverable;
- an exact read/write boundary;
- one explicit acceptance decision;
- isolated failure impact; and
- a meaningful reason to be separate under the break-even invariant.

Do not split a transaction, migration, shared lock interval, tightly coupled edit, or state transition merely to make more cards. Conversely, do not leave multiple unrelated deliverables inside one vague card.

### Required task registry fields

Each task receives a stable ID and records:

- parent deliverable and requirement IDs;
- plan revision, attempt number, and repair lineage;
- one-sentence objective and why it matters;
- authoritative inputs and verified dependencies;
- exact deliverable and acceptance criteria;
- `depends_on` and `unlocks` edges;
- owner and allowed tools/resources;
- exact `may_read`, `may_modify`, and `must_not_modify` boundaries;
- risk, failure impact, rollback, and cleanup obligations;
- verification command, query, or evidence source;
- consultation assignment and `Mode: required|optional|prohibited` when applicable;
- selected transport (`delegate_task` or `kanban`), `work_id`, `attempt_id`, and delegation/card/run execution mapping;
- portable lifecycle status: `planned`, `ready`, `dispatched`, `running`, `handoff_pending`, `verified`, `blocked`, `failed`, `cancel_requested`, `cancelled`, `unknown`, or `superseded`; and
- evidence location or handle after verification.

Every requirement maps to one or more leaves, and every leaf maps back to at least one requirement. Missing reverse traceability blocks dispatch.

## 3. Complete leaf briefs

A Terra child has no parent transcript. The controller must send the complete task card in one self-contained brief. Pass exact paths and handles rather than inlining unrelated large files. Do not include secrets or credentials.

Use this structure:

```text
ROLE
You are a Terra leaf worker. The installation owns your model, provider, reasoning, toolset, and concurrency capacity. Execute exactly one atomic assignment. Do not return a plan instead of doing the work. Do not create grandchildren or dispatch children.

WORK ID / PLAN TASK ID / REVISION / ATTEMPT
w:<plan-id>:<task-id> / <stable plan task ID> / <descriptive revision> / <work-id>@a<N>

TRANSPORT IDENTITY AND LIFECYCLE
<delegation ID + subagent ID, or Kanban board/card/run/idempotency/profile/workspace mapping>
Start in `dispatched` and return a handoff only. Controller evidence alone records `verified`. Live `delegate_task` steering is valid only for an active exact child and only when scope-preserving; Kanban comments are durable guidance, not live delivery proof.

OBJECTIVE
<one concrete outcome>

WHY IT MATTERS
<parent requirement and named downstream unlock>

AUTHORITATIVE CONTEXT
<requirements, decisions, exact repo-relative paths, URLs, handles, and current state>

DEPENDENCIES
<verified predecessor IDs and their outputs; state None only when true>

OWNERSHIP BOUNDARY
May read: <exact paths/resources>
May modify: <exact paths/resources>
Must not modify: <sibling-owned, secret, global, or out-of-scope resources>

DELIVERABLE
<exact artifact or observable side effect>

ACCEPTANCE CRITERIA
- <binary criterion>
- <binary criterion>

VERIFICATION
<exact command, query, test, diff, or read-back>

ROLLBACK / CLEANUP
<exact action, owner, or Not applicable with reason>

EXTERNAL AGENT ASSISTANCE
Mode: prohibited | optional | required
Allowed CLIs: Codex | Claude Code | both | none
Purpose: implementation critique | optimization | independent review | adversarial review | not applicable
Permissions: read-only | bounded edits to <exact owned paths>
Budget: <maximum calls and turns>
Required evidence: loaded skill, command class, exit status, concise findings, changed paths

OUTPUT CONTRACT
Return:
1. Work ID / attempt / transport identity
2. Status: PASS, BLOCKED, or FAILED
3. Result
4. Evidence from real execution
5. Exact files/resources changed
6. Steering/guidance disposition, deviations, risks, or newly discovered work
```

The external assistance block does not change the project-level consultation gate. A required project consultation must be a separately assigned atomic task whose brief says `Mode: required` and whose result is independently verified.

## 4. Dependencies and mutable-resource ownership

Build the DAG before dispatch. A task is `ready` only when every predecessor is `verified`, its inputs are stable, and its resource boundary does not conflict with active siblings.

For each resource, record:

| Resource | Type | Owning task/wave | Read policy | Conflict control | Cleanup owner |
|---|---|---|---|---|---|
| `<repo-relative path or external handle>` | file, record, device, process, branch, environment | `<task ID>` | snapshot or read-only | disjoint path, isolated worktree, lock, or serial wave | `<task ID>` |

Rules:

- Two active leaves must never own the same mutable resource.
- A shared generated file is mutable even if each worker writes a different section; isolate generation or serialize it.
- Separate worktrees or environments are valid only when their integration and ownership are recorded.
- A read-only shared source is safe only when its version/fingerprint remains stable for the wave.
- A task that discovers a new mutable resource must stop before mutating it and request a structural revision.
- External effects require the pre-state, authorization, post-state read-back, and rollback/cleanup records required by Assured when triggered.

## 5. Ready queue and batch waves

Recompute the ready queue after planning and after every verified wave. Order ready leaves by critical-path impact, then downstream unlock value, then risk and deterministic task-ID tie-break. Do not reorder to disguise dependencies.

The runtime capacity is the installation-owned value `C` from the active delegation contract. A wave contains at most `C` leaves and never invents work to fill unused slots. If fewer independent leaves are ready, dispatch only those leaves. If more are ready, form deterministic waves and keep later waves blocked until predecessor verification passes.

Before each wave, verify:

- task cards are complete and self-contained;
- all dependencies are `verified`;
- same-wave mutable ownership is disjoint;
- consultation assignments and Assured preconditions are satisfied for the stage;
- the batch is within installed capacity `C`; and
- the break-even invariant remains positive after incorporating current evidence.

Dispatch one `delegate_task(tasks=[...])` batch for the wave, with every item using the leaf role and no per-task model/provider/reasoning override, only after preflight verifies the active public/model-facing batch-completion contract described in `runtime-contract.md`. Record the returned delegation ID, child IDs, and set every attempt to `dispatched`; move an attempt to `running` only when the supported runtime status reports that exact child active. A dispatch response means pending, never success.

Do not poll, sleep, inspect live child transcripts, or busy-wait for completion. Evaluate results only after the exact completion signal defined by the verified public/model-facing contract. Do not start successor waves from private per-child progress; event-driven scheduling remains unsupported unless a public contract explicitly documents it. If the required batch-completion contract is unavailable or cannot be verified, do not claim a completed wave: use Direct if safe or mark Parallel `BLOCKED`.

### Kanban transport projection

For tasks assigned to Kanban, do not place them in the `delegate_task` batch. Before creating cards, pass the capability and ownership preflight in `kanban-transport.md`. Record one mapping row per attempt:

| Plan task | Work ID | Attempt | Transport | Board | Card ID | Native run | Idempotency key | Assignee/profile route | Workspace | Parents | Board state | Portable lifecycle |
|---|---|---:|---|---|---|---|---|---|---|---|---|---|
| `<ID>` | `w:<plan>:<task>` | `<N>` | `kanban` | `<slug>` | `<t_id>` | `<run>` | `<plan>:<task>:<creation-attempt>` | `<profile/model/provider/reasoning>` | `<kind/path/project>` | `<card IDs>` | `<state>` | `<state>` |

Create parents first and include their card IDs in the child's original create request. Persist and read back every returned card before creating dependents. After a partial failure or restart, reconcile by board and idempotency mapping and create only missing cards. Do not use Kanban auto-decompose, swarm, or worker-created follow-up cards to alter the Sol plan.

Kanban state is operational evidence: `running` maps to `running`; `review`/`done` maps to `handoff_pending`; `blocked`, timeout, crash, reclaim, protocol violation, spawn failure, or gave-up events require controller adjudication as `blocked`, `failed`, `cancel_requested`/`cancelled`, or `unknown`. Card completion never moves the plan task to `verified` without independent verification. A transport handoff or reassignment preserves prior runs, increments the logical attempt where scope/owner changes, and proves the prior worker is terminally fenced before a successor starts.

## 6. Controller verification after every wave

The controller independently verifies every returned task. Child summaries are evidence leads, not acceptance proof.

For each leaf:

1. Read the changed paths or query the authoritative resource.
2. Confirm the result matches the exact task card and no sibling/out-of-scope resource changed.
3. Run the named acceptance check and relevant regression or integration checks.
4. Check safety, error, cancellation, zero/one/many, hostile-input, auth, and concurrency cases that the leaf claims to cover.
5. Confirm external effects in the authoritative system and record the post-state.
6. Confirm cleanup, teardown, locks, processes, temporary artifacts, and pending work.
7. Record `PASS`, `BLOCKED`, or `FAILED` with command output, paths, handles, or hashes.

Use two explicit gates where practical:

- **Spec gate:** all acceptance criteria pass with no scope creep.
- **Quality gate:** implementation is safe, maintainable, regression-covered, and integrated with neighboring behavior.

A task moves to `verified` only after both applicable gates pass. A task remains `handoff_pending` or becomes `blocked`/`failed` when evidence is incomplete. Never mark a whole wave complete because most leaves passed.

## 7. Clean updates versus structural revisions

Every completed wave causes a plan update and ready-queue recomputation. Preserve stable IDs and append evidence; never erase failed attempts.

### Incremental clean update

Use an incremental update only when all of the following hold:

- every returned result fits the existing objective and acceptance criteria;
- no requirement, scope, assumption, dependency, ownership boundary, or consultation tier changed;
- no new resource, defect, or risk changes the DAG; and
- the existing verification commands remain sufficient.

Record the genuine completion event, per-task evidence, controller verification, status transitions, cleanup, newly unlocked tasks, and the next ready queue. Do not relabel a failed or out-of-contract result as clean.

### Structural revision

Create a new descriptive plan revision when any of the following occurs:

- a task fails acceptance or returns an out-of-contract artifact;
- a requirement, scope, assumption, or user decision changes;
- new work, a new dependency, a shared mutable resource, or a new risk is discovered;
- ownership must be changed or a wave must be reordered;
- consultation classification or Assured state becomes stricter; or
- a repair needs different inputs, permissions, or verification.

A structural revision must:

1. state the trigger and evidence;
2. preserve the prior task, attempt, event, and verification history;
3. create a new repair ID such as `<task-id>-R1` rather than overwriting the failed attempt;
4. recursively re-check atomicity, requirements, dependencies, ownership, consultation, and assurance;
5. recompute the ready queue and break-even invariant; and
6. pass the plan-completeness gate before dispatching the repair wave.

A revision number is lineage metadata, not a reason to discard earlier evidence. Use a descriptive heading that says what became true or what changed.

## 8. Repair and failure handling

Keep unaffected sibling evidence valid, but block any integration result that depends on a failed leaf. Stop early when repairs are not reducing the defect or when the user must choose between incompatible outcomes.

For a repair:

- identify the exact failed acceptance criterion and root evidence;
- state the changed behavior/files/resources and relevant dependents;
- preserve the original task and artifact fingerprint;
- assign the smallest focused repair leaf with a new revision suffix;
- do not repeat an unrestricted review of unchanged work;
- rerun deterministic checks for the changed candidate;
- reapply consultation and Assured gates when the candidate or risk changed; and
- run controller spec, quality, integration, external-state, and cleanup verification again.

No repair can widen ownership implicitly. If a repair touches a sibling-owned resource, stop and create a structural revision with serialized ownership or an isolated environment. Use the finite plan-owned repair budget, normally three attempts per tactic. Exhaustion or non-decreasing defects stop that tactic and trigger Chairman-owned root-cause reassessment, not an automatic user question. A materially different evidence-backed tactic may receive a new finite budget only within unchanged authorized scope/cost/risk; preserve failed attempts and stop repetitive non-improving loops. Required evidence cannot be waived by re-planning.

If a child reports a tool failure, missing prerequisite, authentication issue, or unsafe condition, preserve the report as evidence. Do not ask it to improvise outside its brief. Reclassify, repair, or escalate with the concrete missing decision.

## Verification checklist

- [ ] Parallel eligibility is proven for every leaf: independent outcome, explicit inputs, disjoint mutation, independent verification, bounded brief, and downstream value.
- [ ] The break-even invariant is positive for the selected wave; unavailable estimates defaulted to Direct.
- [ ] Requirements map forward to leaves and leaves map backward to requirements.
- [ ] Every task card names objective, inputs, dependencies, ownership, deliverable, acceptance, verification, cleanup, and output contract.
- [ ] The DAG is explicit, acyclic, and recomputed after every verified wave.
- [ ] Same-wave mutable-resource ownership is disjoint or isolated; shared reads are stable.
- [ ] Batch size never exceeds installation-owned capacity `C`, and unused capacity was not filled with invented work.
- [ ] Every logical attempt has exactly one active transport; mixed transports are only used by distinct lanes.
- [ ] Delegate transport used one bounded batch with no per-task routing override; dispatch was treated as pending.
- [ ] Kanban transport passed board/profile/dispatcher/workspace preflight and has a stable idempotent plan↔card mapping.
- [ ] Results were evaluated only after the genuine model-facing batch-completion contract.
- [ ] Kanban `review`/`done` mapped only to plan `verify`; card/run history and artifacts were independently checked.
- [ ] Every leaf received independent controller spec and quality verification, including external-state read-back where relevant.
- [ ] Clean updates were used only when scope and structure were unchanged; structural changes created history-preserving revisions.
- [ ] Failed attempts, repairs, cleanup, and escalation decisions remain recorded.
- [ ] Final integration passes with no unexplained `active`, `ready`, `blocked`, or pending external operation.
