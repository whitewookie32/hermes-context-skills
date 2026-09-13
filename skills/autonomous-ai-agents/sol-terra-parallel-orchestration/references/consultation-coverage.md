# External CLI consultation coverage

Consultation coverage is a project-level review gate independent of Direct or Parallel topology. It governs bounded, read-only Codex and Claude consultations; it does not turn either CLI into a task owner, replace Terra execution, or replace controller verification. Committee chat is advisory and can never satisfy this gate; the rules here concern the required external coding-agent consultations.

Use this reference before the first coding dispatch and again whenever scope or risk changes. The current plan is the authoritative ledger for classification, assignments, fingerprints, attempts, evidence, fallback, waiver, and completion.

## 1. Deterministic classification

Classify the project before the first coding dispatch. If scope expands, reclassify at the next structural revision and apply the stricter tier. When uncertain, choose the higher tier. Precedence is:

```text
High-risk > Broad > Standard > Exempt
```

Any High-risk trigger overrides a breadth-only classification.

### Exempt

Exempt means no required external consultation. It applies only when there is no source, test, build, runtime-configuration, data-shape, public-output, or behavior change, or when the work is purely mechanical documentation/formatting whose acceptance check proves semantic identity.

Examples include whitespace-only changes, presentation-only formatting, or a typo correction whose rendered meaning and commands are unchanged. A documentation edit that changes an instruction, command, route, safety rule, public promise, or example is not Exempt.

Do not create quota-filling review calls for Exempt work. Any uncertain or behavior-affecting code/configuration change is at least Standard.

### Standard

Standard is a bounded behavior-affecting change in one component with limited blast radius and no Broad or High-risk trigger.

Default mode: optional. A useful available reviewer may be selected by the deterministic Codex/Claude preference; no optional CLI creates a login or completion dependency. If the user or task acceptance contract explicitly requires review, assign it before dispatch to an atomic task with `Mode: required`; then require one successful verified consultation, honoring any named-CLI pin.

### Broad

Broad is a materially cross-cutting change with no High-risk trigger, including:

- multiple components or repositories;
- a public contract, user-visible API, or shared integration boundary;
- multiple implementation leaves whose outputs must integrate;
- a change that crosses normal ownership boundaries; or
- a broad behavior or compatibility impact.

Default mode: optional. Use available Codex and Claude perspectives only when materially useful. Explicitly required named reviews remain required and cannot be substituted silently when the user or task acceptance contract names them; those assignments are independently verified against the reviewed artifact. A controller-authored plan must not manufacture an authentication dependency for otherwise optional work.

### High-risk

High-risk includes any:

- auth, authorization, security, credential, or access-control work;
- concurrency, locking, race, deadlock, ordering, or retry-safety work;
- migration, schema, data-integrity, recovery, or destructive data operation;
- production-control, deployment, infrastructure, device, account, or customer-data action;
- irreversible operation or broad blast-radius behavior; or
- change whose failure could corrupt, disclose, duplicate, strand, or irreversibly alter state.

High-risk optional review may use Codex and Claude perspectives on the final immutable candidate, exact final diff, or immutable commit when materially useful, the same default mode as Standard/Broad; a review of an earlier draft does not satisfy any accepted High-risk evidence. If the user or task acceptance contract explicitly requires named review(s), assign `Mode: required` before dispatch and require successful independently verified evidence from the named CLI(s) before completion.

## 2. Deterministic pre-review gate

Consultation must not be dispatched until the deterministic candidate gate passes. Those checks may pass while consultation is unavailable; consultation blocks project completion, not deterministic validation.

Perform these checks in order:

1. Freeze the project scope, exclusions, task registry, dependencies, ownership, and acceptance criteria in the current plan revision.
2. Classify the tier and record the evidence-backed rationale.
3. Confirm every required consultation has an atomic task ID, CLI, purpose, `Mode: required`, read/write permission, call budget, turn budget, and evidence contract.
4. Run the candidate's deterministic acceptance, regression, build, lint, type, schema, integration, and safety checks that apply.
5. Confirm there are no unverified active child results, unresolved local conflicts, unexplained changed paths, or pending external mutations in the review candidate.
6. Create the review-eligibility fingerprint only after the checks pass. Until then, record fingerprint `none` and keep required consultation tasks `blocked`.
7. Select the required CLI using the helper contract and record the selector evidence without treating selection as a reservation.

A bounded diagnostic within existing authorized scope/cost may run before the deterministic gate without routine re-approval; mark it optional/non-coverage and never count it as required final review. New cost, data exposure, or scope needs authorization. Repair a failed deterministic gate before any required review.

## 3. Fingerprint binding

Bind every consultation to the exact post-regression artifact that was reviewed. The fingerprint may be the SHA-256 of:

- the complete immutable candidate tree;
- the exact final diff with stable serialization; or
- an immutable commit, when that commit is the accepted artifact.

Record the fingerprint, artifact kind, scope, revision, CLI, task ID, and review result in the plan and consultation ledger. High-risk reviews must match the final artifact accepted by the integration gate; Broad reviews should use the same binding, and Standard reviews must identify the reviewed candidate clearly.

Any material change to source, tests, configuration, generated output, dependency, task scope, public contract, or relevant behavior invalidates prior coverage. Run deterministic checks again and produce the successor fingerprint. Required coverage needs a budgeted delta review; optional stale evidence is disclosed and need not trigger another call unless materially useful within budget. If the fingerprint is unchanged, reuse valid successful evidence rather than repeating a call.

A successful consultation is advisory evidence, not an approval. The controller must independently inspect the findings, verify changed paths, and decide the disposition.

## 4. Deterministic rotation and ledger contract

After `skill_view` resolves this skill's directory, invoke `python <skill-dir>/scripts/cli_consultation_ledger.py` through `terminal`. The helper is skill-relative and must not be resolved from the active workspace root. It stores exactly this metadata:

- project ID and task ID;
- CLI (`codex` or `claude`);
- purpose, status, and timestamps.

The helper does not store artifact fingerprints, revision data, findings, prompts, source text, secrets, credentials, command text, or raw consultation output. Record fingerprints, revision lineage, concise findings, and controller disposition in the active plan or Assured ledger. Keep any separately authorized evidence artifact under the active workspace with the narrowest possible access and record only its path or handle in the plan.

The helper's committed global ledger uses a cross-process transaction lock. Selection is success-balanced and deterministic:

1. prefer the CLI with the fewest successful uses;
2. then prefer a CLI with no successful use or the oldest successful use; and
3. use Codex as the stable tie-break.

The selection is a preference, not a reservation. Concurrent controllers may receive the same preference until a successful record is committed. Record a helper result only after the controller independently verifies that the consultation ran with the intended purpose, permissions, artifact fingerprint, and exit/result state; keep the fingerprint evidence in the plan because it is outside the helper schema.

Canonical commands are:

```text
python <skill-dir>/scripts/cli_consultation_ledger.py select --tier standard --project-id <project-id>
python <skill-dir>/scripts/cli_consultation_ledger.py record --project-id <project-id> --task-id <task-id> --cli codex|claude --purpose <purpose> --status success|unavailable|failed
python <skill-dir>/scripts/cli_consultation_ledger.py status [--project-id <project-id>]
```

Use the installed helper's current syntax and inspect its real output. Do not hand-edit the committed ledger or infer success from a selected preference.

## 5. One-shot review and repair budgets

Before execution, declare a finite project-owned call/turn budget within existing authorized scope/cost: normally one initial review plus up to two delta-scoped repair reviews per selected CLI, read-only on the exact eligible artifact, when new evidence and a changed fingerprint justify each repair call.

Continue automatically inside that budget; no routine user approval is needed per round. On exhaustion, the Chairman reassesses internally; do not add calls, erase consumed budget, or claim missing required coverage passed. A real additional cost/scope authorization or missing user-only decision may require escalation. Required missing evidence remains blocked, never waived by replanning.

The repair brief must name the changed behavior/files/resources, relevant dependents, new evidence, successor fingerprint, and why the initial result is insufficient. It must not repeat an unrestricted review of unchanged artifacts.

A plan revision must never become a pretext for resetting budget on revision: do not repeat an identical prompt, reset the budget merely because the plan advanced, schedule quota-filling calls, consult Exempt work, or exceed the declared call budget. Each permitted additional round requires a newly recorded material purpose and successor fingerprint, not a routine user prompt. A consultation process must not commit, push, open a pull request, edit global configuration, access secrets, or make unrelated changes.

Default purposes:

- Codex: repository-aware diff, test, implementation, or optimization critique.
- Claude: architecture, correctness, maintainability, user-impact, or independent design critique.

Both outputs remain advisory. The controller reads the exact candidate and verifies every material finding before accepting, repairing, or rejecting it.

## 6. Fallback and waiver rules

Record every unavailable or failed attempt, including CLI, task ID, purpose, status, reason, exit state, artifact fingerprint if known, and impact.

### Standard fallback

Classify optional versus required before preflight. For optional unavailability, record `UNAVAILABLE_OPTIONAL` and missing coverage in the plan (`unavailable` in the metadata helper); continue other checks without requesting login. One available alternate may be used within budget. For explicitly required Standard review not pinned to a particular CLI, one successful independently verified alternate may satisfy the requirement; if none succeeds, required coverage remains blocked. Never substitute an alternate for an explicitly named reviewer.

### Broad and High-risk handling

Broad and High-risk reviews are optional unless explicitly required; unavailable optional reviewers do not block completion at either tier. Any explicitly required named review remains required at every tier, including High-risk. Do not silently substitute a different CLI, Terra review, controller review, or committee advice for missing required evidence. Use already-authorized sessions and supported recovery paths, without exposing credentials or bypassing authentication/MFA; a genuinely unavailable required reviewer remains a blocker.

If a required CLI remains unavailable or fails after safe recovery, complete independent verification but leave the required coverage blocked. A waiver is possible only when the governing requirement permits one and the user explicitly grants it after receiving:

- the concrete failed or unavailable check;
- the exact artifact and fingerprint not independently reviewed;
- the affected scope and residual risk;
- the compensating controller/Terra checks that did pass; and
- the decision to proceed despite the missing independent perspective.

Only the user can waive a waivable required review; Sol cannot self-waive, and non-waivable safety requirements remain binding. Record the user's authority, date/handle, exact waived scope, disclosed risk, and evidence in the plan. Never treat a waiver as a successful review or waive a non-waivable safety requirement; a waiver is not a successful consultation and does not erase the failure, so completion remains visibly conditional on it.

If the required consultation was not assigned as `Mode: required`, an optional result cannot be retroactively counted. Create a valid assignment before the next eligible call and preserve the earlier advisory result separately.

## 7. Evidence and completion gate

A required consultation record is complete only when it contains:

- the exact required task ID and CLI;
- `Mode: required`, purpose, permissions, and budget;
- successful execution evidence and exit/result state;
- the post-regression artifact fingerprint;
- concise grounded findings and controller disposition;
- independently verified changed paths or no-change result;
- any failure/unavailability and fallback or waiver record; and
- revision/repair lineage.

The consultation verdict is `PASS` only for successful independently verified required coverage, including a permitted successful fallback. Record `WAIVED_CONDITIONAL` for a permitted explicit user waiver, never PASS. Exempt work records its exemption; Standard/Broad/High-risk work with no required assignment records `OPTIONAL_ONLY`, disclosing missing optional coverage without blocking other verified completion. Do not present any of those statuses as evidence that an unrun review occurred.

Final completion remains blocked when:

- deterministic checks did not pass for the final candidate;
- a required successful consultation is missing or not bound to the final artifact;
- a required review fingerprint does not match the accepted final artifact;
- a material post-review change invalidates required coverage and remains unreviewed;
- a required CLI failed and no permitted fallback/waiver exists; or
- the controller has not independently verified relied-upon consultation results and all material findings.

Consultation coverage is one final integration gate among requirements, tests, external-state read-back, cleanup, and Assured obligations. It never authorizes unsafe execution or replaces the user's decision on an unresolved risk.

## Verification checklist

- [ ] Tier was classified before first coding dispatch with evidence and precedence `High-risk > Broad > Standard > Exempt`.
- [ ] Exempt work proves semantic identity and did not create quota-filling calls.
- [ ] Standard/Broad reviewers were classified optional versus explicitly required before dispatch; optional unavailability and missing coverage were disclosed without login/completion blockers.
- [ ] Explicitly required named reviews, at any tier including High-risk, have successful matching evidence or a permitted user-only waiver with concrete residual risk, visibly conditional and never recorded as review PASS. High-risk work with no explicit requirement records `OPTIONAL_ONLY` like Standard/Broad.
- [ ] Every required consultation maps to an atomic task with `Mode: required`, CLI, purpose, permissions, call budget, turn budget, and evidence contract.
- [ ] Deterministic acceptance/regression checks passed before required review dispatch.
- [ ] Review eligibility fingerprint was created only after those checks and is bound to the exact artifact reviewed.
- [ ] Any material post-review change invalidated prior coverage; required coverage received a successor fingerprint and budgeted delta review, while unused optional evidence stayed marked stale.
- [ ] Rotation used the committed global ledger's least-success/oldest-success/Codex tie-break rule; selection was not mistaken for reservation.
- [ ] Initial and repair budgets were respected; no identical, quota-filling, or unauthorized extra call occurred.
- [ ] Ledger contains metadata and concise verified evidence only, never secrets, prompts, source text, credentials, command text, or raw output.
- [ ] Controller independently verified every material consultation finding and reviewed changed paths.
- [ ] Final consultation verdict and artifact fingerprints agree with the final integration gate.
