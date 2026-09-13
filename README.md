# Codex-Only Skills

> This is the `codex-only` branch of [`whitewookie32/hermes-context-skills`](https://github.com/whitewookie32/hermes-context-skills). It is a standalone, single-agent Codex CLI bundle. The repository's `main` branch retains the Hermes LCM, compression, Headroom, and multi-agent orchestration bundle.

## Included

| Skill | Purpose |
| --- | --- |
| [`codex`](skills/autonomous-ai-agents/codex/) | Run OpenAI Codex CLI safely for implementation, isolated PR review, and parallel worktree tasks. |

## Install

Copy the `skills/autonomous-ai-agents/codex/` directory into the skill location recognized by your Codex setup.

```text
skills/autonomous-ai-agents/codex/
```

## Codex-only boundaries

- This branch does **not** require Hermes, OpenClaw, an LCM plugin, Headroom, or a multi-agent coordinator.
- Use Codex in a Git worktree or repository. For scratch work, initialize a disposable Git repository first.
- Use `codex exec` for bounded tasks. Review the diff and run the relevant checks before committing or pushing.
- Prefer one Codex process per isolated worktree for parallel tasks; do not run concurrent writers in the same worktree.
- Never place API keys, OAuth tokens, or `~/.codex/` credential files in the repository.

## Verification

```bash
codex --version
git status --short
```

For authentication repair, see [`skills/autonomous-ai-agents/codex/references/codex-oauth-troubleshooting.md`](skills/autonomous-ai-agents/codex/references/codex-oauth-troubleshooting.md).

## License

MIT. See [`LICENSE`](LICENSE).
