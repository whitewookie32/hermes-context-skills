# Concurrent Evidence Freshness

Use this reference when a Chairman delegates a read-only review while other workers may change the same repository, configuration, or candidate artifact.

## Dispatch ledger

Record in every mutable-resource brief:

- repository/worktree identifier and revision or content fingerprint;
- exact files, services, or artifact hashes in scope;
- whether other work may mutate those resources;
- the observation time and a request for `changed-resources: none` on read-only work.

A reviewer may report valid evidence about that snapshot. It is not automatically evidence about later tree state.

## Chairman reconciliation

Before accepting a delayed finding that asserts a file is absent, a test is failing/passing, a route is unavailable, or an artifact has a property:

1. Inspect the current named resource yourself.
2. Re-run the smallest relevant test or verification command against the current state.
3. Compare current revision/content identifiers with the review snapshot.
4. Classify the finding as **current**, **superseded**, or **structural-only**.

Keep structural design advice when it remains independently sound, but never carry a stale aggregate verdict forward as approval of changed bytes or configuration.

## Final evidence ledger

For each material decision, record both the advisory snapshot and the Chairman's post-integration verification timestamp/fingerprint. The final answer must rely on the latter for claims about current implementation, candidate identity, deployment, or hardware readiness.
