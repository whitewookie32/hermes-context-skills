---
name: sol-terra-parallel-orchestration
description: "Proportional Sol–Terra orchestration with safety gates."
version: 2.8.0
author: Donna, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [orchestration, delegation, kanban, parallel, direct, assured, planning]
    related_skills: [subagent-driven-development, plan, kanban-orchestrator, kanban-worker, kanban-codex-lane, codex, claude-code]
---

# Sol–Terra Proportional Orchestration

This is the compact, always-loaded core policy. It contains the complete set of non-negotiable rules; every mode reference under "Mandatory classification-to-reference loading gate" below adds procedural detail but never relaxes what is stated here. If a linked reference is missing, stale, or inconsistent, follow this file, record the deviation, and do not infer unsupported runtime capabilities.

## Runtime routing boundary

Sol remains the accountable Chairman for orchestration, integration, and verification. The skill does not select providers, models, or reasoning effort: those remain owned by supported Hermes runtime configuration and routing programs. Policy prose is not runtime proof. Before relying on a route, inspect the active profile's model/provider configuration, `smart_model_routing`, reasoning settings and overrides, delegation settings, and the observed fresh-agent or fresh-child route. Explicit supported pins remain authoritative unless a non-waivable safety or capability conflict requires the Chairman to stop and resolve it.

Automatic routing may run only at a supported fresh session, fresh agent, or fresh delegated-child boundary; cached and resumed conversations preserve their concrete route. Workers do not promote themselves or introduce model/provider/reasoning overrides. No skill may replace, duplicate, move, or silently override programmatic routing or configuration.

## Non-negotiable invariants

These rules apply in every topology, tier, and assurance profile:

- Sol/Chairman owns scope interpretation, classification, planning, routing, dispatch, integration, verification, consultation evidence, and the final completion decision.
- Delegated workers are leaves: no grandchildren, further delegation, or recruited agents. They receive self-contained briefs and execute only their assigned atomic outcome.
- Before dispatch, every atomic unit receives a stable secret-free `work_id`; every live owner receives a distinct `attempt_id`. `work_id` survives retries and transport changes, while a material objective, scope, ownership, acceptance, or side-effect change creates a new linked work item. Record native IDs beneath the attempt: delegation/child IDs or Kanban board/card/run IDs.
- Every logical task attempt has exactly one active execution transport owner. Never run the same attempt through `delegate_task` and Kanban simultaneously, and never treat a transport retry or handoff as authorized until the prior owner is terminally fenced, possible effects are read back, and the successor attempt is recorded.
- Capacity is a ceiling, never a quota. Never invent, split, or dispatch work only to fill available slots.
- No two active workers may own the same mutable file, record, branch, account, device, environment, or process. Use disjoint paths or isolated workspaces when parallel work is justified. Record these ownership boundaries in each brief.
- Never silently change global model configuration, provider routing, tool policy, spawn depth, credentials, or unrelated service state. Install-level configuration owns child routing.
- A worker summary, external CLI opinion, configuration readback, or successful API response is evidence to inspect, not proof by itself. Read back material external effects from the authoritative source.
- Preserve exact identifiers and user-provided values. Do not expose secrets or place credentials, tokens, `.env` contents, or auth stores in briefs, plans, ledgers, or consultation prompts.
- Stop or escalate when scope, ownership, safety, authority, or required evidence is unclear. Do not trade away a safety gate for speed.
- For High-risk or Assured work, the safety requirement is an observed, runtime-authorized Sol route at literal `max`; if that route cannot be established without overriding a pin or changing global configuration, stop the affected lane and have the Chairman resolve the conflict. This skill does not select or mutate the route.

## Provider and runtime contract

The runtime program and active profile configuration own provider, model, fallback, and reasoning selection. The Chairman must record the requested policy and separately verify the observed route at the supported fresh execution boundary. An explicit supported pin is never silently substituted.

For High-risk or Assured work, verify the runtime actually established Sol at literal `max` before relying on that lane. If the runtime cannot establish that route safely, use a safe Direct alternative only when it satisfies the same control, or mark the lane `BLOCKED`; never compensate by changing a skill, passing invented child overrides, or editing global route configuration without the user's explicit authorization.

Delegated workers remain leaf-only. Automatic routing, when active, never expands iteration, timeout, concurrency, or spawn-depth budgets. Cached/resumed conversations preserve their existing route unless a supported fresh boundary constructs a new agent.

## Plan-to-completion contract

For an implementation or action request, interpret the task, retrieve prerequisites, create or update the bounded plan internally, execute, inspect, test, repair, and re-plan until the acceptance criteria are verified. Do not wait for routine plan approval or progress feedback. Explicit plan-only, draft, comparison, or research requests remain within that scope. Ordinary retrievable questions and low-stakes design choices are Chairman-owned; genuine missing material decisions and security, privacy, authentication/MFA, destructive, hardware, and external-publication authorization remain gates.

Establish finite repair and consultation budgets in the plan. Budget exhaustion escalates to Chairman reassessment first, not automatically to the user. Required tests and reviews cannot be waived by replanning.

## Two-axis classification

Classify risk and consultation tier before choosing a topology. If facts are missing, retrieve them with tools; if uncertainty affects safety or blast radius, choose the stricter tier. If scope expands, reclassify at the next plan revision and only move upward.

### Consultation tiers

Tier precedence is `High-risk > Broad > Standard > Exempt`. The tier is independent of `Direct` versus `Parallel`.

- **Exempt:** no source, test, build, runtime configuration, data shape, public output, or behavior changes; or a mechanical documentation/formatting change whose acceptance check proves semantic identity. No consultation is required. Any uncertain or behavior-affecting code/configuration change is at least `Standard`.
- **Standard:** a bounded behavior-affecting code or configuration change in one component with limited blast radius and no broader or high-risk trigger. External CLI consultation is optional by default; use one useful reviewer selected by the deterministic Codex/Claude preference when available. It becomes required only when the user or task acceptance contract explicitly requires that review.
- **Broad:** a multi-component, public-contract, multi-leaf, or materially cross-cutting change without a high-risk trigger. Codex and Claude perspectives are optional by default; use them when available and materially useful. Require one successful Codex consultation and one successful Claude consultation only when the user or task acceptance contract explicitly requires both.
- **High-risk:** any authentication, security, concurrency, migration, data-integrity, production-control, irreversible-operation, or broad-blast-radius work. Codex and Claude review is optional by default, the same as Standard/Broad: use available perspectives when materially useful, selected by the deterministic preference. It becomes a required completion gate only when the user or task acceptance contract explicitly names it. High-risk automatically enables `Assured` controls and full independent Chairman verification regardless of whether external review was used.

Risk classification and deterministic verification remain mandatory. Standard/Broad/High-risk consultation assignments all use `Mode: optional` by default; a controller-authored plan must not manufacture a new login dependency. Only an explicitly required named review, at any tier including High-risk, is a non-waivable-by-Sol completion gate. Never retroactively count optional evidence as required coverage. Never reclassify a required review merely because it is unavailable. Record fallback, missing coverage, and any permitted user-only waiver explicitly. See `references/consultation-coverage.md` for the full tier detail, fingerprint binding, ledger, and fallback/waiver rules.

### Execution topology

Choose `Direct` when the work is linear, tightly coupled, read-only, mechanical, or too small for delegation overhead to be repaid; Sol performs the work without Terra delegation. Choose `Parallel` only when independent, isolatable, independently verifiable leaves exist and the break-even invariant in `references/parallel-mode.md` §1 is positive. Neither topology weakens a consultation tier, changes verification depth, or skips Assured controls when the tier or user request requires them. See `references/direct-mode.md` and `references/parallel-mode.md` for full classification and workflow detail.

### Parallel execution transport

After choosing Parallel, select the execution transport independently for each logical task — `delegate_task` for bounded same-session work that must return to Sol's context, or Kanban for durable, restart-surviving, human-interactive, multi-run, or audit-trailed work. One logical task attempt must never have two live transports. Direct creates no Kanban execution cards. See `references/kanban-transport.md` for card creation, state mapping, recovery, workspace, review, retention, and verification rules.

### Work identity, lifecycle, and steering

Every dispatched leaf uses `work_id: w:<plan-id>:<task-id>` and `attempt_id: <work-id>@a<N>`, recorded with its selected transport and native identity. Use the portable lifecycle `planned -> ready -> dispatched -> running -> handoff_pending -> verified` (plus `blocked`, `failed`, `cancel_requested`, `cancelled`, `unknown`, `superseded`); only Sol's independent verification may enter `verified`. See `references/work-item-lifecycle.md` for the full transition, checkpoint, and steering contract, and `templates/work-item-record.md` for the per-leaf record.

### Assurance overlay

`Assured` adds upward-only controls — full traceability, an authoritative ledger, immutable artifact fingerprints, required consultation evidence, material-output verification, rollback/cleanup planning, and history-preserving revisions — over either topology. Enable it for High-risk work, an explicit user request for full orchestration, or Sol's own judgment that impact, reversibility, external mutation, or uncertainty warrants it. Once external mutation or an irreversible step begins, never silently downgrade assurance or consultation requirements. See `references/assured-controls.md`.

## Trace and plan floors

Every mode has an evidence floor proportional to its ceremony. For Direct behavior-changing work, write a compact trace before acting (`templates/compact-direct-trace.md`; full detail in `references/direct-mode.md` §2 Step 3). For any multi-wave or multi-turn Parallel project, persist a compact plan under the active workspace (`templates/parallel-plan.md`; full detail in `references/parallel-mode.md` §2). A delegated leaf is cost-coherent, not defined by a fixed wall-clock duration — see `references/parallel-mode.md` §1 for the break-even invariant that governs atomicity.

## Direct workflow

Inspect and classify, set the trace floor, prepare safely, execute one coherent operation within its declared boundary, verify by risk, then complete or escalate. Direct does not delegate a "review child" merely to imitate Parallel; required Codex/Claude consultations remain external, bounded, read-only reviews governed by the project tier. See `references/direct-mode.md` for the full six-step workflow and verification checklist.

## Parallel execution workflow

Sol builds a requirement-to-task trace, decomposes only to cost-coherent and ownership-safe leaves, builds the ready queue from verified prerequisites and disjoint ownership, and sends complete self-contained leaf briefs — Terra children do not inherit the parent transcript. See `references/parallel-mode.md` §§1–3 for the full decomposition procedure and the canonical leaf brief template.

### Dispatch through the selected transport

For a `delegate_task` wave, use one model-facing `delegate_task(tasks=[...])` call containing all ready, independent leaves; do not pass child model, provider, reasoning, or toolset overrides. Before relying on batch completion, verify the supported Hermes contract documents the completion handoff — event-driven per-child scheduling is unsupported until a documented public contract exposes it; do not start a successor wave from one child finishing, do not poll or busy-wait, and treat `status: dispatched` as **pending, not complete**. Evaluate results only after the exact **completion signal** defined by the verified public/model-facing contract. See `references/runtime-contract.md` §5 and `references/parallel-mode.md` §5 for the full state machine, and `references/kanban-transport.md` for the Kanban dispatch path.

### Verify the consolidated result

**Sol independently reads every changed file or diff**, checks every worker against its acceptance criteria, runs relevant tests/builds/lints/type checks, validates integration assumptions, and reads back material external effects. **A child that reports PASS without evidence is unverified** — the same applies to a Kanban worker or card that reports PASS/done without evidence. Mark it failed or return it to a focused repair leaf/card. See `references/parallel-mode.md` §6 for the full verification and re-plan procedure.

## Risk-based verification

Verification depth follows impact, reversibility, coupling, and assurance — not merely topology or leaf count. Low-impact/read-only work needs only the narrow observable check; behavior-affecting, broad, High-risk, and Assured work need progressively deeper regression, integration, adversarial, rollback, and authoritative-readback evidence, never a self-attestation alone. See `references/direct-mode.md` and `references/parallel-mode.md` for the full checklists.

## External CLI consultation coverage

Consultation coverage applies regardless of Direct or Parallel topology. Sol classifies the project at the first planning revision and records the rationale. Required consultations are assigned to explicit atomic task IDs with `Mode: required`.

After `skill_view` resolves this skill's directory, invoke the metadata-only helper through `terminal` by its skill-relative path. Do not resolve the helper relative to the active workspace root. For example:

```text
python <skill-dir>/scripts/cli_consultation_ledger.py select --tier standard --project-id <id>
python <skill-dir>/scripts/cli_consultation_ledger.py record --project-id <id> --task-id <id> --cli codex|claude --purpose <value> --status success|unavailable|failed
python <skill-dir>/scripts/cli_consultation_ledger.py status [--project-id <id>]
```

**No required consultation starts until deterministic acceptance and regression checks pass.** Bind every required consultation to the exact **post-regression artifact fingerprint** — a SHA-256 digest of the final candidate tree, exact final diff, or immutable commit as appropriate. See `references/consultation-coverage.md` for classification detail, ledger fields, fallback/waiver rules, and the completion gate.

## Optional committee relation

A Chairman committee is optional advisory support for research, design, review, memory recall, or conflict resolution. It never replaces Sol–Terra delegation, changes routing, creates grandchildren, weakens tier coverage, or approves its own output. Sol/Chairman owns the brief, roster, ordering, scope, round budget, evidence standard, acceptance decision, and final answer. Committee evidence cannot satisfy an external CLI consultation gate.

## Repair, escalation, abort, and completion gates

- **Pre-flight gate:** required capabilities and explicit route pins, prerequisites, classification, trace/plan floor, atomicity, dependencies, ownership, capacity, leaf-only boundaries, and supported delegation semantics are established. Unknown optional routing telemetry is recorded, not guessed. Failure blocks only the affected action/lane; safely satisfiable Direct work may continue.
- **Repair gate:** use a finite repair budget with exact scope, new evidence, and preserved lineage, normally three attempts per tactic. On exhaustion or non-decreasing defects, stop that tactic and perform Chairman-owned root-cause reassessment. A materially different evidence-backed tactic may receive a new finite budget within unchanged authorized scope/cost/risk; stop repetitive non-improving retries. A material repair reruns deterministic checks and changes the fingerprint before required delta review.
- **Escalation gate:** resolve ordinary questions and exhausted tactics through tools and Chairman re-planning first. Ask only for a conflicting/non-retrievable material requirement, missing authority, unresolved unsafe ownership/risk, or unavailable required dependency after safe recovery is exhausted. Preserve required evidence and do not silently broaden scope.
- **Abort gate:** stop and preserve the trace/plan, verified artifacts, failed evidence, and cleanup state when safety boundaries are violated, destructive scope is unclear, authority is missing, required rollback is unavailable, or external state cannot be verified. State the concrete reason and safe recovery point.
- **Completion gate:** every requirement is traceable to verified work; the selected topology and tier were not bypassed; the final integration check passes; all required consultation evidence is successful or an explicitly documented permitted user waiver exists; every required fingerprint matches the accepted artifact; material external effects were read back; cleanup/teardown is complete; no unexplained active, ready, or blocked task remains; and no global configuration was silently changed.

For Assured work, also confirm the full ledger, immutable identity, review coverage, rollback/cleanup evidence, revision history, and final decision are internally consistent.

## Mandatory classification-to-reference loading gate

Before dispatching, selecting Kanban, claiming a route, applying Assured controls, or treating external review as coverage, load the corresponding reference with `skill_view`. This is a required step, not a suggestion — but the core invariants above remain fully binding even if a reference is unavailable or stale; record the deviation and proceed on this SKILL.md alone rather than inventing unsupported behavior.

| Condition established by classification | Required reference |
|---|---|
| `Direct` selected and work is behavior-changing | `references/direct-mode.md` |
| `Parallel` selected | `references/parallel-mode.md` |
| High-risk tier or `Assured` overlay active | `references/assured-controls.md` |
| External CLI review is selected, or explicitly required | `references/consultation-coverage.md` |
| Exact route/provider/effort resolution, delegation capability, or the autonomous execution layer matters | `references/runtime-contract.md` |
| Kanban transport selected | `references/kanban-transport.md` |
| A leaf is dispatched, retried, handed off, or steered | `references/work-item-lifecycle.md` |
| Enabling or testing Kanban integration | `references/kanban-activation-plan.md` |
| A machine-checkable conformance comparison against v2.2.1 is needed | `references/v2.2.1-safety-baseline.md` |

Templates: `templates/compact-direct-trace.md`, `templates/parallel-plan.md`, `templates/work-item-record.md`, `templates/assured-ledger.md`.

## Invocation and reporting

Project and integration requests may select this skill automatically, but skill selection is not proof of any provider, model, reasoning effort, or configuration contract. Verify the runtime contract before making those claims. An explicit request such as `Use iterative Sol–Terra orchestration for: <objective>` selects the policy but still cannot override safety, scope, or user-controlled global configuration.

At the end of work, report:

1. Status: `PASS`, `BLOCKED`, or `FAILED`.
2. The concrete result and acceptance verdict.
3. Real commands, tests, queries, or other evidence.
4. Exact files/resources changed and the trace/plan path.
5. Deviations, unresolved risks, consultation/fingerprint status, and any required user decision.

After an installation or skill change, an already-open session may need `/reset` to load the new body; do not claim activation until a fresh read verifies it.
