# `<Objective>` — Work Item Record

> Use one record per atomic work item. It is a compact controller-owned reconciliation record: Kanban remains authoritative for Kanban lifecycle; Hermes delegation remains authoritative for delegated runtime state. This record does not overwrite either surface.

## 1. Identity

| Field | Value |
|---|---|
| Plan ID | `<stable plan/project ID>` |
| Task ID | `<stable atomic task ID>` |
| Work ID | `w:<plan-id>:<task-id>` |
| Attempt ID | `<work-id>@a<N>` |
| Predecessor / successor | `<attempt ID or N/A>` |
| Revision | `<R<N> / scope milestone>` |
| Transport | `delegate_task \| kanban` |
| Native transport identity | `<delegation ID + subagent ID, or board/card/run>` |
| Controller | `<profile/session>` |
| Worker owner | `<leaf or validated Kanban profile>` |

## 2. Scope and proof contract

**Objective:** `<one observable outcome>`

**Authoritative inputs / freshness:**

- `<path, revision/hash, URL, query, decision, or artifact handle>`

**Dependencies:** `<verified work IDs/attempts, or N/A>`

**Ownership:**

- May read: `<exact resources>`
- May modify: `<exact resources>`
- Must not modify: `<siblings, secrets, global config, external targets, or N/A>`

**Deliverable:** `<artifact or observable effect>`

**Acceptance criteria:**

- [ ] `<binary criterion>`
- [ ] `<binary criterion>`

**Verification:** `<exact command, query, artifact inspection, or external readback>`

**Rollback / cleanup:** `<exact action or N/A>`

## 3. Lifecycle ledger

| Time | From → to | Actor | Native evidence | Reason | Input/output fingerprint |
|---|---|---|---|---|---|
| `<ISO>` | `planned → ready` | `controller` | `<preflight>` | `<why dispatchable>` | `<hash/N/A>` |
| `<ISO>` | `ready → dispatched` | `controller/runtime` | `<dispatch/card receipt>` | `<selected transport>` | `<native ID>` |
| `<ISO>` | `dispatched → running` | `runtime` | `<status/card run>` | `<worker active>` | `<run ID>` |
| `<ISO>` | `running → handoff_pending` | `runtime` | `<completion/review/done>` | `<worker handoff>` | `<artifact>` |
| `<ISO>` | `handoff_pending → verified` | `controller` | `<independent checks/readbacks>` | `<acceptance met>` | `<final hash/N/A>` |

Use only valid states: `planned`, `ready`, `dispatched`, `running`, `handoff_pending`, `verified`, `blocked`, `failed`, `cancel_requested`, `cancelled`, `unknown`, `superseded`.

## 4. Steering or durable guidance register

| Seq. | Type | Requested at | Target | Redacted intent | Response / readback | Delivery outcome | Disposition |
|---:|---|---|---|---|---|---|---|
| 1 | `live-steer \| durable-guidance` | `<ISO>` | `<subagent ID/card>` | `<scope-preserving instruction>` | `<queued/rejected/comment receipt>` | `<landed/missed/unknown/not-live>` | `<continue/retry/replan>` |

- `live-steer` is permitted only for a currently active, steerable `delegate_task` child.
- A queued steer is not delivered proof.
- Kanban entries are `durable-guidance`; they do not claim to reach an in-flight worker.
- An immediate behavior/scope change requires stop/reclaim, prior-owner fencing, and a new attempt or work item as appropriate.

## 5. Handoff and controller verification

**Worker handoff:**

- Status: `PASS | BLOCKED | FAILED`
- Result: `<concise result>`
- Real evidence: `<commands, output references, test results, queries>`
- Changed resources: `<exact paths/resources or none>`
- Artifacts/checkpoint: `<paths, hashes, links, or N/A>`
- Risks / new work: `<none or exact item>`

**Controller verification:**

| Gate | Result | Evidence |
|---|---|---|
| Scope and ownership | `PASS \| BLOCKED \| FAIL` | `<inspection>` |
| Acceptance checks | `PASS \| BLOCKED \| FAIL` | `<commands/outputs>` |
| External readback | `PASS \| N/A \| BLOCKED \| FAIL` | `<authoritative query>` |
| Required consultation/fingerprint | `PASS \| N/A \| BLOCKED \| FAIL` | `<ledger>` |
| Lifecycle reconciliation | `PASS \| BLOCKED \| FAIL` | `<native record + ledger>` |

**Controller verdict:** `verified | blocked | failed | cancelled | unknown | superseded`

## 6. Checkpoint for a successor

- Current verified facts: `<concise references only>`
- Input/artifact fingerprints: `<exact values or N/A>`
- Prior transport/run evidence: `<IDs and terminal state>`
- Partial effects read back: `<results>`
- Unresolved blocker / decision owner: `<specific>`
- Required successor: `<new attempt ID or a new work ID; why>`

Never include credentials, raw private transcripts, unbounded tool logs, or hidden reasoning.
