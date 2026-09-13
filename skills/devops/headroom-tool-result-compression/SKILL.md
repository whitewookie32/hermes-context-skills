---
name: headroom-tool-result-compression
description: Use when adding optional Headroom compression for large tool results without compromising exact reads.
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [headroom, compression, tool-results, mcp, hermes]
    related_skills: [hermes-agent, context-compression-integration]
---

# Headroom Tool-Result Compression

Use this skill when adding a content-aware compression layer to a Hermes/Donna runtime. The goal is to shrink repetitive tool outputs before the next model call without replacing Hermes' native conversation compression or exact file-read behavior.

## Best-fit scope

Headroom is useful for high-bloat text results:

- terminal/build logs with repeated INFO lines and sparse ERROR/WARN lines
- large JSON/API arrays with repeated schema
- grep/search output where structure matters more than every line
- generated reports or tabular dumps where summary + anomalies are enough

Do **not** use automatic compression for exact retrieval tools unless the user explicitly asks. Exact reads should stay exact and the model can rerun them with narrower ranges.

## Integration pattern

1. Load current Hermes command guidance first (`hermes-agent`), then use supported Hermes commands for configuration and verification.
2. Back up `~/.hermes/config.yaml` to a timestamped `~/.hermes/archive/<operation>/config.yaml.before` before mutation.
3. Keep Headroom's MCP-server runtime isolated from Hermes' own Python environment. Do **not** install the historical `headroom-ai==0.24.0` into the Hermes venv as a generic fix: its unconstrained `mcp>=1` dependency can resolve MCP SDK 2.x, while its server still calls the removed v1 `Server.list_tools()` API and exits with `Connection closed`. Create a dedicated current Headroom venv instead:

```bash
HEADROOM_VENV="$HOME/.hermes/headroom-mcp-venv"
uv venv --python "$HOME/.hermes/hermes-agent/venv/bin/python" "$HEADROOM_VENV"
uv pip install --python "$HEADROOM_VENV/bin/python" 'headroom-ai[mcp]==0.37.0'
uv pip check --python "$HEADROOM_VENV/bin/python"
"$HEADROOM_VENV/bin/headroom" mcp status
```

`uv venv` does not necessarily bundle `pip`; use `uv pip check`, not `python -m pip check`, for this verification.

4. Back up `~/.hermes/config.yaml`, then point only the Headroom MCP entry at the isolated binary. Set a safe `cwd` such as `$HOME`: an agent workspace can contain a file such as `inspect.py` that shadows a Python standard-library module and crashes the server before discovery.

```bash
stamp="$(date +%Y%m%d-%H%M%S)"
mkdir -p "$HOME/.hermes/archive/headroom-mcp-$stamp"
cp "$HOME/.hermes/config.yaml" "$HOME/.hermes/archive/headroom-mcp-$stamp/config.yaml.before"
hermes config set mcp_servers.headroom.command "$HOME/.hermes/headroom-mcp-venv/bin/headroom"
hermes config set mcp_servers.headroom.cwd "$HOME"
hermes config check
hermes mcp test headroom
```

A successful test must report `Connected` and exactly three tools: `headroom_compress`, `headroom_retrieve`, and `headroom_stats`. Start a fresh Hermes/WebUI session after the configuration change so its cached tool schema is rebuilt.

5. Keep automatic compression as a separate, reversible config flag. Example shape:

```yaml
headroom:
  enabled: true
  auto_compress_tool_results: true
  min_chars: 8000
  min_savings_ratio: 0.15
  skip_tools:
    - headroom_compress
    - headroom_retrieve
    - headroom_stats
    - read_file
    - mcp_qmd_get
    - mcp_qmd_multi_get
    - vision_analyze
    - browser_vision
```

6. Hook compression after a tool returns and before oversized-output persistence/truncation. This lets Headroom shrink structured bloat first; Hermes can still spill the result to disk if the compressed form is too large.
7. Guard the hook:
   - no-op unless `headroom.enabled` and `headroom.auto_compress_tool_results` are true
   - only process string tool results
   - skip multimodal/image tool results
   - skip Headroom's own tools to avoid recursion
   - skip exact document/file-read tools
   - require a minimum size and a minimum savings ratio
   - on any Headroom exception or insufficient savings, return the original content unchanged
8. Add an audit header to compressed tool results so the model knows it is seeing a compressed representation and can rerun the tool with a narrower query/range when exact detail matters.

## Verification

Use a focused local probe before claiming success:

```python
from agent.headroom_tool_compression import maybe_compress_tool_result

rows = []
for i in range(160):
    if i in (17, 88, 121):
        rows.append(f"2026-06-10T12:00:{i%60:02d}Z ERROR payment failed order={i} retry=false")
    else:
        rows.append(f"2026-06-10T12:00:{i%60:02d}Z INFO health_check ok worker=checkout latency=12ms")
content = "\n".join(rows)
out = maybe_compress_tool_result("terminal", content)
print(len(content), len(out), "order=88" in out)
```

Also run:

```bash
./venv/bin/python -m py_compile agent/headroom_tool_compression.py agent/tool_executor.py
./venv/bin/python -m pytest tests/agent/test_headroom_tool_compression.py tests/tools/test_tool_result_storage.py -q
hermes mcp list
```

If the live WebUI/gateway process was already running before the code hook changed, restart the service after reporting or at a safe point:

```bash
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
launchctl kickstart -k gui/$(id -u)/com.npadilla.donna-webui
```

## Pitfalls

- Do not replace Hermes' native conversation compression with Headroom. They solve different layers: conversation/history compaction vs. high-bloat tool-result triage.
- Do not compress `read_file`/exact retrieval outputs automatically. The agent needs exact text for code edits and legal/contract-style quoting.
- Do not treat Headroom MCP registration as automatic compression. MCP exposes tools; an executor hook or proxy is needed for automatic mutation of tool results.
- Do not use system Python for config-edit snippets on machines where PyYAML is only installed in the Hermes venv. Use the Hermes venv Python or supported `hermes config` commands.
- Do not restart the live WebUI/gateway mid-response unless the user accepted the interruption or the service restart is clearly safe.
