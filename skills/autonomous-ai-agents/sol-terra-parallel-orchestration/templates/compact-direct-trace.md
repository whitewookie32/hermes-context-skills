# `<Objective>` — Direct Execution Trace

> Use this compact template for one controller-owned, dependency-ordered execution. **Direct** is a topology choice, not a consultation tier. Add `assured-ledger.md` when the execution needs the Assured overlay. If the work contains independently verifiable leaves, use `parallel-plan.md` instead of hiding fan-out in a Direct trace.

## 1. Identity and decision

| Field | Value |
|---|---|
| Plan ID | `<stable project/plan ID>` |
| Revision | `Revision <N> — <descriptive milestone>` |
| Status | `PLANNING \| EXECUTING \| VERIFYING \| COMPLETE \| BLOCKED \| ABORTED` |
| Controller/owner | `<accountable controller or owner>` |
| Topology | `Direct` |
| Project consultation tier | `exempt \| standard \| broad \| high-risk` |
| Assured overlay | `OFF \| ON` |
| Assured ledger | `<linked ledger ID/path or N/A>` |
| Capacity readback | `N/A for Direct; no parallel dispatch` |
| Created / updated | `<ISO timestamps>` |

**Topology decision:** `<why this is one coherent, linear operation and cannot be safely split into independent leaves>`  
**Tier decision:** `<evidence for the project-level consultation tier; tier is selected independently of Direct topology>`  
**Assured decision:** `<why the overlay is OFF or why full traceability/state proof is ON>`

## 2. Objective and boundaries

**Requested outcome:**  
`<one observable statement of the final result>`

**Authoritative inputs:**

- `<user requirement, contract, or source>`
- `<repository/system state readback>`
- `<decision or constraint>`

### In scope

- `<included result or resource>`

### Exclusions

- `<explicitly excluded resource, behavior, deployment, or cleanup>`

### Constraints and invariants

- `<safety, ownership, compatibility, privacy, or process constraint>`
- `<No fixed duration target; progress is evidence- and gate-based.>`
- `<If a prerequisite or destructive boundary is unclear, stop and report the concrete blocker.>`

## 3. Assumptions

| ID | Assumption | Evidence | Impact if false | Resolution owner | State |
|---|---|---|---|---|---|
| A1 | `<assumption>` | `<source/readback>` | `<specific blocked or unsafe outcome>` | `<owner/user>` | `open \| confirmed \| rejected` |

An unconfirmed assumption that affects scope, identity, safety, or external mutation blocks the affected gate; do not silently convert it into a fact.

## 4. Affected resources and ownership

| Resource/handle | Read or mutate | Exact owner | Pre-state evidence | Conflict control | Cleanup owner |
|---|---|---|---|---|---|
| `<repo path, record, account, device, process, or service>` | `read \| mutate` | `<owner>` | `<hash/query/status>` | `serialized \| isolated \| none` | `<owner or N/A>` |

No sibling or unlisted resource may be modified. Record every changed resource in Section 8, including generated or deleted artifacts.

## 5. Acceptance contract

The trace is complete only when every applicable box is checked and the verdict is `PASS`.

- [ ] The requested outcome is observable and matches the objective.
- [ ] Every requirement is mapped to a concrete action and a binary check.
- [ ] Preconditions and ownership checks pass.
- [ ] The deterministic validation set passes without skipped or incomplete required checks.
- [ ] Any required consultation coverage is `PASS`; optional advice is not counted as required evidence.
- [ ] For high-risk work, every required reviewer saw the exact accepted fingerprint and all fingerprints match.
- [ ] Every external mutation has an authoritative readback matching the intended result.
- [ ] Rollback, cleanup, and teardown obligations are complete, or explicitly `N/A` with evidence.
- [ ] No unexplained `active`, `pending`, `failed`, `blocked`, `unknown`, or `cleanup-required` state remains.

**Acceptance verdict:** `PASS \| BLOCKED \| ABORTED`  
**Defects or exceptions:** `<none, or exact gate and evidence>`

## 6. Deterministic validation

Run these checks before any token-consuming consultation. A consultation may be pending while deterministic checks finish, but it cannot be recorded as review-eligible until the post-regression candidate passes.

| Check ID | Check/command/query | Expected binary result | Actual evidence | Status |
|---|---|---|---|---|
| V1 | `<precondition, unit, lint, build, query, or invariant check>` | `PASS` | `<exit status/output/handle>` | `PASS \| FAIL \| BLOCKED` |
| V2 | `<integration/regression check>` | `PASS` | `<exit status/output/handle>` | `PASS \| FAIL \| BLOCKED` |
| V3 | `<scope/diff/readback check>` | `PASS` | `<hash/diff/query>` | `PASS \| FAIL \| BLOCKED` |

**Deterministic gate:** `PASS \| BLOCKED`  
**Review-eligibility fingerprint:** `<SHA-256 of the post-validation candidate/diff/immutable commit, or NONE until the gate passes>`

## 7. Consultation assignments and results

Consultation coverage is project-level and independent of topology. Use the configured deterministic selector/ledger; record metadata only, never secrets, prompts, source text, or raw output.

**Classification evidence:** `<why exempt/standard/broad/high-risk>`  
**Selector evidence:** `<relative selector command or recorded helper result>`  
**Required minimum:** `<none for optional Standard/Broad/High-risk; named explicitly required reviews only, at any tier>`  
**Regression status:** `incomplete \| failed \| passed`  
**Fallback/waiver:** `<N/A, permitted standard fallback with evidence, or explicit user waiver for broad/high-risk>`

| Assignment task ID | CLI | Mode | Purpose | Permissions/budget | Fingerprint reviewed | Status | Independent verification |
|---|---|---|---|---|---|---|---|
| `<consultation task ID>` | `Codex \| Claude` | `required \| optional` | `<bounded purpose>` | `<read-only/bounded; call and turn limits>` | `<SHA-256 or N/A>` | `planned \| success \| unavailable \| failed` | `<owner/check/result>` |

Rules:

- Required assignments must have `Mode: required` and an atomic task ID; an informal comment never satisfies coverage. Standard/Broad reviews are optional unless explicitly required; disclose optional unavailability as `UNAVAILABLE_OPTIONAL` (`unavailable` in the helper), not a login/completion blocker.
- Required review follows passing deterministic validation. A bounded optional diagnostic within existing authorized scope/cost may run earlier without routine re-approval, but is non-coverage. New cost, data exposure, or scope still needs authorization.
- Reuse successful evidence when the fingerprint is unchanged. Any material change requires deterministic validation again; required coverage needs a budgeted delta review, while unused optional evidence stays marked stale.
- Declare a finite call/turn budget, normally one initial plus up to two evidence-backed delta reviews per selected CLI within authorized scope/cost. Continue within it automatically. Exhaustion triggers Chairman reassessment, not a per-round user prompt, reset, or silent excess call; missing required coverage remains pending.
- High-risk completion is blocked unless both required independent fingerprints match the final accepted artifact, or the user records an explicit waiver after the concrete risk is disclosed.

**Consultation coverage verdict:** `PASS \| BLOCKED \| OPTIONAL_ONLY \| EXEMPT \| WAIVED_CONDITIONAL` (never count missing/waived review as successful)

## 8. Changed resources

| Resource | Before | Intended after | Actual after | Evidence | Rollback/cleanup |
|---|---|---|---|---|---|
| `<path/record/device/service>` | `<pre-state>` | `<intended state>` | `<readback>` | `<diff/hash/query/handle>` | `<action or N/A>` |

Include created, modified, deleted, renamed, registered, started, stopped, or externally updated resources. If no resource changed, write `none` and cite the read-only evidence.

## 9. External-effect readback

Complete this section for every side effect outside the local candidate. A successful command is not proof until the exact target is read back from the authoritative system.

| Effect ID | Target and operation | Intended value/state | Readback query/source | Observed value/state | Match | If mismatch |
|---|---|---|---|---|---|---|
| E1 | `<exact target and mutation>` | `<expected>` | `<authoritative query/handle>` | `<observed>` | `YES \| NO` | `<abort/rollback/escalate>` |

**External-effect gate:** `PASS` only if every applicable row is `YES`; otherwise `BLOCKED` or `ABORTED`.

## 10. Risks and limitations

| ID | Risk/limitation | Trigger/evidence | Mitigation | Residual impact | State |
|---|---|---|---|---|---|
| R1 | `<risk or limitation>` | `<condition>` | `<bounded mitigation>` | `<remaining impact>` | `open \| accepted \| closed` |

State explicitly when Direct was chosen despite a coupled operation, when review evidence is advisory rather than proof, and when an unavailable authoritative system prevents completion.

## 11. Final verdict

| Gate | Required result | Actual result | Evidence |
|---|---|---|---|
| Scope and ownership | `PASS` | `PASS \| BLOCKED \| FAIL` | `<evidence>` |
| Deterministic validation | `PASS` | `PASS \| BLOCKED \| FAIL` | `<evidence>` |
| Consultation coverage | `PASS` or permitted `N/A` | `PASS \| BLOCKED \| FAIL` | `<ledger/evidence>` |
| High-risk fingerprint gate | `PASS` or permitted `N/A` | `PASS \| BLOCKED \| FAIL` | `<matching hashes or N/A>` |
| External-effect readbacks | `PASS` or permitted `N/A` | `PASS \| BLOCKED \| FAIL` | `<readbacks>` |
| Cleanup and unresolved-state audit | `PASS` | `PASS \| BLOCKED \| FAIL` | `<evidence>` |

**Final verdict:** `PASS \| BLOCKED \| ABORTED`  
**Final evidence:** `<exact commands, outputs, paths, hashes, queries, or handles>`  
**Open decision required:** `<N/A or one concrete user decision>`  
**Completed at:** `<ISO timestamp>`
