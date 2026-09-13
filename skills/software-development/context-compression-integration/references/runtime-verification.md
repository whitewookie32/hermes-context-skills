# Runtime verification matrix

Use this matrix after implementation and after any routing/configuration change.

| Layer | Verify in source/config | Live proof | Failure meaning |
|---|---|---|---|
| Beginning context | A dedicated stable block is assembled before history; protected fields are explicit | Send a distinctive marker and confirm it is present and unchanged on the first and a later request | A generic prefix-cache hit does not prove header protection |
| Ordinary messages | The runtime passes the intended message list into the compressor | Proxy request log shows the request and input-token delta | A request count without a delta may be pass-through |
| Tool calls | Tool-call and tool-result roles are retained during conversion and reassembly | Use a real tool call, then inspect transforms or compression counters | MCP availability alone does not prove model-path coverage |
| Large tool results | Threshold and skip lists are known; active tool sequence is protected | Controlled repetitive result crosses the threshold and reduces tokens | Small smoke payloads can legitimately remain uncompressed |
| Provider routing | Base URL/env override is applied by the actual provider runtime | Intended proxy request count/provider/model increases | YAML configuration may be bypassed by provider-specific runtime code |
| Headroom margin | Token budget reserves current turn, response, tools, and retrieval metadata | Request remains below limit after compression and preserves continuation state | Compressing only after overflow is too late |

## Minimal evidence sequence

1. Record proxy stats before the test.
2. Send a small request with a unique beginning-context marker; verify routing and marker preservation.
3. Send a controlled request with a large repetitive tool result; verify token reduction and transform names.
4. Record proxy stats after the test and compare request count, compression count, and saved tokens.
5. Report each layer as configured, active, or verified; never merge those labels.

## Provider-specific check

Inspect the runtime implementation that resolves the endpoint. If it uses an environment variable or a provider-specific transport instead of the normal configuration field, set the override through the supervised process environment, restart that process, and verify the child process received it without printing secrets.
