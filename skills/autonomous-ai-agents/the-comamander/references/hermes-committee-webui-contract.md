# Hermes Committee WebUI Contract v1.1.0

This document defines the required contract for an implementation that claims to expose the bounded Agent Committee through an authenticated Hermes WebUI and equivalent CLI surface. It is a contract for conformance, not evidence that every Hermes installation exposes these routes or CLI behavior. An active installation may use this contract only after it identifies an authoritative supported contract and passes the applicable conformance checks; otherwise committee delivery is unavailable.

## 1. Scope and boundaries

The committee API is a thin, authenticated control surface over existing Hermes profiles and the canonical Bot Chat. It may persist a bounded roster, open the canonical chat, and dispatch a bounded brief. It must not become:

- a second transcript or message store;
- an automatic model, profile, or execution-topology router;
- a replacement for Sol–Terra delegation or Terra execution;
- a replacement for mandatory Codex/Claude consultation coverage or any other assurance-tier gate;
- a voting, quorum, majority, or consensus authority; or
- a mechanism for creating grandchildren, expanding scope, or granting review writes implicitly.

`default` is the Chairman. The Chairman owns scope, dependency ordering, Direct|Parallel topology selection, conflict resolution, approvals, integration, independent verification, and the final decision. The API must preserve that authority in both roster and message behavior.

Committee evidence can inform a material decision, but it never selects Direct|Parallel automatically and never lowers the assurance tier. A successful API response is not completion evidence until the canonical session/message state is independently verified.

The committee, Sol–Terra delegation, and external CLI consultation are separate boundaries: committee chat is advisory communication, Terra leaves execute atomic work, and external CLI review supplies an independent assurance lane. A committee response must not be presented as Terra completion or as required external CLI coverage.

### 1.1 Execution topology versus committee-message ordering

Execution topology and committee communication ordering are independent Chairman decisions:

- **Direct** remains controller-owned execution. The Chairman performs the execution itself, and Direct has no Terra requirement. Committee advice may be requested under Direct, but a committee brief or response is advisory communication and never performs the execution.
- **Parallel** uses Terra leaves for independent, non-overlapping atomic execution in bounded waves.
- Committee briefs may be sent sequentially or concurrently based on advice dependencies and the bounded response-round budget. That communication ordering never selects, changes, or implies Direct or Parallel, and committee advice never executes a Terra leaf.

An implementation claiming support must preserve this separation in its route, session, and message behavior. The contract does not authorize an API to choose topology, dispatch execution, replace Terra leaves, or change the Chairman's plan.

## 2. Canonical surfaces (capability-contingent)

The following routes are required only for an implementation claiming support for the authenticated committee WebUI. Their presence is not implied by this reference. An active installation may use them only when its authoritative supported contract identifies these routes and the implementation passes the verification matrix below; otherwise it must record committee delivery unavailable.

An implementation claiming support exposes these authenticated routes under the canonical API prefix:

| Method and route | Purpose | Required canonical behavior |
|---|---|---|
| `GET /api/committee` | Read the current roster and Chairman metadata | Return the installation-owned roster resolved from the live profile catalog; always identify `default` as Chairman. |
| `POST /api/committee` | Create or update the bounded roster | Require authenticated state-changing access, validate every member, preserve `default`, reject duplicates and unsupported roles, and persist through the installation-owned roster mechanism. |
| `GET /api/committee/chat?profile=<name>` | Open or retrieve a canonical Bot Chat for a validated profile | Resolve the exact live profile, use the canonical `Bot Chat` title/session renderer, and do not create a duplicate transcript backend. |
| `POST /api/committee/chat` | Explicitly create/open a canonical Bot Chat | Validate the profile before any process/session operation, use the same canonical title and bounded timeout as the CLI, and return only safe session metadata. |
| `POST /api/committee/message` | Dispatch a bounded Chairman brief to a validated target | Validate sender, target, and message before invoking a Bot process; use argument-safe canonical CLI semantics; return a bounded receipt only after delivery can be verified. |

A deployment may add versioning or a host-specific prefix, but it must preserve the route semantics, authentication, validation order, and canonical Bot Chat mapping above. It must not expose an unauthenticated alias that bypasses these requirements.

For an implementation claiming support, the equivalent CLI surface is:

```bash
hermes -p <profile> chat --in ~ -c "Bot Chat" --create-if-missing -Q -q "Message from 🤖 <sender>: <bounded brief>"
```

An active installation must not assume this command is available merely because it appears in this reference. Use it only after the authoritative supported contract identifies the CLI capability and the applicable conformance checks pass; otherwise record committee delivery unavailable.

A conforming WebUI implementation may invoke this behavior through an internal service rather than a shell, but the effective profile, canonical chat title, bounded message, timeout, and sanitized error behavior must be equivalent. Implementations must pass arguments without shell interpolation and must never put credentials or raw subprocess output in the response.

Where the capability is supported, the roster is installation-owned (for example, an installation's `committee.json`), not frontend-only state. Both WebUI and CLI profile resolution must use the live Hermes profile catalog. Frontend display fallbacks may show cached names, but cached names are not authorization or dispatch input.

## 3. Authentication, authorization, and request validation

### 3.1 Authentication and request integrity

1. Every committee route, including read-only `GET` routes, requires the installation's normal authenticated user/session context.
2. Every state-changing `POST` requires the normal CSRF protection and same-origin or explicitly approved-origin check. Do not add a committee-specific bypass.
3. Authentication and origin/CSRF validation happen before roster lookup, profile lookup, subprocess creation, or transcript access.
4. An unauthenticated request returns `401` without invoking a Bot process or revealing roster/profile details.
5. An authenticated request that fails CSRF/origin or authorization returns `403` without mutating the roster or dispatching a message.
6. Errors exposed to the browser are generic and correlation-safe. Do not return credentials, environment values, command lines containing secrets, raw transcript dumps, or unsanitized stack traces.

### 3.2 Chairman and roster validation

The roster payload is installation-defined but must carry a Chairman and a bounded member list. A conforming logical shape is:

```json
{
  "chairman": "default",
  "members": [
    {"profile": "researchbot", "role": "authoritative research"},
    {"profile": "codebot", "role": "read-only code review"}
  ]
}
```

The server must:

- require the Chairman identifier to be exactly `default`;
- reject attempts to remove, rename, demote, or replace `default`;
- resolve each member by exact identity against the live profile catalog;
- reject unknown, empty, duplicate, malformed, path-like, or control-character profile identifiers before persistence or dispatch;
- reject duplicate member identities and unbounded member/role fields;
- keep one bounded role and evidence contract per member; and
- reject fields that attempt to create children, grandchildren, delegation trees, automatic routing rules, votes, or implicit write permissions.

The API must not trust a profile name supplied solely by a browser cache. The canonical catalog is the source of truth. Profile identifiers must not be silently rewritten to a nearby spelling or inferred from an unknown token; reject an invalid identifier and report a safe client error.

### 3.3 Chat profile validation

For `GET /api/committee/chat?profile=<name>` and `POST /api/committee/chat`, `profile` is required, non-empty, bounded, and an exact live-catalog match. The server rejects unknown or malformed values before opening a session or spawning a process. The canonical chat title is exactly `Bot Chat`; implementations must not create a per-request title or a parallel transcript store.

Opening a chat does not grant the selected profile authority over scope, roster, topology, assurance, or final approval. The Chairman remains `default` even when a specialist chat is displayed.

### 3.4 Message validation

A logical message request is:

```json
{
  "sender": "default",
  "target": "researchbot",
  "message": "Provide authoritative sources for the bounded decision described here.",
  "request_id": "optional-idempotency-token"
}
```

The server must:

1. require a non-empty `sender`, `target`, and `message`;
2. require `sender` to be the authorized Chairman identity `default` for committee control messages;
3. resolve `target` by exact live-catalog match and reject unknown or malformed targets before dispatch;
4. enforce a configured maximum message size in bytes and characters (a deployment should publish the bound; 16 KiB UTF-8 is a suitable default);
5. reject control-only or empty-after-validation messages, and reject invalid JSON/content types before dispatch;
6. preserve the message content as submitted after transport validation rather than guessing at identifiers or silently changing instructions;
7. attach the bounded brief context through the canonical Bot Chat mechanism, without exposing private transcript history; and
8. use a bounded timeout, safe argument passing, and sanitized failure handling.

The message contract is advisory. It cannot authorize a reviewer write, a new profile, a topology change, an assurance downgrade, a scope expansion, or a child/grandchild worker. Those require a separate Chairman-controlled workflow.

A valid response should contain only safe metadata, for example:

```json
{
  "ok": true,
  "chat": "Bot Chat",
  "sender": "default",
  "target": "researchbot",
  "request_id": "optional-idempotency-token",
  "receipt_id": "installation-generated-id"
}
```

The implementation must not claim delivery solely because a subprocess was started. It must read the canonical session/message surface or an equivalent delivery receipt and confirm the exact target and request before reporting success.

## 4. CLI/WebUI parity and operational limits

WebUI dispatch and the canonical CLI must agree on:

- the live profile catalog and exact profile identifiers;
- Chairman identity (`default`);
- canonical chat title (`Bot Chat`);
- bounded message size and timeout;
- argument-safe invocation;
- sanitized errors; and
- end-to-end verification requirements.

Committee waves are bounded: one response round is preferred and no wave exceeds three serial response rounds. The API must not provide an unbounded streaming or recursive fan-out control that bypasses the Chairman. A specialist may consult a named peer only for an explicit dependency; the WebUI must not expose a generic spawn-grandchild operation.

The committee is optional. The API may be used only when it improves a material decision. It must not be required for ordinary linear work or used to manufacture execution work or communication concurrency. Committee brief ordering is independent of execution topology: Direct remains controller-owned with no Terra requirement, while Parallel uses Terra leaves; committee responses never select or alter either topology. Mandatory Codex/Claude consultation coverage and all other assurance-tier gates remain in force regardless of committee responses.

## 5. Response and error contract

Use the host API's normal JSON envelope and status conventions, with these semantic requirements:

| Condition | Required result | Side-effect requirement |
|---|---|---|
| Missing/invalid authentication | `401` | No roster detail, session open, or Bot process. |
| CSRF/origin/authorization failure | `403` | No roster mutation or dispatch. |
| Unknown or malformed profile/target | `404` or `422` | Reject before subprocess/session invocation. |
| Invalid roster, Chairman, role, or forbidden control field | `422` | No persistence or dispatch. |
| Empty, invalid, or oversized message | `422` or `413` | Reject before dispatch. |
| Valid roster update | `2xx` | Persist bounded roster, then read back the exact saved roster. |
| Valid chat open | `2xx` | Use the canonical Bot Chat/session renderer; return safe session metadata. |
| Valid message dispatch | `2xx` only after verified receipt | Confirm exact target/message receipt through the canonical surface. |
| Timeout or Bot failure | `502`, `504`, or host-equivalent safe error | Return sanitized error; do not expose command output or secrets. |

Error bodies should identify the class of client-correctable failure and, where useful, a correlation identifier. They must not disclose whether an unprivileged caller guessed a sensitive profile beyond the minimum behavior required by the host API.

## 6. Verification matrix

The following matrix is the acceptance gate for a conforming implementation. “No process” means no Bot subprocess, canonical chat open, or equivalent dispatch operation is attempted.

| ID | Scenario | Request precondition | Expected observable result | Verification evidence |
|---|---|---|---|---|
| V1 | Unauthenticated roster read | No valid authenticated session | `401`; no roster/profile leak; no process | HTTP response and process/audit counter show zero dispatches. |
| V2 | Unauthenticated chat/message | No valid authenticated session | `401`; no session open or message delivery | HTTP response plus no-process audit. |
| V3 | CSRF/origin failure | Authenticated session, invalid integrity token/origin | `403`; no mutation or dispatch | Response and unchanged roster/session state. |
| V4 | Unknown profile | Authenticated request with a profile absent from live catalog | `404`/`422`; no process | Catalog lookup rejection and no-process audit. |
| V5 | Malformed profile | Empty, path-like, duplicate, or control-character profile | `422`; no process | Validation result and no-process audit. |
| V6 | Chairman preservation | Roster attempts to replace/remove/rename `default` | `422`/`409`; roster unchanged | Read back roster and confirm `default` remains Chairman. |
| V7 | Invalid roster member | Unknown member, duplicate identity, unbounded role, or forbidden control field | `422`; no persistence | Read back exact prior roster. |
| V8 | Empty message | Missing, empty, or control-only message | `422`; no dispatch | Response and no-process audit. |
| V9 | Oversized message | Message exceeds published bound | `413`/`422`; no dispatch | Boundary-size tests and no-process audit. |
| V10 | Non-Chairman sender | Authenticated message with `sender` other than `default` | `403`/`422`; no dispatch | Response and unchanged canonical chat. |
| V11 | Valid roster update | Authenticated, integrity-checked, catalog-valid bounded roster | `2xx`; exact roster persisted | Read-after-write equality against the submitted canonical roster. |
| V12 | Valid chat open | Authenticated exact profile | `2xx`; canonical title `Bot Chat`; existing renderer/session | Session metadata and canonical chat title read back. |
| V13 | Valid bounded message | Authenticated Chairman, valid target, bounded content | `2xx` only after verified delivery | Canonical session/receipt contains exact target and request/receipt identifier. |
| V14 | Bot timeout/failure | Valid request, bounded operation exceeds timeout or exits nonzero | Safe `502`/`504`; no raw output | Sanitized body, bounded completion, and secret-redaction check. |
| V15 | Direct|Parallel and assurance preservation | Committee evidence recommends a topology, changes communication ordering, or appears to lower a gate | No automatic re-route or assurance downgrade; Direct remains controller-owned with no Terra requirement, while Parallel uses Terra leaves | Plan shows Chairman-selected topology separately from sequential/concurrent committee ordering, plus mandatory Codex/Claude coverage. |
| V16 | Round/grandchild bounds | Request attempts recursive fan-out or a fourth serial round | Rejected or stopped by Chairman-controlled boundary | Audit shows at most three serial rounds in the wave and no child/grandchild. |
| V17 | Read-only reviewer default | Review brief without explicit repair authorization | No resource mutation | Changed-resource audit is empty; reviewer reports `changed-resources: none`. |
| V18 | Memory restriction | Committee reply without explicit memory assignment | No durable memory write | Memory audit shows no write; explicit assignment test is separately bounded. |
| V19 | Research provenance | Research response contains external claims | Source URLs plus fact/inference/uncertainty distinction | Chairman can independently retrieve or inspect each authoritative citation. |
| V20 | Chairman verification | Specialist returns material PASS or disagreement | Chairman rechecks evidence before acceptance | Verification record names the checked resource/result and final decision. |
| V21 | Mandatory external-CLI non-substitution | Project tier requires Codex and/or Claude review and committee returns any status, recommendation, or apparent consensus | Completion remains blocked until each required external CLI consultation is independently performed, recorded, and verified; a committee response never satisfies the gate | Ledger record names the required CLI, task, status, and artifact fingerprint where applicable; review output and final artifact are independently matched. |

A passing roster UI or a `2xx` response without the readback and audit evidence above is insufficient. The implementation and Chairman must preserve evidence, dissent, unavailable members, risks, open decisions, and changed resources for the final decision without exposing private or secret data to unauthorized callers.

## 7. Implementation notes

- Prefer the existing authenticated session middleware, profile catalog, Bot Chat/session renderer, CSRF/origin middleware, timeout utilities, and error envelope rather than committee-specific substitutes.
- Keep route handlers thin: validate first, call the canonical service, sanitize the boundary response, and verify state before claiming success.
- Use idempotency or request correlation where the host supports it to prevent duplicate briefs after client retries; never use retries to bypass a failed validation or round limit.
- Keep roster and message schemas bounded and versionable. Unknown control fields should be rejected when they could affect authority, routing, scope, writes, or fan-out.
- Treat committee responses as advisory evidence. The Chairman independently verifies material findings and decides whether to continue, repair, re-plan, or stop.
