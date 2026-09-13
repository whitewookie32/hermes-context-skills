# Direct mode

Direct is the no-delegation execution topology. The controller owns the complete task, performs the work in the current session, and verifies the result without creating Terra children. Direct is not a lower-safety mode: consultation tier and the Assured overlay are selected independently and still apply.

Use this reference when the objective is best kept under one owner. Use `parallel-mode.md` when independent, isolatable work can pass the break-even invariant. Use `assured-controls.md` whenever an Assured trigger is present, regardless of topology.

## 1. Direct classification

Choose Direct when all of the following are true:

- One owner can perform the objective without handing off an independent deliverable.
- The work is one coherent transaction, state transition, investigation, or tightly coupled edit.
- Splitting would duplicate context, create shared mutable ownership, or add coordination and verification work that outweighs the parallel benefit.
- The controller can name one authoritative output and one acceptance check.
- All prerequisites are known, or uncertainty can be resolved without creating a second owner.

Direct remains appropriate for a large but indivisible operation. Do not split a migration, transaction, tightly coupled refactor, or state transition merely to use available capacity.

Direct is not appropriate when two or more leaves have independently verifiable outcomes, disjoint mutable ownership, explicit inputs, and a positive parallel break-even result. Reclassify to Parallel before mutation when that condition becomes clear.

Topology and controls are separate axes:

| Axis | Direct decision | Independent control |
|---|---|---|
| Execution topology | Controller performs all work; no `delegate_task` call | Parallel may be selected later if the DAG proves a benefit |
| Consultation tier | Exempt, Standard, Broad, or High-risk still applies | Required external reviews are not Terra children |
| Assurance | Baseline controls or Assured overlay | Any Assured trigger upgrades Direct; it never creates a third topology |

When classification is uncertain, choose the safer coherent topology or ask for the one missing decision. If the delegation runtime is unavailable, Direct is a permitted fallback only when the objective still satisfies every Direct ownership, scope, and verification condition; otherwise report Parallel as blocked. Never choose Parallel only because capacity exists.

## 2. No-delegation workflow

### Step 1 — Inspect authoritative context

Gather the user requirement, repository instructions, current state, relevant source and tests, live-system facts needed for the requested effect, and explicit safety boundaries. Resolve retrievable unknowns with the available read tools. Record assumptions that could change scope or safety.

The Direct path must not call `delegate_task`, spawn a Hermes child, or ask a child to perform a subtask. A required Codex or Claude consultation is a separate project-level review gate, not an execution child; it is allowed only under `consultation-coverage.md`, after deterministic regression checks pass, and with the exact permissions and budget recorded in the plan.

### Step 2 — Classify the change

Record:

- topology: `Direct`;
- consultation tier and evidence-backed rationale;
- whether the Assured overlay is active;
- objective, in-scope resources, exclusions, and assumptions;
- the single owner and the exact deliverable;
- the acceptance criterion and verification command/query;
- expected external effects, if any; and
- the escalation condition if the work stops being atomic.

Do not infer that documentation is mechanical merely because it is in Markdown. Inspect whether it changes instructions, examples, public output, routing, safety behavior, or a contract.

### Step 3 — Establish the trace floor before mutation

Create the compact Direct trace in the active plan or task record before making a behavior-changing edit or external mutation. The trace may be concise, but it must retain enough evidence to reconstruct what was authorized and what was verified.

The minimum record is:

```text
Mode: Direct
Objective: <one concrete outcome>
Scope: <owned paths/resources and explicit exclusions>
Classification: <mechanical | behavior-changing | external-effect>
Consultation: <exempt | standard | broad | high-risk; rationale>
Assured: <off | on; trigger or rationale>
Inputs/pre-state: <authoritative paths, queries, handles, or fingerprints>
Acceptance: <binary criterion>
Verification: <exact command/query/read-back>
Result: <PASS | BLOCKED | FAILED>
Evidence: <real output, diff, handle, or read-back>
Changed resources: <exact paths/resources, or none>
Rollback/cleanup: <exact action, or not applicable>
Risks/escalation: <open items, or none>
```

The trace does not replace the detailed plan when the project is broad or assured. It is the minimum Direct evidence, not permission to omit required consultation, rollback, or verification records.

### Step 4 — Execute once under the declared boundary

Perform only the declared operation. Keep reads, edits, builds, tests, and external calls within the stated ownership boundary. Do not add opportunistic cleanup, unrelated refactoring, or quota-filling review work.

For a behavior-changing edit, preserve the pre-change state needed for comparison and keep the working candidate stable until its checks pass. For an external effect, confirm authorization, target identity, and pre-state immediately before the action. If a precondition differs from the trace, stop and reclassify rather than silently widening scope.

### Step 5 — Verify the result independently

Use the acceptance check named in the trace, then perform the checks appropriate to the change class:

1. **Spec gate:** the result satisfies every stated criterion and does not exceed scope.
2. **Quality gate:** relevant tests, lint, type checks, builds, parsers, render checks, or invariant checks pass.
3. **Diff/state gate:** every changed path or external resource is accounted for; no unexplained mutation remains.
4. **External-effect gate:** query the authoritative system after the action and compare the observed state with the expected transition.
5. **Cleanup gate:** temporary files, locks, processes, worktrees, credentials, and pending operations are absent or explicitly retained with an owner and reason.

A command that exits successfully is evidence for that command only. It is not proof that the requested behavior, integration, or external state is correct.

### Step 6 — Close or escalate

Mark the Direct task `done` only after all applicable gates pass and the trace contains real evidence. Mark it `BLOCKED` when a user decision, required review, unavailable authoritative system, or safety precondition prevents completion. Mark it `FAILED` when the operation ran but its acceptance check failed; preserve the attempt and create a focused repair record rather than rewriting history.

## 3. Mechanical versus behavior-changing work

This distinction controls verification and consultation. It does not excuse a weak acceptance check.

### Mechanical change

A change is mechanical only when its intended semantic result is identity-preserving and all of these are true:

- no source behavior, test behavior, build behavior, runtime configuration, data shape, public output, or external state changes;
- the edit is limited to formatting, whitespace, ordering with proven semantic identity, typo-only documentation, or equivalent presentation work;
- the acceptance check can prove semantic identity rather than merely showing that a file was written; and
- no hidden instruction, command, example, route, or safety meaning changes.

Use a normalized or parser-aware comparison where appropriate. For documentation, compare the rendered or extracted meaning when formatting could alter a code block, link, table, heading, or instruction. If semantic identity cannot be proven, classify the change as behavior-changing.

Mechanical status does not authorize quota-filling consultation. It does require a trace, a bounded diff, and an identity-preserving verification result.

### Behavior-changing change

Treat a change as behavior-changing if it changes or may change any code path, configuration value, dependency, test expectation, generated artifact, public contract, runtime route, data schema, security boundary, model/provider selection, user-visible instruction, or external resource. Uncertainty is behavior-changing.

For behavior-changing work:

- run deterministic acceptance and regression checks before required external consultation;
- classify Standard, Broad, or High-risk using `consultation-coverage.md`;
- preserve a candidate fingerprint when consultation is required;
- verify the final diff and relevant neighboring behavior; and
- apply Assured controls when any trigger in `assured-controls.md` is present.

## 4. External effects

An external effect includes changing a record, account, device, service, process, branch, repository, deployment, message, schedule, credential, or other state outside the local uncommitted read-only view.

Before an external effect, record:

- exact target identity and authorization boundary;
- observed pre-state and any baseline fingerprint;
- intended transition and why it is in scope;
- reversibility, rollback action, and cleanup owner;
- abort conditions; and
- the authoritative post-action query.

After the action, read back the exact target. If the read-back is unavailable, ambiguous, or inconsistent, do not claim success. Freeze further mutations, preserve the evidence, and escalate to Assured or to the user as appropriate. If the action is irreversible, high-impact, or destructive, Assured is mandatory before mutation.

## 5. Escalation rules

Escalate from ordinary Direct controls to the appropriate stronger path when:

- a second independently verifiable deliverable appears and the parallel break-even invariant becomes positive;
- the scope crosses components, public contracts, or mutable ownership boundaries;
- auth, security, concurrency, migration, data integrity, production control, irreversible operation, or broad blast radius appears;
- the pre-state, target, authorization, or rollback path is unclear;
- a required consultation cannot be completed under the tier rules;
- verification fails or reveals an unplanned change; or
- the user changes the objective or acceptance criteria.

A topology change before mutation creates a new plan revision and re-runs the completeness gate. Once a mutable external effect has begun, do not downgrade an active Assured overlay; use the Assured abort, rollback, cleanup, and history rules instead. Never hide an escalation by editing the original Direct trace.

## Verification checklist

- [ ] The objective has one concrete outcome, one owner, explicit scope, and an observable acceptance check.
- [ ] Direct was selected for atomicity or non-positive parallel break-even, not for convenience or capacity scarcity.
- [ ] No `delegate_task`, child process, or hidden execution owner was used.
- [ ] Mechanical versus behavior-changing classification is evidenced; uncertainty was treated as behavior-changing.
- [ ] Consultation tier was classified independently of topology, and required coverage was not skipped.
- [ ] Assured triggers were evaluated before mutation and applied when any trigger matched.
- [ ] Compact trace floor records inputs/pre-state, acceptance, verification, result, changed resources, cleanup, and risks.
- [ ] Spec, quality, diff/state, external-effect, and cleanup gates passed where applicable.
- [ ] Every external target was read back from its authoritative system.
- [ ] Failures, blocked decisions, and repair attempts preserve history and do not claim completion.
- [ ] Final status is `PASS`, `BLOCKED`, or `FAILED` with real evidence and exact changed resources.
