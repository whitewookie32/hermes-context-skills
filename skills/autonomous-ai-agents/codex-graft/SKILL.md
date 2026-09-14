---
name: codex-graft
description: Use when Codex needs a local code graph for repository orientation, symbol tracing, impact analysis, or scoped code search.
version: 1.0.0
license: MIT
metadata:
  agent_skills:
    tags: [codex, graft, code-graph, mcp, repository-analysis]
---

# Codex + Graft

Use Graft to give Codex a compact, local, repository-specific code graph. Graft indexes code locally and can expose graph queries through MCP; it does not grant write access or replace direct source inspection.

## Prerequisites

- Work inside the target Git repository.
- Install Graft separately and verify it before configuration:

  ```bash
  graft --version
  ```

- Treat `graft/` as generated index state unless the repository explicitly tracks it. Do not build an index across secrets, vendored dependencies, build output, or unrelated nested repositories.

## Build a narrow graph

1. Start with a structural graph—no model/API key required:

   ```bash
   graft build .
   graft check .
   ```

2. Constrain the graph when only part of a large repository is relevant:

   ```bash
   graft build --only-dir src --only-dir tests .
   ```

3. Use `--deep` only when symbol summaries and a concept map justify the additional model work. Do not pass credentials in the command line; use Graft's documented environment/configuration path.

## Add Graft to Codex through MCP

Register a server for the specific repository after building its graph:

```bash
codex mcp add graft-my-project -- graft mcp /absolute/path/to/repository
```

Then start a new Codex session and inspect active servers with:

```text
/mcp
```

The server exposes graph queries including `graft_find_code`, `graft_trace_calls`, `graft_find_all`, `graft_file_api`, `graft_repo_map`, and `graft_check_freshness`.

Use a distinct MCP server name and absolute repository path per project. Do not register a broad home-directory graph, and do not run `graft init` without a dry-run and explicit review: it can modify agent instructions and configuration.

## Operating sequence

1. Ask for `graft_check_freshness` before relying on graph results.
2. Orient with `graft_repo_map` or `graft_file_api`.
3. Trace callers/callees or search before changing a shared API.
4. Read the source files implicated by the graph before making an exact claim or edit.
5. Rebuild and check the graph after structural code changes.

## Guardrails

- Graph output is navigation evidence, not a substitute for source code, tests, or runtime verification.
- Keep one repository per graph/MCP server. Nested-repository and submodule indexing are opt-in because they can change scope materially.
- Prefer a project-local Codex configuration where supported; avoid mutating global Codex configuration for a one-off repository.
- Never expose `.env` files, credentials, private keys, or generated caches through graph prompts or shared output.
