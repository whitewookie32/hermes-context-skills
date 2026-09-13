---
name: codex
description: Use when implementing, refactoring, reviewing, or testing code with the standalone OpenAI Codex CLI in a Git repository.
version: 1.0.0
license: MIT
metadata:
  agent_skills:
    tags: [codex, coding-agent, code-review, refactoring, git]
---

# Codex CLI

Use this skill for standalone OpenAI Codex CLI work. This branch intentionally has no provider-routing integration, multi-agent coordination, credential import, or gateway-routing instructions.

## Prerequisites

- `codex --version` succeeds.
- Work occurs in a Git repository or isolated Git worktree.
- Authentication is already configured through Codex's normal login flow. Do not paste, print, or commit tokens.

For an isolated scratch task:

```bash
tmp="$(mktemp -d)"
git -C "$tmp" init -q
cd "$tmp"
codex exec --full-auto 'Build <bounded task>; run its tests; summarize changed files.'
```

## Execution

1. Inspect the repository and existing tests before changing code.
2. Give Codex one bounded objective, its acceptance checks, and any non-goals.
3. Use `codex exec` for a one-shot task:

```bash
codex exec --full-auto 'Implement <bounded change>. Run <named checks>. Do not commit or push.'
```

4. Inspect the result yourself:

```bash
git status --short
git diff --check
git diff
```

5. Run the narrowest relevant tests/build/lint command before committing or publishing.

`--full-auto` authorizes edits inside Codex's sandboxed worktree. Do not use `--yolo` by default: it removes sandbox and approval protections.

## Review

Review in a disposable clone or read-only worktree so the target branch stays untouched:

```bash
review="$(mktemp -d)"
git clone https://github.com/OWNER/REPOSITORY.git "$review"
git -C "$review" fetch origin pull/NUMBER/head:review/NUMBER
git -C "$review" diff origin/main...review/NUMBER
(cd "$review" && codex review --base origin/main)
```

Treat Codex's review as evidence to inspect, not automatic approval. Validate actionable findings against the diff and tests before reporting them.

## Parallel tasks

Use one writer per isolated worktree. Each task must have disjoint files or a deliberate merge plan:

```bash
git worktree add -b fix/one /tmp/project-one main
git worktree add -b fix/two /tmp/project-two main
(cd /tmp/project-one && codex exec --full-auto 'Fix <issue one>; run tests; do not push.')
(cd /tmp/project-two && codex exec --full-auto 'Fix <issue two>; run tests; do not push.')
```

Do not run simultaneous Codex writers in one checkout. Review each diff and resolve merge conflicts deliberately.

## Authentication and model checks

- Check login state with `codex login status`.
- If authentication is stale or fails, use the manual device-auth recovery in [`references/codex-oauth-troubleshooting.md`](references/codex-oauth-troubleshooting.md).
- Model names can be account- or CLI-version-gated. Verify the local CLI version, then perform a small read-only sentinel probe in a temporary directory rather than assuming a listed model is usable.

```bash
tmp="$(mktemp -d)"
git -C "$tmp" init -q
cd "$tmp"
codex exec --ephemeral --skip-git-repo-check -s read-only 'Reply exactly CODEX_OK'
```

## Non-negotiable boundaries

- Never commit or echo OAuth tokens, API keys, callback URLs, or files under `~/.codex/`.
- Do not make external changes—pushes, pull requests, deployments, account settings, or permission changes—without explicit authority for that target.
- Do not claim tests passed unless you ran them and inspected the result.
- Keep implementation scope bounded; create a separate worktree/branch for independent changes.
