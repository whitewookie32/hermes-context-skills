# Runtime contract

This reference defines the runtime boundary for Sol–Terra execution. It is deliberately narrow: installation-owned routing and capacity are discovered from the active Hermes delegation contract; children receive fresh self-contained context; children are leaves; and, only when the public/model-facing contract is verified, the controller evaluates a consolidated batch-completion result. Do not infer unsupported behavior from local logs, configuration shape, or historical smoke tests.

## 1. Installation-owned routing and capacity

The active installation owns the values for:

- controller model and provider;
- delegated child model and provider;
- controller and child reasoning policy;
- controller and child model-tier policy (Sol versus Luna), including the tier-to-route floor table and `auto` resolution defined in `SKILL.md`;
- enabled child toolsets/capabilities;
- maximum concurrent children;
- maximum spawn depth;
- child iteration/turn limits and timeout policy; and
- whether the public delegation and batch-completion contracts are available.

The skill references do not set, override, or promise a particular model slug, provider, capacity number, timeout, or toolset. A plan records the values discovered at preflight as evidence, but a task card cannot change them. Do not pass per-task model, provider, reasoning, or capacity overrides to `delegate_task`.

Before dispatch, inspect the active installation-owned route and supported tool contract. Distinguish requested policy from observed runtime facts; untraced effort/wire values remain unknown. Verify explicit user route pins and capabilities required for safety or acceptance, including leaf role, ownership, capacity, and spawn depth. If one of those required facts is missing, malformed, stale, or contradictory, block the affected lane and record the defect. An unverified preferred model label alone does not require user model selection; continue on the current supported route when safe, without inventing proof or changing global settings.

Capacity is a ceiling, not a target. Let `C` be the verified installed maximum concurrent children for this session. A batch has at most `C` leaves. Do not infer `C` from a plan template, an old transcript, a worker count in documentation, or a historical configuration snapshot.

The controller remains on the installation-owned session route unless an authorized supported change is required. If an explicit route/provider pin cannot be met, do not substitute silently. Use Direct when it safely meets the objective and all explicit constraints; otherwise report the exact runtime blocker after supported self-service checks.

## 2. Fresh child context

A child does not inherit the parent transcript as an implicit contract. Every leaf receives a fresh context containing only the task information needed to execute and verify its assignment:

- stable task ID, plan revision, attempt, and one concrete objective;
- parent requirement and downstream purpose;
- authoritative repo-relative paths, URLs, handles, and current facts;
- verified dependencies and their outputs;
- exact read, write, tool, account, device, and process boundaries;
- deliverable, binary acceptance criteria, and verification method;
- rollback and cleanup obligations;
- external-agent assistance mode, permissions, and budget if relevant; and
- the output contract: status, result, real evidence, changed resources, and risks/open work.

Pass paths rather than copying unrelated large files. Do not pass secrets, credentials, auth stores, or parent-only assumptions. If a fact is absent from the brief, first retrieve it from allowed resources or use a safe in-scope default. Report `BLOCKED` only for a non-retrievable material prerequisite or authority/safety ambiguity; never discover a new scope or ask a grandchild. The Chairman resolves ordinary gaps and continues, involving the user only when truly necessary.

A fresh context is a safety boundary, not merely a prompt style. The controller remains accountable for planning, routing, integration, verification, consultation coverage, and final completion.

## 3. Leaf and spawn-depth contract

Every delegated task uses the leaf role. A Terra leaf:

- performs one atomic assignment only;
- may use only the capabilities named in its brief;
- may not create grandchildren, delegate another task, spawn a Hermes process, or form a new team;
- may not change global configuration, routing, credentials, or unrelated resources;
- reports a result but cannot declare the project complete; and
- stops and reports `BLOCKED` or `FAILED` when the brief's prerequisites or safety boundary fails.

The installation's maximum spawn depth must be verified as one for this workflow. A child request to delegate, recruit, or widen scope is a contract violation; the controller records it, stops the affected leaf, and repairs or aborts under the topology and Assured rules.

External Codex or Claude assistance, when explicitly allowed by the task card and consultation policy, is bounded assistance under the leaf owner. It is not a Hermes grandchild and does not permit the CLI to spawn additional agents or exceed the named permissions and call budget.

## 4. No per-task routing override

Task cards express task risk, purpose, tools, acceptance, and verification. They do not select:

- model slug;
- provider or endpoint;
- reasoning effort;
- child timeout or iteration policy;
- concurrency capacity; or
- a different toolset than the installation exposes.

The controller sends one batch of complete leaf tasks through the supported delegation interface and lets the installation resolve the model/provider/capacity contract. A brief that attempts to override routing is invalid and must be corrected before dispatch. This prevents a task prompt from silently moving work to an unapproved model or provider. The tier-driven auto-router in §7 and `SKILL.md`'s tier-to-route floor table is not an exception to this rule: it resolves model tier and reasoning effort from the task's own risk/complexity classification at the installation-owned routing layer, never from a field the task card or brief supplies directly.

## 5. Model-facing batch completion (capability-contingent)

A Parallel wave may follow this state machine only after preflight verifies that the active installation's supported public/model-facing contract provides consolidated batch completion:

```text
planned -> ready -> dispatched -> running -> model-facing batch complete
        -> handoff_pending -> controller verification -> verified
        -> blocked | failed | cancel_requested -> cancelled | unknown
```

The controller performs these steps:

1. Build a wave of ready, independent tasks no larger than installed capacity `C`.
2. Call `delegate_task` once with the complete batch and record the delegation ID plus every returned child ID under its `work_id`/`attempt_id`.
3. Record `dispatched` on the accepted response; move to `running` only when the supported status surface reports that exact child active.
4. Do not claim success, write a requested final marker, or close the plan on the dispatch response.
5. Do not poll, sleep, inspect live child transcript files, or busy-wait for results.
6. Wait for the exact public/model-facing completion signal defined by the verified contract for that delegation ID.
7. Map a terminal child result to `handoff_pending`, independently verify it, then record `verified`, `blocked`, or `failed`.

The consolidated result must account for the dispatched batch and identify each task's status/result/evidence. Missing, partial, contradictory, or unbound results leave the wave pending or blocked; they do not count as success. A child result that says `PASS` is not the controller's final verification.

If the installed delegation surface does not provide, or preflight cannot verify, the public/model-facing completion contract, do not dispatch a Parallel wave that relies on it and do not emulate it by reading internal cache files, daemon state, logs, or live transcripts. Use Direct when safe, or report Parallel as unsupported/`BLOCKED`. A historical event, a tool-schema field, or a private implementation detail is not a runtime guarantee, and no particular completion event is guaranteed across Hermes installations.

## 6. Narrow capability discovery

Capability discovery is limited to facts required for the next topology decision or dispatch. Check only:

- that the delegation tool is enabled and its current schema is available;
- active controller and delegated model/provider routing as exposed by the supported runtime surface;
- installed maximum concurrency `C` and maximum spawn depth;
- the leaf role and allowed task fields;
- whether model-facing consolidated batch completion is part of the public contract; and
- whether the adaptive reasoning-effort and model-tier resolver supports the configured `auto` value(s) and the tier-to-route floor table.

Do not use capability discovery to enumerate secrets, inspect private child transcripts, read unrelated accounts, or probe unsupported internal endpoints. Do not treat a child process's existence, a cache file, or a log line as proof of public capability.

If discovery cannot establish a required fact, choose the safe fallback: Direct when it satisfies the objective without delegation, otherwise `BLOCKED` with the missing capability, attempted supported check, and impact. Do not guess capacity, route, event semantics, or spawn depth.

## 7. Adaptive `auto` verification guard

`delegation.reasoning_effort: auto` and the paired `delegation.model_tier: auto` are desired policy values. Each is valid only when the installed resolver accepts it and converts a unit of work's tier — Exempt/Standard/Broad/High-risk, classified once in `SKILL.md`'s Two-axis classification and mapped through its tier-to-route floor table — into a concrete supported effort or model tier before the request is sent, for both a dispatched leaf and the Chairman's own current action. `reasoning_effort: auto` selects reasoning effort only; `model_tier: auto` selects the model tier (Luna or Sol) only. Neither key selects provider or endpoint, which remains installation-owned; and neither key is a second classification system — both resolve strictly from the one tier/topology decision already required elsewhere in this skill.

Before relying on adaptive behavior:

1. verify the configured `auto` value(s) are accepted by the installed resolver;
2. verify the resolver classifies a representative bounded leaf, and a representative Chairman action, into a concrete supported effort and model tier that meet or exceed that tier's floor — never below it;
3. verify the resulting request uses the resolved model/provider and the resolved effort, not merely the installation's static default; and
4. record the real probe or public per-child/per-controller routing evidence in the runtime ledger.

Configuration readback alone does not prove resolution. If `auto` is rejected, passed through to a fixed-level parser, or silently inherits a fixed parent level or tier regardless of classification, record adaptive routing as unavailable. Preserve the conservative inherited safety floor — the highest floor known to apply, never a discounted one — do not make performance/latency/cost claims, and block acceptance claims that depend on adaptive selection until the resolver is repaired and covered by focused and live delegation tests. If the required adaptive capability is unavailable, use Direct when safe; otherwise report `BLOCKED` rather than dispatching on an unsupported assumption.

Ordinary context length does not by itself raise a task's risk floor. Explicit task risk, security/concurrency/data-integrity triggers, and Assured rules may raise controls; `auto` may only move a resolved route upward relative to its tier's floor and must never be used to lower it — not for a leaf, and not for the Chairman's own action. High-risk work, Assured-controls work, and verification of High-risk or Assured work always resolve to the top floor (Sol at `max`) regardless of what `auto` would otherwise select for efficiency; this exception is non-negotiable and is not itself subject to adaptive selection.

## 8. Public contract boundary for event claims

Do not claim an event-driven scheduler, event-driven orchestration, or event-triggered execution unless the public Hermes runtime contract explicitly documents the event, delivery, identity, ordering, retry, and failure semantics required by the claim.

The selected Parallel workflow may use a model-facing consolidated batch-completion message only when preflight verifies that public contract. That is a completion handoff, not permission to invent a general event-driven scheduler. Internal filesystem watchers, live transcript files, cache entries, polling loops, or daemon behavior are implementation details and cannot establish the public contract.

If a future public event contract is added, verify its version, subscription/dispatch authority, event identity, delivery semantics, duplicate handling, and failure behavior before updating this reference or making the claim. Until then, describe execution as explicit controller dispatch followed by model-facing batch completion and controller verification.

## 9. Kanban capability contract

Kanban is a separate durable Parallel transport, not delegated batch completion. Before using it, verify the active top-level Sol profile exposes orchestrator Kanban tools; delegated child contexts may be prohibited from mutating boards and must never bypass that guard. Verify the exact named board, profile catalog, gateway-embedded singleton dispatcher, profile route, pinned skills, workspace, dependency/idempotency fields, and supported worker lifecycle tools.

Do not infer Kanban availability from the CLI help text or a database file alone. A board may exist while the top-level model lacks the toolset, the gateway dispatcher is stopped, the assignee profile is missing, or the current process is a protected child context. Use the supported tool/status surfaces and record real readbacks.

Kanban workers are named profiles and are not automatically Terra. Record the actual profile model/provider/reasoning/toolsets and call it a Terra worker only when verified. Per-task route overrides are capability-contingent and plan-owned; they never authorize global profile edits.

The board's durable states and events are transport evidence. They do not replace the plan's acceptance or completion state. See `kanban-transport.md` for mapping, recovery, and retention.

## 10. Complexity-gated takeover guard

The Chairman's own resolved model tier and reasoning effort auto-scale with the tier of whatever it is currently doing for orchestration decisions — planning a trivial Exempt change does not route the same as verifying a High-risk one — subject always to the non-negotiable floor in `SKILL.md`: High-risk work, Assured-controls work, and verification of High-risk or Assured work resolve to Sol at `max` regardless of what efficiency-first routing would otherwise select.

Before taking work back from a Luna worker, assess and record: coupling and dependency depth, ambiguity or conflicting evidence, reversibility and blast radius, security/concurrency/data-integrity exposure, required verification/consultation tier, and whether decomposition remains ownership-safe. Complexity changes topology, assurance, and the resolved model/effort floor together — all three derive from the same tier decision, never from independent judgment calls.

Luna workers resolve to the floor recorded for their assigned tier by default and may not promote themselves or smuggle model overrides into `delegate_task`. A takeover brief must name the triggering complexity factors, exact resource boundary, required evidence, the resolved model/effort floor Sol resumes at, and the return-to-Chairman handoff.

**Full Sol takeover** is an explicit Chairman decision: Sol retains or resumes controller ownership in `Direct` topology and performs the tightly coupled or high-risk operation itself at the floor required by that operation's tier — `max` whenever the operation is High-risk or Assured. It is not an untracked model fallback, a worker self-promotion, or permission to bypass review, verification, or external consultation gates.

Before relying on a stored setting, verify `agent.reasoning_effort`, `agent.model_tier` (or the installation's equivalent), the active model's override, and `delegation.reasoning_effort`/`delegation.model_tier` through the supported configuration surface. A per-session slash command, per-job pin, model-specific override, named-profile config, or provider capability clamp can change the effective level, so inspect applicable precedence when exact reasoning or model tier matters. Configuration readback proves the requested policy is stored; a live model-call trace is required to prove the provider received a particular wire value and model.

## 11. Autonomous execution layer

Sol/Chairman may use an autonomous runtime layer for bounded execution without surrendering authority. This layer improves throughput and continuity; it does not make acceptance decisions, lower assurance, or authorize scope expansion.

The runtime layer may provide these seven capabilities:

1. **Harness and adapter abstraction** — resolve a validated role to an approved harness/provider without changing the controller's policy or silently changing global configuration.
2. **Detached supervision** — launch bounded workers with process-group supervision, timeout, cancellation, cleanup, and liveness handling. A detached worker must have one active transport owner and a recorded native run identity.
3. **Durable run state** — persist queued/running/done/failed/cancelled/incomplete state, transition history, attempts, timestamps, and report-claim leases in a controller-owned state store. Runtime `done` maps to `handoff_pending`, never directly to `verified`.
4. **Role and harness resolution** — select from the live, allowlisted role/harness catalog using explicit task metadata. Unknown, malformed, path-like, or unauthorized roles/harnesses fail closed before launch.
5. **Background artifact and session reporting** — keep full worker output in bounded artifacts or harness-owned sessions and return concise reports to Sol. Reports must identify the work/attempt/run, result status, evidence, changed resources, risks, and open decisions; do not copy private transcripts or secrets.
6. **Runtime testing and fake-worker coverage** — exercise dispatch, supervision, cancellation, timeout, state transitions, report delivery, adapter behavior, and end-to-end failure paths with deterministic fake workers before relying on autonomous behavior.
7. **Budgets and incomplete-result recovery** — enforce per-run iteration, wall-clock, output, and concurrency budgets. Empty, truncated, malformed, or budget-exceeded results become `incomplete` or `failed`; recover with a bounded continuation or a new fenced attempt, never by treating partial output as success.

### Autonomous control loop

After Sol/Chairman has classified the work and sealed the bounded brief, the runtime may autonomously execute only the next ready assignment, supervise it, collect its report, and prepare a handoff. It may retry a transport failure only when the prior owner is terminally fenced, possible effects are read back, the retry budget remains, and the new attempt is recorded. It may continue independent ready work in the same sealed wave, but it may not invent tasks, change dependencies, alter ownership, approve a result, satisfy consultation coverage, or release a downstream task whose prerequisite is only `done`.

Autonomous actions are limited to the declared scope:

- permitted: launch, supervise, collect, summarize, persist state, notify Sol, and perform bounded continuation recovery;
- prohibited: scope expansion, unsanctioned writes, global configuration changes, credential access, self-approval, hidden transport handoff, and automatic promotion to `verified`;
- escalation to Chairman required: material ambiguity, ownership collision, unavailable authoritative input, repeated non-decreasing failure, incomplete required evidence, destructive or external action outside the declared authorization, or exhausted budget. The Chairman recovers/re-plans internally where safe; only a real unresolved decision, authority, or dependency requires the user.

Every autonomous run must retain: stable `work_id`, unique `attempt_id`, selected role/harness, transport/native run ID, approved resource boundary, budget, state transitions, report/artifact handles, cleanup result, and Chairman verification outcome. If the runtime cannot persist or read back these fields, use Direct or mark the autonomous lane `BLOCKED`.

### Repository-review autonomous workflow

For repository review, use the local **Sol Review** clone as the functional design reference when available: `<active-workspace>/sol-review/README.md` and `DESIGN.md`. Treat those documents as project-local evidence, not universal policy, and re-inspect them if the clone changes. The review runtime should progress through bounded stages:

1. **Inspect:** collect repository metadata, base revision, unified diff, changed paths, and working-tree fingerprint without modifying the target repository.
2. **Deterministic pass:** parse the unified diff, review added lines, run deterministic analyzers, and ingest SARIF or equivalent structured findings when present. Security rules take precedence over probabilistic suggestions.
3. **Context pass:** retrieve only the repository context required to interpret findings; Tree-sitter/indexing work is a separate bounded stage and must not silently become a full-repository write operation.
4. **Evidence-gated model pass:** an LLM reviewer may rank or explain findings only when source spans, file/line anchors, rule output, and confidence are available. It must not invent findings unsupported by the inspected revision.
5. **Report:** emit structured findings with severity, file, line, rule/category, evidence, confidence, and disposition. HTML output must escape repository and finding values and must not embed credentials, source contents, or uncontrolled HTML.
6. **Verification:** run the CLI/CI acceptance checks, verify report readability and print behavior where applicable, and have Sol independently inspect high-severity findings and the final artifact.

The runtime may autonomously continue from one stage to the next only when the preceding stage has a successful, persisted handoff and the revision fingerprint is unchanged. A material repository change, missing source anchor, parser failure, analyzer disagreement, or confidence/evidence failure returns the workflow to `blocked` or a new fenced attempt. GitHub webhook ingestion, repository indexing, analyzer/SARIF ingestion, and LLM review are planned extensions—not capabilities to assume merely because the design documents name them.

## Verification checklist

- [ ] Observed routes were read from supported surfaces, untraced values marked unknown, and explicit route pins plus required capabilities verified; no preferred model label became a routine selection prompt.
- [ ] No per-task model, provider, reasoning, timeout, capacity, or toolset override was passed through the task card or delegation call.
- [ ] Every child received a fresh self-contained brief with authoritative context, exact ownership, acceptance, verification, cleanup, and output contract.
- [ ] Every delegated task used the leaf role and no child created grandchildren, teams, Hermes processes, or global configuration changes.
- [ ] The batch size was at most installed capacity `C` and capacity was treated as a ceiling, not a quota.
- [ ] Dispatch was recorded as pending; no success was claimed before the genuine model-facing consolidated completion message.
- [ ] Results were evaluated only from the public completion contract; private logs, caches, and live transcripts were not used as a substitute.
- [ ] Narrow capability discovery established delegation schema, routing, capacity, spawn depth, completion contract, and required adaptive support.
- [ ] If adaptive `reasoning_effort: auto` or `model_tier: auto` was required or claimed, concrete resolution to a tier-floor-conformant effort and model was verified; otherwise leave adaptive claims unproven and continue safely without making optional telemetry a task dependency.
- [ ] No resolved model tier or reasoning effort fell below its tier's floor, and any High-risk/Assured work or verification of it resolved to Sol at `max` regardless of efficiency-first defaults.
- [ ] Missing runtime capabilities caused a safe Direct fallback or an explicit `BLOCKED` result rather than a guessed workaround.
- [ ] No event-driven scheduler claim was made without a documented public contract.
- [ ] If Kanban was selected, the top-level toolset, named board, singleton dispatcher, profile/route, workspace, idempotency/dependencies, and lifecycle tools were verified without bypassing child-context guards.
- [ ] Kanban workers were identified by their actual profile route and board states were treated only as transport evidence.
- [ ] Controller independently verified every child result and recorded final integration, repair, cleanup, and external-state evidence.
