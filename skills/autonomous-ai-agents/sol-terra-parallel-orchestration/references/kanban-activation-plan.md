# Kanban activation and rollback plan

This reference defines the narrow configuration cutover that makes Kanban orchestration available to the WebUI/API-server Sol controller after the v2.4 skill and required runtime guards are installed. It is a plan, not proof that activation already occurred.

## Scope

Managed configuration changes are exactly:

1. Add `kanban` to `platform_toolsets.api_server` while preserving every existing API-server toolset and every other platform's toolsets byte-for-semantic-value.
2. Set `kanban.auto_decompose: false` so gateway ticks cannot create plan cards outside Sol's authoritative graph.

Preserve all other `kanban` keys, including dispatcher interval, failure limits, review dispatch behavior, stale timeout, concurrency limits, notification settings, and board metadata.

Do not change:

- `platform_toolsets.cli` except to verify it already contains `kanban` when CLI orchestration is expected;
- messaging-platform toolsets;
- profile model/provider/reasoning settings;
- delegation routing or spawn depth;
- gateway platform configuration, credentials, or authentication;
- board databases, task rows, or workspaces during the configuration cutover; or
- worker profile toolsets merely to make the Sol controller an orchestrator.

## Preflight

Before writing configuration:

- capture a credential-free rollback artifact containing only the complete pre-change `platform_toolsets` and `kanban` subtrees, their YAML types, and the pre-install skill/runtime bytes;
- generate the config snapshot with `scripts/capture_activation_snapshot.py`; do not manufacture `resolved_api_server_toolsets` or unmanaged hashes by hand;
- reject secret-like keys in the artifact rather than copying the complete config;
- run the rollback helper against a fake `HERMES_HOME` and verify dry-run plus apply preserve unrelated sentinel keys;
- verify the candidate skill and runtime commits/fingerprints match required reviews or an explicit permitted user waiver;
- verify `hermes tools list --platform api_server` currently lacks `kanban` and `hermes tools list --platform cli` reflects the intended CLI state;
- verify the gateway is supervised and `kanban.dispatch_in_gateway` is or will remain true;
- verify no standalone `hermes kanban daemon` is running against the same board root; and
- verify the current execution context is authorized to change configuration and is not attempting to bypass delegated-child Kanban mutation guards.

## Staged write

Use the supported Hermes toolset configuration surface to add Kanban only to API Server:

```text
hermes tools enable kanban --platform api_server
```

Then apply one typed YAML edit setting:

```yaml
kanban:
  auto_decompose: false
```

Do not replace the complete `kanban` mapping with that one key. Preserve all siblings and verify the resulting value is a YAML boolean, not a string.

After the write, parse the config and prove:

- `platform_toolsets.api_server` equals its exact pre-state plus one `kanban` member;
- every non-API-server platform list equals its pre-state;
- `kanban.auto_decompose is False`;
- every other `kanban` key/value equals its pre-state; and
- no unrelated top-level key changed.

Any additional semantic diff triggers immediate config rollback before activation.

Run `scripts/validate_activation_delta.py --before <snapshot> --after <snapshot>` against snapshots produced from the real parsed pre/post config. The validator rejects raw/resolved disagreement, pre-existing Kanban, missing pre-existing API-server tools, any other platform change, unmanaged config drift, and any Kanban mapping change beyond `auto_decompose: false`.

## Dispatcher and project setup

The gateway-embedded dispatcher remains the only dispatcher. Do not start the deprecated standalone daemon.

Kanban transport is not ready for a project until Sol verifies or explicitly creates:

- a dedicated named board for that unrelated project or repository;
- the board's display identity and persistent default work directory when needed;
- the exact assignee profiles from the live profile catalog;
- profile model/provider/reasoning/toolsets and pinned task skills;
- workspace rules (`worktree`, trusted absolute `dir`, or disposable `scratch` with declared artifacts);
- retry/runtime budgets and notification behavior; and
- Sol-plan idempotency keys and the runtime-enforced worker no-child-card guard.

The global `default` board remains valid for intentionally shared/general work. Do not move existing cards or change the current board pointer as part of this cutover.

## Activation

Toolset changes do not alter the schema of an already-open session. Activate at a safe external boundary:

1. Restart or reload the gateway/API-server process through its normal supervisor; never terminate the service from the request it is currently serving.
2. Start a fresh WebUI session (`/reset`) so the new tool schema and skill body load.
3. Do not create a project card until every smoke gate below passes.

## Smoke verification

From a fresh top-level API-server Sol session, verify:

- the model-facing schema exposes `kanban_list`, `kanban_create`, and the needed orchestrator board tools;
- no `HERMES_KANBAN_TASK` or delegated-child context is present;
- the default board can be listed read-only;
- the gateway reports one supervised running service and the embedded dispatcher owns the singleton path;
- profile discovery returns exact configured profiles;
- `kanban.auto_decompose` is false;
- a temporary isolated test board can be created only when the smoke is explicitly authorized;
- on that isolated board, two concurrent same-idempotency creates return one card ID and one row;
- a test card using `sol-plan:<plan>:<task>:<attempt>` spawns a worker whose schema omits/refuses `kanban_create`, while a generic Kanban worker retains normal fan-out;
- parent-at-create gating, done→plan-verify reconciliation, and archival retention work as documented; and
- the temporary board/workspaces are archived or retained according to the smoke plan without touching existing boards.

A CLI/help listing is not model-facing schema proof. A database file is not dispatcher proof. A card marked done is not plan acceptance proof.

## Rollback

Rollback is required on config drift, failed gateway restart, missing orchestrator tools, duplicate idempotent cards, missing worker fence, profile/dispatcher mismatch, or any smoke mutation outside the isolated test board.

Rollback procedure:

1. Stop new card creation and preserve the smoke board, card IDs, runs, logs, and artifact evidence.
2. Restore the exact pre-change `platform_toolsets` and `kanban` subtrees through `scripts/restore_activation_config.py`; run `--dry-run` first and use `--apply` only after it passes.
3. Restore the reviewed pre-change skill/runtime bytes when activation failure is caused by those artifacts.
4. Reload the gateway externally and start a fresh session.
5. Verify API Server no longer exposes Kanban, CLI/other platforms match pre-state, `auto_decompose` and all other Kanban values match pre-state, and no unrelated config changed.
6. Read back every smoke task/external effect. Archive the test board only after rollback evidence no longer depends on live board state.

The rollback helper never edits credentials, memories, sessions, unrelated config, or user project workspaces and never restarts Hermes itself.

## Verification checklist

- [ ] Pre-change typed config subtrees and skill/runtime bytes are in a credential-free rollback artifact.
- [ ] Fake-home rollback dry-run and apply tests preserve unrelated sentinels.
- [ ] Only API Server gains `kanban`; all other platform toolsets are unchanged.
- [ ] `kanban.auto_decompose` is explicitly false and every sibling Kanban key is unchanged.
- [ ] One gateway-embedded dispatcher is active; no competing standalone daemon exists.
- [ ] Fresh API-server schema exposes Kanban only in an authorized top-level context.
- [ ] Concurrent idempotent create and Sol-plan worker-fence smoke gates pass in isolation.
- [ ] Board/profile/workspace/dependency/recovery behavior matches `kanban-transport.md`.
- [ ] Rollback restores exact pre-state and independently verifies tool/schema/config readback.
