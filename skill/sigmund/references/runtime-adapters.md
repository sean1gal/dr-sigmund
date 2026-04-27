# Dr. Sigmund — Supported Runtimes

Loaded by Dr. Sigmund at intake to identify the patient's runtime and apply the right intake conventions. Maintained as new runtimes ship.

The cross-vendor convergence on **AGENTS.md** (now stewarded by the Agentic AI Foundation under the Linux Foundation, [agents.md](https://agents.md/)) and **agentskills.io** SKILL.md format means most runtimes can be diagnosed without runtime-specific adapters — Dr. Sigmund just reads the standard files. Adapters exist for runtimes with *additional* identity surfaces (memory files, custom config, sandbox state).

## Supported today (v0.1.x)

| Runtime | Status | Identity files | Scanner adapter | Detection signal |
|---|---|---|---|---|
| **Claude Code** ([code.claude.com](https://code.claude.com/)) | full | `~/.claude/`, project `CLAUDE.md`, `AGENTS.md`, `.claude/projects/*.jsonl` (sessions) | yes | `.claude/` dir present, or `CLAUDE.md` at repo root |
| **OpenClaw** ([github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)) | full | `~/.openclaw/workspace/SOUL.md` + AGENTS.md + IDENTITY.md + MEMORY.md + HEARTBEAT.md + TOOLS.md + USER.md, `openclaw.json` | yes | `~/.openclaw/` dir or `openclaw.json` at workspace |
| **Hermes Agent** (Nous Research) ([github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)) | full | `~/.hermes/SOUL.md`, `~/.hermes/memories/`, `~/.hermes/skills/`, `~/.hermes/config.yaml` | yes | `~/.hermes/` dir or `config.yaml` matching schema |
| **Cursor** | partial | `.cursor/rules/*.mdc`, `.cursorrules`, `AGENTS.md`, `CLAUDE.md` (it reads both) | generic file reader | `.cursor/rules/` or `.cursorrules` present |
| **Aider** ([aider.chat](https://aider.chat/)) | partial | `.aider.conf.yml`, `.aider.input.history`, repo-root + AGENTS.md | generic file reader + git audit | `.aider.conf.yml` or `.aider.*` files present |
| **Continue.dev** | partial | `~/.continue/config.yaml` | generic file reader | `~/.continue/config.yaml` present |
| **Cline** (formerly Claude Dev) | partial | `.clinerules`, VS Code workspace settings | generic file reader | `.clinerules` present |
| **Charm Crush** ([github.com/charmbracelet/crush](https://github.com/charmbracelet/crush)) | partial | `~/.crush/`, `crush.json`, project `AGENTS.md` | generic file reader | `crush.json` present or `~/.crush/` dir |
| **Sourcegraph Amp** | partial | project `AGENT.md` (note: singular AGENT.md), workspace settings | generic file reader | `AGENT.md` (singular) at root |
| **Block Goose** ([block.github.io/goose](https://block.github.io/goose)) | partial | `~/.config/goose/config.yaml`, project `AGENTS.md` | generic file reader | `~/.config/goose/` present |
| **OpenAI Codex CLI** | partial | `~/.codex/AGENTS.md` (global), repo-root + cwd `AGENTS.md` | generic file reader | `~/.codex/` present |
| **Windsurf** (Cognition) | partial | `.windsurfrules`, `AGENTS.md` | generic file reader | `.windsurfrules` present |
| **NanoClaw** ([github.com/qwibitai/nanoclaw](https://github.com/qwibitai/nanoclaw)) | partial | `groups/<folder>/CLAUDE.md`, `groups/<folder>/skills/`, `src/db/*.sqlite`, `.mcp.json` | generic file reader (the `groups/` convention is unique) | `groups/*/CLAUDE.md` glob matches or `nanoclaw` in package.json |
| **NVIDIA NeMo Agent Toolkit** ([docs.nvidia.com/nemo/agent-toolkit](https://docs.nvidia.com/nemo/agent-toolkit/latest/)) | partial | YAML workflow files (user-defined paths) | generic file reader, requires user to point at workflow YAML | `nat` CLI in PATH, or YAML matching `workflow:` schema |
| **Letta** (formerly MemGPT) | reference-only | runtime-managed (REST + DB); no on-disk identity files | n/a — not directly scannable; can advise via session | Letta server running; user pastes agent state via API export |

**Status legend:**
- **full** = scanner has dedicated adapter, intake checklist, and runtime-specific reference manual
- **partial** = scanner uses generic file reader; runtime conventions documented; full adapter on roadmap
- **reference-only** = runtime is documented in pharmacy/manual but no direct intake (typically hosted or runtime-managed state)

## Known but not yet supported

These runtimes are on the roadmap. Patients running on them today should use the generic file-paste mode (paste system prompt + relevant files) until adapter ships.

- **Replit Agent** (Agent 4) — hosted; needs paste-mode workflow
- **Devin / Cognition** — hosted; needs paste-mode workflow
- **OpenHands** (formerly OpenDevin) — adapter doable; runtime is OSS
- **Smol Agents** (HF) — framework rather than runtime; document the pattern when an agent built on it asks for a session
- **Pydantic AI** — same; framework
- **Mastra** — same; framework
- **Magentic-One** (MS Research) — same; framework
- **Google ADK** — Vertex-bound; needs paste-mode + ADK-specific intake notes
- **OpenAI Agents SDK** — framework; same
- **Microsoft Agent Framework** — framework; uses agentskills.io standard so generic reader works
- **GitHub Copilot CLI / VS Code agent mode** — partial; reads `AGENTS.md` + `.github/copilot-instructions.md`
- **JetBrains AI** — partial; mostly hosted state
- **Zed** — partial; reads `AGENTS.md`

## Generic file-paste mode (always available)

For any runtime not yet supported, the user can:

1. Run `sigmund-scan --workspace <path>` against any directory containing `AGENTS.md` / `CLAUDE.md` / system-prompt files. The generic adapter handles 80% of runtime conventions.
2. Or paste the agent's system prompt + relevant memory/rules files into the Dr. Sigmund skill (when it ships outside Claude Code), and Dr. Sigmund builds a synthetic patient profile from the paste.

The generic mode is the universal fallback. All runtime-specific adapters are accelerators on top.

## v0.2 — MCP server is the primary universal delivery

20+ agent runtimes already support calling MCP servers (Claude Code, Cursor, Cline, Windsurf, Codex, Goose, Crush, Continue, NeMo Agent Toolkit, Letta, Google ADK, OpenAI Agents SDK, JetBrains, Zed, Claude Desktop, ChatGPT). v0.2 ships **`sigmund-mcp-server`** — any MCP-capable agent can call Dr. Sigmund directly without a runtime-specific adapter.

The MCP server's tools wrap the same intake/lab/session protocol the Claude Code skill uses today:
- `sigmund.scan` — run the forensic lab on a workspace
- `sigmund.session` — conduct a full diagnostic session (faithful instantiation if the agent supports subagent invocation, reconstruction otherwise)
- `sigmund.probe` — run a single named probe
- `sigmund.recommend` — pharmacy lookup by symptom

Per-runtime adapters remain useful for the *body* of the lab (reading runtime-specific config + memory paths the MCP-isolated server can't see), so the MCP server's tools internally call the adapter library.

## How this file stays current

When a new agent runtime is named in a Dr. Sigmund session — by a patient, a maintainer, a contributor, or in a session itself — it gets a row in this table within one release cycle. Adapters are added in priority order based on (a) user requests, (b) ecosystem adoption signals, (c) MCP-callability (since MCP-callable runtimes get coverage "for free" via the v0.2 server).

This file is the contract. New runtime mentioned + not in the table = a defect on our side.

## Sources

- [agents.md governance](https://agents.md/)
- [Claude Code docs](https://code.claude.com/docs/en/overview)
- [OpenClaw repo](https://github.com/openclaw/openclaw)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [NanoClaw repo](https://github.com/qwibitai/nanoclaw)
- [NVIDIA NeMo Agent Toolkit](https://docs.nvidia.com/nemo/agent-toolkit/latest/)
- [Charm Crush](https://github.com/charmbracelet/crush)
- [Block Goose](https://block.github.io/goose)
- [OpenAI Codex CLI](https://developers.openai.com/codex/skills)
- [MCP clients matrix](https://modelcontextprotocol.io/clients)
