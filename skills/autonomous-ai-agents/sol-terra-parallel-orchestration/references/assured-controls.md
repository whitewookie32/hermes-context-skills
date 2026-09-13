# Assured controls

Assured is an upward-only control overlay on either the Direct or Parallel execution topology. It is not a third scheduler and it does not create another class of worker. Direct and Parallel determine who executes; Assured determines how much evidence, rollback discipline, history, and independent verification are required.

Use Assured whenever a trigger below is present. Continue using `direct-mode.md` or `parallel-mode.md` for topology rules, `consultation-coverage.md` for external review, and `runtime-contract.md` for child-runtime limits.

## 1. Overlay invariants

The following invariants are mandatory:

- Assured may be enabled before execution or upgraded when new evidence raises risk.
- Assured can be added to Direct or Parallel; it never replaces either topology.
- Once a mutable external effect has begun, an Assured overlay cannot be downgraded or removed for convenience.
- Once an Assured ledger records an armed or mutation state, later revisions inherit the overlay unless the user explicitly terminates the operation under the abort rules.
- A successful child summary, consultation opinion, or command exit code never substitutes for Assured pre-state, post-state, rollback, cleanup, or deep verification.
- Missing rollback, unclear authorization, identity mismatch, or ambiguous post-state is a stop condition, not an invitation to proceed optimistically.
- History is append-only for the operation: failed attempts, partial effects, rollback, cleanup, abort, and user decisions remain visible.

Assured is not a promise that an irreversible action can be undone. For an irreversible action, the control objective is to prove authorization, scope, preconditions, evidence capture, stop conditions, and post-action state before committing the action.

## 2. Automatic triggers

Enable Assured before mutation when any one of these conditions is true:

### Risk triggers

- authentication, authorization, secrets, security boundaries, or access-control changes;
- concurrency, locking, races, deadlocks, retries, or ordering-sensitive behavior;
- migrations, schema changes, data-integrity operations, backfills, or recovery actions;
- production or customer data, service control, deployment, infrastructure, or device control;
- irreversible, destructive, externally visible, or broad-blast-radius operations;
- deletion, credential rotation, account changes, permission changes, or record/device mutations;
- an operation whose failure could corrupt, strand, duplicate, disclose, or irreversibly alter state.

### Evidence and uncertainty triggers

- the target identity, authorization, pre-state, or rollback path cannot be proven;
- a required external system is partially available or returns ambiguous state;
- a child, tool, consultation, or integration discovers an unplanned dependency or shared mutable resource;
- a material artifact changes after a review fingerprint was recorded;
- scope expands across components, public contracts, accounts, environments, or ownership boundaries;
- the user explicitly requests guarded, staged, reversible, audited, or high-assurance handling; or
- the controller cannot establish that a lower-control path is safe.

High-risk consultation classification and Assured are related but not interchangeable. A project may be Standard and still require Assured for an external effect; a Broad or High-risk project may also use Direct or Parallel under Assured controls.

When uncertain, enable Assured. Do not wait for the first mutation to decide that the mutation needed guarding.

## 3. Full Assured ledger

Create the ledger before arming the operation. Keep it in the active plan or a repo-relative workspace evidence file named by the plan. Do not store secrets, tokens, raw credentials, or unnecessary personal data in the ledger.

The ledger must contain these fields:

### Identity and scope

- operation ID, project ID, plan revision, attempt, and topology (`Direct` or `Parallel`);
- objective, business/user impact, exact in-scope targets, and explicit exclusions;
- owner, authorized decision-maker, required approvals, and escalation contact;
- consultation tier, required CLIs, review status, and artifact fingerprint when applicable;
- assumptions, known limitations, and the condition that would invalidate them.

### Preconditions and baseline

- exact target identifiers and environment/account boundary;
- authorization evidence or user instruction handle;
- observed pre-state, baseline query output, and stable artifact/resource fingerprint;
- dependency, lock, capacity, authentication, and service-health checks;
- dry-run, staging, snapshot, backup, or export result where available;
- expected state transition and invariants that must remain true.

### Action and stop conditions

- exact action, ordered substeps, owning task, and allowed tools;
- resource ownership and concurrency boundary;
- abort conditions, including pre-state drift, fingerprint mismatch, auth drift, unexpected target count, error class, timeout/transport ambiguity, or verification mismatch;
- explicit forbidden actions and scope expansion path;
- whether the action is reversible, partially reversible, or irreversible.

### Recovery and evidence

- rollback procedure for each mutable effect, with prerequisites and owner;
- cleanup procedure for temporary artifacts, processes, locks, worktrees, staged resources, and credentials;
- post-action authoritative query and deep-verification checks;
- evidence handles, command/query results, diffs, hashes, and changed-resource list;
- final disposition: `VERIFIED`, `ROLLED_BACK`, `CLEANED`, `ABORTED`, or `BLOCKED`.

### Append-only history

Record state transitions rather than rewriting fields in place. Recommended states are:

```text
PLANNED
PREFLIGHT_PASSED
ARMED
MUTATION_STARTED
MUTATION_PARTIAL
MUTATION_COMPLETED
VERIFYING
VERIFIED
ROLLBACK_STARTED
ROLLBACK_COMPLETED
CLEANUP_STARTED
CLEANUP_COMPLETED
ABORTED
BLOCKED
```

Every history entry includes revision/attempt, state, actor/owner, observed evidence, decision, and next obligation. A `MUTATION_PARTIAL` entry is required whenever an operation may have changed only part of its target set or the transport result is ambiguous.

## 4. Assured execution procedure

### Step 1 — Freeze the candidate and scope

Record the exact candidate, diff, commit, input set, target identifiers, and plan revision. For Parallel, freeze task cards and same-wave ownership. For Direct, freeze the declared single operation. Any material change after this point creates a new revision and invalidates relevant evidence.

### Step 2 — Run preflight gates

Before arming, verify:

- the objective, target, authorization, and exclusions are unambiguous;
- the current pre-state matches the ledger;
- the candidate fingerprint and required review fingerprints match;
- all dependencies and required consultation coverage are satisfied or a permitted user waiver is recorded;
- the rollback/cleanup procedure is specific, available, and owned;
- no active sibling, child, process, lock, or external operation conflicts with the action;
- dry-run, backup, snapshot, or staged checks pass when applicable; and
- the stop conditions are actionable and the authoritative verification query is ready.

If any gate fails, remain `BLOCKED` or escalate to the user. Do not arm the action.

### Step 3 — Arm and perform the smallest mutation

Record `ARMED` only after preflight passes. Perform the exact declared action in the declared order. Do not combine unrelated changes, widen target selection, or retry an ambiguous mutation without first querying state and updating the ledger.

For Parallel, each child remains a leaf and cannot create grandchildren. The controller owns the Assured ledger, integration, rollback coordination, and final decision. A child may report a bounded result, but it cannot declare the overall operation verified.

On any stop condition, enter `ABORTED` or `MUTATION_PARTIAL`, stop further mutation, and begin the recovery procedure. No downgrade to ordinary Direct or Parallel is allowed after mutation has started.

### Step 4 — Verify deeply

Deep verification is independent of the action's success response. It must include, as applicable:

- authoritative read-back of every target, not only a sampled target;
- expected state transition and invariant checks before/after comparison;
- count, identity, uniqueness, referential-integrity, permission, and ordering checks;
- neighboring service, build, integration, and regression checks;
- audit/log/event confirmation when the system exposes it;
- verification that no unintended resource, account, process, file, or device changed;
- repeatable query or independent observer evidence for ambiguous systems; and
- cleanup/teardown confirmation.

Do not mark `VERIFIED` until every applicable check passes. If any check fails, preserve the evidence and use rollback or abort rules.

## 5. Rollback, cleanup, and abort

### Rollback

Rollback is a named procedure, not a generic instruction such as “reset” or “try again.” For each effect, specify the inverse or compensating operation, prerequisites, expected post-rollback state, and verification query.

When rollback is safe and supported:

1. freeze new mutations;
2. record the failure and current observed state;
3. verify rollback authorization and target identity;
4. apply the smallest compensating action;
5. read back every affected target;
6. record `ROLLBACK_COMPLETED` only after verification; and
7. proceed to cleanup and final disposition.

If rollback is incomplete, unsupported, or would increase harm, do not improvise. Preserve the partial state, mark the operation `BLOCKED` or `ABORTED`, disclose the exact residual risk, and ask the authorized user for the next decision.

### Cleanup

Cleanup includes temporary files, snapshots that are no longer required, staging records, locks, child processes, worktrees, network sessions, generated artifacts, and credentials created solely for the operation. Never delete evidence needed for audit or rollback.

Record an owner and expected disposition for every retained resource. Verify no active child, process, lock, pending request, or external mutation remains. If cleanup cannot complete safely, leave the operation blocked with the residual resource and its owner explicit.

### Abort

Abort before mutation when authorization, target identity, pre-state, fingerprint, rollback, required review, or scope is unclear. Abort during mutation on any declared stop condition, unexpected target, partial failure, transport ambiguity, or unsafe verification result. Preserve all evidence and history.

An abort is not a failure to document. It is a valid controlled outcome only when the ledger records why the action stopped, what changed, what did not change, residual risk, rollback/cleanup status, and the next owner decision.

## 6. Revision and no-downgrade rules

A clean evidence update may append verification results without changing topology or control state. A structural revision is required when scope, target, candidate, fingerprint, dependencies, ownership, risk, rollback, consultation, or acceptance changes.

Structural revisions:

- retain every prior ledger entry and failed attempt;
- create a new revision/attempt ID;
- recompute consultation and fingerprint eligibility;
- rerun preflight before any successor mutation; and
- preserve Assured even if the revised task would otherwise appear Direct or Parallel.

After `MUTATION_STARTED`, `MUTATION_PARTIAL`, or any external side effect, no controller may downgrade the operation to a lower control profile because the remaining work looks small, the first step passed, or the user wants a faster close. The operation may finish as `VERIFIED`, be rolled back, or be aborted/blocked with residual risk.

## Verification checklist

- [ ] Direct or Parallel topology is declared separately from the Assured overlay.
- [ ] Every automatic trigger was evaluated; uncertainty enabled Assured rather than weakening controls.
- [ ] Ledger exists before arming and includes identity, scope, authorization, pre-state, fingerprint, action, stop conditions, rollback, cleanup, verification, and owner.
- [ ] Candidate and target state were frozen or fingerprinted; material changes created a new revision.
- [ ] Preflight passed before `ARMED`, including required consultation coverage and rollback/cleanup readiness.
- [ ] Mutation was limited to the declared target and ordered action; no hidden retry or scope expansion occurred.
- [ ] History is append-only and records partial failure, user decisions, rollback, cleanup, and residual risk.
- [ ] No downgrade occurred after mutation or any external effect.
- [ ] Deep verification read back every affected target and checked invariants, neighboring behavior, unintended changes, and teardown.
- [ ] Rollback was verified when used, or the operation is explicitly blocked/aborted with residual state and owner.
- [ ] Cleanup was verified without deleting evidence needed for recovery or audit.
- [ ] Final disposition is `VERIFIED`, `ROLLED_BACK`, `CLEANED`, `ABORTED`, or `BLOCKED` with real evidence.
