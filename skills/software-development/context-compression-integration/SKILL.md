---
name: context-compression-integration
description: 'Use when integrating context compression. Verify both paths.'
license: MIT
metadata:
  category: software-development
  tags: "context compression, tool calls, prompt routing, Headroom, Hermes, OpenClaw"
---

# Context compression integration

Use this class-level workflow when a compression layer must operate across initial prompt context, conversation history, tool calls, tool results, or multiple agent runtimes.

## Procedure

1. **Map request paths before editing.** Identify where each runtime assembles initial system/context entries, ordinary messages, tool calls, and tool results. Separate client-side context compression from proxy-side request optimization; they are independent layers.

2. **Define protected beginning context.** Construct a stable, explicit beginning-context block containing system instructions, identity/profile context, workspace/runtime rules, active skills, and tool contracts. Keep it lossless and before ordinary history. Reserve headroom for the current request, next response, active tool calls, and retrieval metadata before compression.

3. **Compress the remaining context.** Apply compression to older messages and large tool results while preserving the active tool-call sequence and newest user turn. Keep retrieval references for removed content. Do not treat provider prefix caching as a substitute for a protected header.

4. **Implement both calls explicitly when required.** Use one call/path to establish or preserve the beginning-context prefix and a second call/path to compress conversation history and tool results. Ensure the second path cannot rewrite or drop the protected prefix. If a runtime only exposes one assembly hook, adapt the structure inside that hook rather than claiming a two-call design exists.

5. **Verify configuration and live execution separately.** Check configuration, source wiring, process environment, and proxy health first. Then issue a real request containing a distinctive initial-context marker and a real tool result. Confirm the marker survives and compression counters or request logs change. A healthy proxy or configured URL alone is not proof of routing.

6. **Report state with three labels.** Distinguish **configured**, **active**, and **verified**. State separately whether initial entries, ordinary messages, tool calls, and tool results are covered. Do not call the integration complete when only model-request routing or only tool-result compression has been proven.

## Evidence gates

- Require request counts to increase on the intended proxy for a live routing test.
- Require compression counters, token deltas, or request transforms for a compression test; pass-through alone is insufficient.
- Inspect actual request assembly code before asserting that system messages or beginning context are compressed or protected.
- Preserve exact tool calls and tool results needed for continuation; compression must not make active tool state unrecoverable.

## Pitfalls

- **Do not infer initial-context coverage from tool-result statistics — the paths often use different hooks and flags.**
- **Do not claim a header or two-call flow from a proposed layout — verify concrete implementation and live request evidence first.**
- **Do not enable system-message compression by default when governing instructions live there — protect them explicitly and test content stability.**
- **Do not count MCP/manual compression as ordinary model-request routing — an MCP tool can be healthy while model transport bypasses the proxy.**
- **Do not use a short smoke prompt to judge efficiency — use a controlled repetitive payload large enough to trigger the threshold.**

## References

- See `references/runtime-verification.md` for the reusable verification matrix and provider/runtime checks.
