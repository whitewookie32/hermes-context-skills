---
name: the-comamander
description: "Use bounded specialist committees under a Commander."
version: 1.4.0
author: Donna, Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [bots, committee, orchestration, profiles, chairman, bot-chat]
    related_skills: [sol-terra-parallel-orchestration, hermes-agent, ponytail]
---

# The Comamander

## Runtime routing boundary

The Commander governs scope, evidence, safety, and verification; it is not a model router. Provider, model, and reasoning selection remain owned by the active Hermes runtime configuration and routing programs. Preserve explicit supported model/provider/reasoning pins and verify the observed route at a fresh agent or child boundary before claiming it. A skill must not replace, duplicate, move, or silently override routing code/configuration.

The primary profile is the **Chairman** under the Sol–Terra execution policy. The Chairman owns scope, classification, decomposition, dependency ordering, topology selection, conflict resolution, approvals, integration, independent verification, and the final decision. Specialists provide bounded evidence; they are not equal coordinators.

## When to use a committee

Create a committee only when named perspectives are likely to improve a material decision, such as:

- resolving a substantive architecture, correctness, security, or integration disagreement;
- gathering authoritative, source-grounded research that changes a decision;
- reconciling durable memory or prior decisions before acting;
- reviewing a verified candidate from independent specialist angles; or
- deciding whether a focused repair or a re-plan is warranted.

Do not create a committee for ordinary linear work, routine status collection, or to manufacture parallelism. If no material decision is unlocked, the Chairman should proceed without a committee. A committee may advise on a decision, but the Chairman remains responsible for making and verifying it.

## Authority and roster contract

`default` is always the Chairman and final coordinator. The roster is a bounded set of existing Hermes profiles, each with one named role, one evidence contract, and one accountable owner. The Chairman must validate membership against the live profile catalog before dispatch.

The standard specialist roles are:

- `memorybot`: retrieve and reconcile durable memory and session history. It may write memory only for an explicit memory-maintenance assignment or user request.
- `researchbot`: gather current, authoritative sources, citations, uncertainty, and open questions. It must distinguish sourced facts from inference and include source URLs for external research.
- `codebot`: review correctness, regressions, security, tests, and maintainability. It is read-only by default.
- `codexc`: provide repository-aware integration, optimization, and performance review. It is read-only by default and does not replace a required Codex consultation.
- `claude`: provide an independent architecture and correctness review through the bounded Claude CLI harness. It is read-only by default and does not replace a required Claude consultation.

Additional profiles require a bounded role and Chairman approval. A specialist may not redefine the roster, transfer ownership, expand scope, or approve its own work. No grandchildren or other child workers may be created. No committee voting, quorum, majority rule, or consensus-as-authority is permitted. Disagreement is evidence for the Chairman to reconcile, not a vote to resolve.

## Direct|Parallel execution topology and committee-message ordering

Execution topology and committee communication ordering are separate Chairman decisions. The Chairman selects **Direct** or **Parallel** in the Sol–Terra plan from dependency, ownership, and execution facts; the ordering of committee briefs never selects or changes that topology:

- **Direct** is controller-owned execution. The Chairman performs the execution itself, and Direct has no Terra requirement. The Chairman may request advisory committee briefs under Direct, but those briefs and replies are communication only and never perform the execution.
- **Parallel** uses Terra leaves for independent, non-overlapping atomic execution in bounded waves. The Chairman dispatches only leaves whose inputs, dependencies, and mutable ownership are isolated.
- Committee briefs may be sent sequentially or concurrently as a communication-ordering choice based on advice dependencies and the response-round budget. Sequential or concurrent briefs do not imply Direct or Parallel, and committee advice never executes a leaf.

Committee evidence can inform a topology decision or identify a dependency, but it never changes the plan by itself. The Chairman must re-plan explicitly after reviewing verified evidence. Under Parallel, keep atomic Terra leaves, their ownership boundaries, and their completion criteria in the plan; under Direct, the Chairman's own execution remains the execution path. In either topology, committee work is advisory communication and never performs or replaces execution.

The assurance tier is monotonic: committee evidence may add context, but it cannot lower the assurance required by the plan. Committee replies do not replace mandatory Codex/Claude consultation coverage, required tests, independent review, authoritative citations, or Chairman verification. A `codexc` or `claude` committee reply is not, by itself, proof that the corresponding mandatory external-CLI consultation occurred.

## Targeted brief contract

The Chairman sends a self-contained, targeted brief. Each brief has:

1. one accountable specialist and one bounded role;
2. one concrete question or decision to inform;
3. explicit in-scope work and non-goals;
4. allowed resources and read/write permissions;
5. the expected result format and acceptance criteria;
6. the evidence required, including citations or reproducible commands where applicable;
7. whether the work is advisory review or a separately authorized focused repair; and
8. a bounded response deadline or timeout.

Use separate briefs for independent perspectives. Do not broadcast identical prompts merely to create activity. A specialist may mention one named peer with `@name` only for an explicit, necessary dependency. That is a bounded peer consultation, not permission to spawn grandchildren or create a delegation tree. The Chairman may authorize a finite response-round budget in the initial brief. Evidence-driven rounds within it continue without user re-approval; record the material question for each round.

A brief must not contain credentials, unredacted private transcript dumps, or instructions to access unrelated resources. The specialist must reject or report a request that would cross the allowed scope rather than silently broadening it.

## Specialist response contract

Every specialist response must report all of the following fields, even when a field is empty:

```text
status: PASS | BLOCKED | FAILED
result: <concise answer to the assigned question>
evidence:
  - <reproducible observation, command/test result, or authoritative citation>
changed-resources:
  - <exact resource identifiers, or "none">
risks:
  - <known risks, uncertainty, or "none identified">
open-decisions:
  - <decision still owned by Chairman, or "none">
```

`PASS` means the bounded assignment produced usable evidence; it does not mean the overall project is approved. `BLOCKED` identifies a missing prerequisite or decision. `FAILED` identifies an execution or evidence failure. A member that has no material addition passes with that fact instead of repeating another response.

Evidence must be real and attributable. Research evidence includes authoritative source URLs and separates fact, inference, and uncertainty. Code evidence names the inspected resources and actual test or analysis results. A claimed change lists exact changed resources; a read-only reviewer reports `none`. Specialists must not claim completion from an unrun command, an unverified subprocess start, committee agreement, or a plausible reconstruction. If a specialist hits a timeout, truncation, schema-validation failure, or malformed handoff, classify that brief as `FAILED`/`BLOCKED` and do not use its partial summary as acceptance evidence; independently inspect the cited resources and rerun the smallest decisive check. When a delegated batch reports a top-level completion status but any leaf reports truncation, timeout, or iteration-cap exhaustion, the leaf status controls: record that leaf as incomplete and do not promote its self-reported `PASS` to committee evidence.

## Rounds, failures, and stopping

Prefer one response round per committee wave. A wave has a maximum of three serial response rounds; there is no automatic fourth round and no routine user-approval pause between budgeted rounds. A new wave is allowed only when the Chairman explicitly opens a new bounded decision with a fresh brief and records why another wave is material. A member that times out, is unavailable, is unauthenticated, or returns ungrounded evidence is recorded as `BLOCKED` or `FAILED`. Continue without that member when its evidence is optional. Block only when the acceptance criteria explicitly require that evidence; then surface the concrete decision to the Chairman or user.

The Chairman independently verifies every material finding before accepting it. For Broad, High-risk, or Assured implementation work, verify in this order: focused tests for the changed seam, a fresh-process smoke probe of the public behavior, the applicable regression slice, and only then long-lived service activation or deployment readback. For Exempt or Standard work, apply the proportional policy below and stop at the smallest decisive check when it proves the requested outcome. Repeat or inspect the relevant evidence, check citations, read back changed resources, and reconcile disagreements. Establish whether unrelated failures reproduce on the pre-change baseline before modifying them; do not “fix” an unrelated failure merely to make the committee report green. Committee consensus is never sufficient proof. The Chairman records accepted evidence, dissent, unavailable members, decisions, and any re-plan.

### Proportional verification and Ponytail mode

Verification is proportional to the task's assurance tier; it is not a ritual checklist that every small change must pay in full. For Exempt or mechanical work, use a direct tool or one deterministic check and stop when the requested outcome is proven. For Standard work, run the smallest decisive check for the changed seam; add a fresh-process smoke probe only when the change crosses a public runtime boundary, and add a regression slice only when an affected regression exists. Broad work retains the focused test, fresh-process smoke, and applicable regression sequence. High-risk or Assured work retains the full sequence plus required external review, state proofs, and readback. Security, data-integrity, compatibility, and explicit user acceptance gates are never removed by proportional verification.

For coding tasks, apply the local `ponytail` skill (or its narrower `ponytail-safe` subset) on demand: understand the affected path, question whether new code is necessary, reuse existing or native capabilities, make the smallest correct change, preserve safeguards, and run the proportionate decisive check. This is an instruction-only local adaptation; do not install upstream Ponytail plugins, hooks, MCP servers, or publishing scripts. Record the selected tier and why additional checks were unnecessary when stopping below the Broad sequence.

### Concurrent evidence freshness

A read-only specialist report is evidence about the resource snapshot it observed, not a standing claim about a concurrently changing worktree, service, or candidate. In every brief that touches mutable resources, record the revision/content fingerprint, exact in-scope resources, and whether concurrent mutation is expected. Before accepting a delayed finding about file presence, test state, configuration, or artifact identity, the Chairman must re-inspect the current resource and repeat the smallest relevant verification. Classify the report as **current**, **superseded**, or **structural-only**; only current, post-integration evidence can support a final implementation, candidate, deployment, or hardware-readiness claim. See `references/concurrent-evidence-freshness.md` for the dispatch and reconciliation ledger.

## Mutations, memory, and safety

- Specialists, especially code reviewers, are read-only by default.
- A write requires a separate, explicit, bounded assignment naming the owner, allowed resources, and verification gate. A review brief does not grant write permission.
- Memory writes require an explicit memory-maintenance assignment or user request. Do not turn a committee reply, transient opinion, credential, or private transcript into durable memory implicitly.
- No member may modify sibling-owned resources, change configuration, create profiles, or perform unrelated side effects without explicit authorization.
- Deep project hierarchies may use pre-authorized coordinator descendants, but every level requires an explicit depth cap, child budget, ownership subtree, timeout, and Chairman-visible evidence return. A coordinator descendant may not create an unlisted child, become a peer Chairman, approve its own work, or bypass the parent and Chairman gates.
- Do not expose credentials, private transcript dumps, subprocess output containing secrets, or raw stack traces in WebUI responses or specialist reports.
- Sanitize failures at the boundary while retaining actionable internal evidence for the authorized Chairman.

## Capability-contingent canonical communication surfaces

This skill-only package contains guidance, not a WebUI or CLI implementation. The route names and command below describe the canonical contract only when the active installation exposes committee delivery through an authoritative supported contract and the applicable conformance checks pass. They do not claim that every Hermes installation exposes these capabilities. Before use, verify the active installation's supported contract and its conformance evidence; otherwise record `committee delivery unavailable` and, when committee communication is optional, continue without it rather than guessing a route or command.

When the supported CLI capability has been verified, use the canonical Bot Chat rather than inventing a second transcript backend:

```bash
hermes -p <profile> chat --in ~ -c "Bot Chat" --create-if-missing -Q -q "Message from 🤖 <sender>: <bounded brief>"
```

When the supported WebUI capability has been verified, its installation-owned committee routes are:

```text
GET  /api/committee
POST /api/committee
GET  /api/committee/chat?profile=<name>
POST /api/committee/chat
POST /api/committee/message
```

For a supported implementation, all WebUI routes require the installation's normal authenticated session. State-changing requests additionally require the normal CSRF and origin checks. Profile names come from the live profile catalog; unknown, malformed, or path-like names are rejected before any Bot process is invoked. Messages must be non-empty and within the configured byte/character bound. The server must use argument-safe process invocation, bounded timeouts, and sanitized errors. See `references/hermes-committee-webui-contract.md` for the required contract for an implementation claiming support; the reference is not evidence that the active installation supports these routes.

For a supported implementation, WebUI and CLI must resolve to the same canonical Bot Chat title and session behavior. A roster editor, successful profile lookup, or successful subprocess start is not proof of end-to-end delivery. Verify the opened session or message receipt through the canonical renderer/session surface. If the supported contract or conformance check is unavailable or fails, record committee delivery unavailable instead of treating an unverified response as delivery.

## Sol–Terra integration checklist

At planning time, the Chairman decides whether committee communication is needed and states the material decision it supports. Keep the selected execution path in the Sol–Terra plan: Direct assigns execution to the Chairman/controller, while Parallel assigns independent leaves to Terra, never to an advisory committee response. Set execution topology independently from committee-message ordering: Direct remains controller-owned with no Terra requirement, while Parallel uses Terra leaves; committee briefs may be sequential or concurrent but cannot select or change that topology. Preserve all mandatory assurance-tier gates, including Codex/Claude coverage and independent verification.

After each verified wave, the Chairman should:

1. reconcile specialist responses and dissent;
2. independently verify material evidence;
3. update the decision and, if necessary, the Direct|Parallel plan;
4. request a narrowly scoped repair or new wave only when justified; and
5. record the final decision, risks, open decisions, and changed resources.

Committee output is input evidence. It is not Terra completion evidence, external-CLI consultation proof, a merge approval, or a final answer.

The committee, Sol–Terra delegation, and external CLI consultation are separate boundaries. Committee chat is advisory communication; Terra delegation executes atomic work; an external CLI review is an independent assurance lane. None may impersonate another, and committee evidence cannot satisfy a required external CLI gate unless that gate's own consultation was actually performed and verified.

## Verification checklist

- [ ] `default` is explicitly preserved as Chairman and final coordinator.
- [ ] The committee is used only for a material decision and has a stated purpose.
- [ ] Every brief has one bounded owner, scope, evidence contract, and permission set.
- [ ] Execution path matches the selected topology: Direct uses controller-owned execution with no Terra requirement; Parallel uses Terra leaves.
- [ ] Every mandatory Codex/Claude consultation remains present where required by the project tier.
- [ ] For every tier requiring external CLI review, the required Codex/Claude ledger record, artifact fingerprint where applicable, and independent review evidence are verified; no committee response, including a `codexc` or `claude` response, can satisfy that gate.
- [ ] One round is preferred and no wave exceeds three serial rounds.
- [ ] Every response contains status, result, evidence, changed-resources, risks, and open-decisions.
- [ ] No voting, grandchildren, silent scope expansion, or self-approval occurs.
- [ ] Reviewers are read-only unless a separate focused repair is authorized.
- [ ] Memory writes are explicitly authorized and bounded.
- [ ] External research includes authoritative citations and fact/inference separation.
- [ ] The Chairman independently verifies material findings and reads back material changes.
- [ ] Verification is proportional to the assurance tier: decisive check for Exempt/Standard, full sequence for Broad, and full sequence plus mandated assurance evidence for High-risk/Assured.
- [ ] `ponytail-safe` is used for coding minimalism without weakening security, compatibility, data-integrity, accessibility, or explicit acceptance gates.
- [ ] If committee delivery is supported, WebUI authentication, CSRF/origin, profile, target, and message validation are active; otherwise `committee delivery unavailable` is recorded.
- [ ] If committee delivery is supported, WebUI and CLI use the canonical Bot Chat and sanitized, bounded dispatch; otherwise `committee delivery unavailable` is recorded.

## References

- `references/hermes-committee-webui-contract.md` — required authenticated WebUI and CLI contract for implementations claiming committee-support capability, plus the verification matrix.
