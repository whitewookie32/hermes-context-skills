---
name: bot-communication-contracts
description: Define bounded communication between Hermes profiles.
version: 0.1.0
author: Nathaniel, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, bots, communication, orchestration]
    related_skills: [hermes-agent]
---

# Bot Communication Contracts Skill

Use this skill to make communication between Hermes profiles explicit, bounded, and reviewable. It defines message contracts and routing decisions; it does not create profiles, approve work, mutate configuration, or replace the Chairman.

## When to Use

- Preparing a brief for another Hermes profile.
- Reviewing bot-to-bot handoffs.
- Designing a profile communication graph.
- Converting repeated conversations into reusable message contracts.

Do not use for unbounded group chat, self-approval, credential transfer, or autonomous profile creation.

## Prerequisites

- The live Hermes profile catalog.
- A named Chairman/owner for the decision.
- A bounded objective, timeout, and evidence requirement.
- Current profile and Bot Chat contracts verified through the `hermes-agent` skill.

## How to Run

Use `terminal` for supported Hermes profile commands and `read_file` for existing contracts. Use `delegate_task` only when the Chairman has selected delegation and the brief has disjoint ownership. Use `write_file` or `patch` for the exact artifacts authorized by the user request and declared in the bounded brief; do not require a second routine approval. A plan or specialist cannot grant new authority.

## Message Contract

Every bot handoff must contain:

```text
message_id: <unique id>
sender: <profile>
recipient: <profile>
objective: <one decision or bounded question>
scope: <allowed resources and actions>
non_goals: <explicit exclusions>
context: <minimum necessary context; no raw transcript dump>
evidence_required: <tests, citations, hashes, or observations>
timeout: <bounded duration>
reply_format: status/result/evidence/changed-resources/risks/open-decisions
```

Responses must use:

```text
status: PASS | BLOCKED | FAILED
result: <concise answer>
evidence:
  - <reproducible observation or citation>
changed-resources:
  - <exact identifiers, or none>
risks:
  - <known risks, or none identified>
open-decisions:
  - <Chairman-owned decision, or none>
```

## Procedure

1. Name one sender, one recipient, and one accountable owner. Completion means ownership is unambiguous.
2. State one decision the message supports. Completion means the recipient can answer without inventing scope.
3. Remove secrets, unnecessary transcript content, and unrelated paths. Completion means the brief contains minimum necessary context.
4. Declare read/write permissions and non-goals. Completion means a review brief cannot be mistaken for write authorization.
5. Send through the verified canonical Hermes Bot Chat or delegation route. Completion means the route is supported by the current Hermes installation, not guessed.
6. Validate the structured response and independently verify material evidence. Completion means the Chairman accepts or rejects the evidence explicitly.
7. Record unresolved decisions and stale-plan conditions. Completion means no response silently changes the plan or approval state.

## Routing Rules

- `default` / Chairman owns scope, approvals, integration, and final decisions.
- `researchbot` supplies current external sources and uncertainty.
- `codexc` supplies repository and interface context.
- `codebot` supplies tests, regressions, and security review.
- `claude` supplies independent architecture challenge.
- `memorybot` reconciles durable context and prior decisions.
- `opsbot` supplies operational health, service, gateway, and rollback evidence.
- `r1` remains experimental until its role is confirmed.
- A proposed free-range profile may explore and summarize for the user, but may not approve, deploy, alter protected files, or speak as another profile.

Communication ordering does not select execution topology. The Chairman separately chooses Direct or Parallel, preserves disjoint ownership, and retains final verification.

## Safety Boundaries

- Never send credentials, tokens, API keys, private endpoints, raw auth files, or unredacted private transcripts.
- A message delivery receipt is not evidence that the requested work succeeded.
- A specialist response is not approval.
- No profile may approve its own work or create grandchildren.
- External side effects require a named plan hash and verified authorization for the exact action/target. A clear user instruction may supply existing authority for a bounded reversible record update; do not ask again solely because a plan was created. Destructive, public/outbound, credential, permission, identity, hardware, and otherwise consequential actions retain their separate applicable authorization gates.
- If the canonical route is unavailable, report `BLOCKED` rather than inventing a transport.

## Verification

- Every message has the required fields.
- Sender, recipient, owner, scope, and non-goals are explicit.
- The route is supported by current Hermes discovery.
- The response has all five evidence fields.
- Material claims are independently read back by the Chairman.
- No unauthorized resource changed.
- Stale fingerprints invalidate dependent approvals.
