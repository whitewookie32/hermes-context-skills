# Codex-Only Skills

This branch is a standalone bundle for **OpenAI Codex CLI**. It intentionally excludes Hermes-LCM, Headroom, and Hermes-specific orchestration/runtime configuration. Those remain on [`main`](../../tree/main).

## Included skills

| Skill | Use it for | Runtime dependency |
|---|---|---|
| [`codex`](skills/autonomous-ai-agents/codex/) | bounded implementation, refactoring, review, and test work | Codex CLI |
| [`codex-graft`](skills/autonomous-ai-agents/codex-graft/) | local code-graph orientation, symbol tracing, impact analysis, and MCP queries | Graft CLI |
| [`codex-fractals`](skills/autonomous-ai-agents/codex-fractals/) | dependency-aware parallel Codex leaves in isolated Git worktrees | TinyAGI Fractals (experimental) |

## Install

Copy the skill directories you want into the skill location recognized by your Codex setup:

```text
skills/autonomous-ai-agents/codex/
skills/autonomous-ai-agents/codex-graft/
skills/autonomous-ai-agents/codex-fractals/
```

These are workflow instructions, not vendored executables. Install and update Codex, Graft, and Fractals through their respective upstream projects. Keep credentials, generated indexes, caches, and application configuration outside this repository.

## Graft with Codex

Build a graph for a specific repository, then register the resulting graph as a Codex MCP server:

```bash
cd /absolute/path/to/repository
graft build .
graft check .
codex mcp add graft-my-project -- graft mcp "$PWD"
```

Start a new Codex session and use `/mcp` to confirm the server. See [`codex-graft`](skills/autonomous-ai-agents/codex-graft/) for freshness checks, per-repository scoping, and the `graft init` safety boundary.

## Fractals with Codex

Use Fractals only after defining leaf-task contracts, worktree ownership, dependencies, acceptance tests, timeouts, and escalation conditions. Leaf Codex agents must not commit, merge, push, publish, expand scope, or bypass sandbox/approval controls. See [`codex-fractals`](skills/autonomous-ai-agents/codex-fractals/) for the complete contract.

## Codex-only boundaries

- No Hermes runtime or provider configuration.
- No automatic access to Hermes-LCM or Headroom.
- No OAuth-token import, copied authentication state, `.env` files, private keys, caches, or generated output.
- No automatic publication, branch merging, deployment, or permission bypass.

## License

The bundle is MIT-licensed; see [`LICENSE`](LICENSE). Upstream tools retain their own licenses and installation requirements.
