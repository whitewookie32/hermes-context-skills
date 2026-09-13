# Hermes Context Skills

A small, shareable Hermes skill bundle for **lossless context recall**, **safe context compression**, **Headroom-based tool-result triage**, and **bounded multi-agent orchestration**.

## Included skills

| Skill | What it covers |
| --- | --- |
| [`hermes-lcm`](skills/hermes-lcm/) | Operating and retrieving exact evidence from the Hermes-LCM context plugin. |
| [`context-compression-integration`](skills/software-development/context-compression-integration/) | Designing and verifying protected-context and tool-result compression paths. |
| [`headroom-tool-result-compression`](skills/devops/headroom-tool-result-compression/) | Adding optional Headroom compression for large, repetitive tool outputs without compromising exact reads. |
| [`sol-terra-parallel-orchestration`](skills/autonomous-ai-agents/sol-terra-parallel-orchestration/) | Plans bounded Direct or Parallel execution with safety controls, consultation coverage, and durable work-item records. |
| [`the-comamander`](skills/autonomous-ai-agents/the-comamander/) | Runs bounded specialist committees under a Chairman who owns the decision and verification. |
| [`bot-communication-contracts`](skills/autonomous-ai-agents/bot-communication-contracts/) | Defines reviewable, minimum-context handoffs and structured evidence contracts between Hermes profiles. |

## Design rules

1. **Raw messages and exact reads remain source truth.** Summaries and compressed tool output must preserve a route back to narrower or exact retrieval.
2. **Keep layers separate.** Hermes-LCM compacts conversation history; Headroom triages high-bloat tool output. One does not replace the other.
3. **Protect governing context.** System instructions, active tool contracts, and the newest active tool sequence should not be silently rewritten.
4. **Verify live behavior.** A configured proxy, installed MCP server, or healthy process is not proof that the relevant request path is active.
5. **Keep authority explicit.** The Chairman owns scope, approvals, reconciliation, and final verification; specialist evidence informs a decision but never replaces it.

## Installation

Copy the individual skill directories into the matching locations in your Hermes skill library, then start a new Hermes session so skill discovery and tool schemas refresh.

```text
skills/hermes-lcm/
skills/software-development/context-compression-integration/
skills/devops/headroom-tool-result-compression/
skills/autonomous-ai-agents/sol-terra-parallel-orchestration/
skills/autonomous-ai-agents/the-comamander/
skills/autonomous-ai-agents/bot-communication-contracts/
```

For LCM activation, enable the `hermes-lcm` plugin and set `context.engine: lcm`. The `hermes-lcm` skill includes the configuration reference.

## Headroom scope

Headroom is intentionally limited to large, repetitive string tool results. Do not automatically compress exact-source tools such as file or document reads. The included skill provides the isolation, configuration, hook guards, and verification sequence.

## License

MIT. See [`LICENSE`](LICENSE).
