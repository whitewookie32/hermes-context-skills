---
name: codex-fractals
description: Use when a bounded coding task must be decomposed into dependency-aware Codex worktree leaves with explicit scope contracts.
version: 1.0.0
license: MIT
metadata:
  agent_skills:
    tags: [codex, fractals, worktrees, task-decomposition, parallel-execution]
---

# Codex + Fractals

Use this workflow for a complex implementation that benefits from explicit decomposition into small, independently verifiable Codex tasks. Fractals is experimental orchestration software; do not treat recursive decomposition as authority to expand scope, publish changes, or bypass review.

## Preconditions

- The parent repository has a clean, committed baseline.
- Every proposed leaf has a scope contract before execution:
  - hierarchical task ID and concise task description;
  - allowed and prohibited relative paths;
  - completed dependency IDs;
  - concrete acceptance commands;
  - timeout, escalation conditions, and `noNetworkPublish: true`.
- Do not schedule two leaves that can write the same file. Resolve interfaces and ownership before creating worktrees.

## Safe Codex leaf contract

For each approved leaf:

1. Create an isolated Git worktree and branch from the verified baseline.
2. Run Codex with normal sandbox and approval policy—never `--yolo`, and do not add a permission-bypass flag.
3. Give Codex only the approved task, permitted paths, dependencies, test commands, and escalation conditions.
4. Keep credentials and general application configuration out of child-process environments. If a dedicated executor home is required for authentication, create and manage it outside the repository; never commit or copy its credential files.
5. Enforce a finite timeout and terminate the entire child process group on expiry.
6. Reject any result that changes Git history, touches prohibited/out-of-scope paths, or fails its acceptance commands.
7. Return a concise handoff with changed files, commands/outcomes, risks, and blockers. Do not let a leaf commit, merge, push, or publish.

## Codex invocation pattern

The Fractals pilot uses structured output so the runner can preserve the leaf handoff:

```bash
codex exec --json 'Execute only the approved leaf contract. Run the stated acceptance commands. Do not commit, merge, push, publish, change credentials, or edit paths outside the contract.'
```

Run it from that leaf's worktree. The orchestrator—not the leaf—owns dependency release, integration, conflict resolution, final commits, and any publication decision.

## Execution waves

1. Validate every contract: paths must be relative/non-traversing; no leaf can depend on itself; allowed paths cannot overlap prohibited paths.
2. Run only dependency-ready leaves concurrently.
3. Wait for evidence and review for every leaf before releasing dependents.
4. Integrate one verified change set at a time in a dedicated integration worktree.
5. Run repository-wide tests and inspect the final diff before committing or opening a pull request.

## Fractals project boundary

The upstream project is [TinyAGI/fractals](https://github.com/TinyAGI/fractals). It is experimental and requires its own separately managed installation and provider configuration. This skill packages the portable Codex safety contract, not the Fractals application, its web server, dependencies, or credentials.

## Do not use Fractals when

- The task is a small, linear change that one Codex session can safely verify.
- Interfaces or file ownership between prospective leaves are unresolved.
- The repository baseline is dirty or the work requires a human-controlled credential, external publication, deployment, or destructive operation.
- You need automatic branch merging: treat it as an explicit integration/review phase, not a leaf-agent capability.
