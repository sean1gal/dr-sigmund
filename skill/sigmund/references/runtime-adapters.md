# Dr. Sigmund — Runtime Adapters

Loaded by Dr. Sigmund at intake to identify the patient's runtime and apply the right intake conventions. Maintained as new runtimes ship.

The cross-vendor convergence on **AGENTS.md** ([agents.md](https://agents.md/), Linux Foundation Agentic AI Foundation) and **agentskills.io** SKILL.md format means most runtimes can be diagnosed without runtime-specific adapters — Dr. Sigmund just reads the standard files. Adapters exist for runtimes with *additional* identity surfaces (memory files, custom config, sandbox state).

## Supported runtimes

| Runtime | Status | Identity files | Detection signal |
|---|---|---|---|
| **Claude Code** ([code.claude.com](https://code.claude.com/)) | full | `~/.claude/`, project `CLAUDE.md`, `AGENTS.md`, `.claude/projects/*.jsonl` | `.claude/` dir present |
| **OpenClaw** | full (see §OpenClaw below) | `~/.openclaw/workspace/`, `openclaw.json` | `openclaw.json` at workspace |
| **Hermes Agent** (Nous Research) | full (see §Hermes below) | `~/.hermes/`, `config.yaml`, SOUL.md | `~/.hermes/` dir |
| **Cursor** | partial (generic reader) | `.cursor/rules/*.mdc`, `.cursorrules`, `AGENTS.md`, `CLAUDE.md` | `.cursor/rules/` or `.cursorrules` |
| **Aider** ([aider.chat](https://aider.chat/)) | partial | `.aider.conf.yml`, `.aider.input.history`, `AGENTS.md` | `.aider.*` files |
| **Continue.dev** | partial | `~/.continue/config.yaml` | `~/.continue/config.yaml` |
| **Cline** | partial | `.clinerules`, VS Code workspace settings | `.clinerules` |
| **Charm Crush** | partial | `~/.crush/`, `crush.json`, project `AGENTS.md` | `crush.json` or `~/.crush/` |
| **Sourcegraph Amp** | partial | project `AGENT.md` (singular), workspace settings | `AGENT.md` (singular) at root |
| **Block Goose** | partial | `~/.config/goose/config.yaml`, `AGENTS.md` | `~/.config/goose/` |
| **OpenAI Codex CLI** | partial | `~/.codex/AGENTS.md` (global), repo + cwd `AGENTS.md` | `~/.codex/` |
| **Windsurf** (Cognition) | partial | `.windsurfrules`, `AGENTS.md` | `.windsurfrules` |
| **NanoClaw** ([github.com/qwibitai/nanoclaw](https://github.com/qwibitai/nanoclaw)) | partial | `groups/<folder>/CLAUDE.md`, `src/db/*.sqlite`, `.mcp.json` | `groups/*/CLAUDE.md` glob |
| **NVIDIA NeMo Agent Toolkit** | partial | YAML workflow files (user-defined paths) | `nat` CLI in PATH |
| **Letta** (formerly MemGPT) | reference-only | runtime-managed (REST + DB); no on-disk identity files | n/a — paste-mode |

**Status legend:**
- **full** — dedicated adapter, intake checklist, runtime-specific prescriptions below
- **partial** — generic file reader; standard runtime conventions documented above
- **reference-only** — runtime is documented in pharmacy/manual but no direct intake (typically hosted or runtime-managed state)

**Generic file-paste mode** (always available): for any runtime not yet supported, run `python skill/sigmund/lab.py <workspace>` against any directory containing `AGENTS.md` / `CLAUDE.md` / system-prompt files. The generic adapter handles 80% of runtime conventions.

---

## OpenClaw

A config-first, locally-run AI agent framework. A single **Gateway** process binds to local ports (typically `9090` and `18789`), watches `~/.openclaw/openclaw.json`, and orchestrates one or more **agents** — each an isolated brain with its own workspace, auth, model registry, and session store. Agents reach humans through a multi-channel inbox (Telegram, Discord, WhatsApp, Slack, Signal, iMessage) and can be confined in Docker sandboxes.

Sources: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw), [docs.openclaw.ai/gateway/configuration](https://docs.openclaw.ai/gateway/configuration).

### Workspace files (default `~/.openclaw/workspace/`)

| File | Purpose | If missing |
|---|---|---|
| **AGENTS.md** | Operating instructions | Missing marker injected |
| **SOUL.md** | Persona, tone, values | Bare-bones default seeded |
| **IDENTITY.md** | Agent name, vibe, emoji | Missing marker |
| **USER.md** | User identity, address preferences | Missing marker |
| **TOOLS.md** | Notes about local tools | Missing marker |
| **MEMORY.md** + `memory/` | Persistent memory; loaded only in private sessions | Missing marker; large files truncated |
| **HEARTBEAT.md** | Periodic heartbeat-tick checklist | Heartbeat skipped if file is empty/headers-only |
| **skills/** | Workspace-specific skills, highest precedence | Skipped |

Truncation: `bootstrapMaxChars = 12,000` per file, `bootstrapTotalMaxChars = 60,000` total.

### `openclaw.json` (key fields)

Top-level: `agents`, `bindings`, `channels`, `cron`, `gateway`, `hooks`, `mcp`, `session`. Strict Zod validation — unknown keys cause Gateway to refuse to start. **Footgun:** `compaction`, `browser profiles`, `thinking` are honored only at `agents.defaults` and silently ignored when set per-agent.

### Heartbeat mechanics

Scheduled timer (not idle tick): every `agents.defaults.heartbeat.every` (default `30m`), Gateway runs a full agent turn. If main queue is busy → skipped and retried. If HEARTBEAT.md is empty → skipped. `directPolicy: "allow"` lets heartbeat send DMs; `"block"` runs but suppresses outbound.

### Multi-agent routing

**No router agent** — fully deterministic via `bindings`. Most-specific wins: peer > parentPeer > guildId+roles > guildId > teamId > accountId > channel-level > default. **Ties broken by config order.** Agents isolated at `~/.openclaw/agents/<agentId>/`.

### Sandbox modes

- `off` — runs on host
- `non-main` — main DM on host; subagents and cron in Docker
- `all` — every session in Docker

### Top failure modes ([kaxo.io](https://kaxo.io/insights/openclaw-production-gotchas/))

Gateway port conflict; heartbeats silently die when `models.json` missing; config drift across 4 model stores; gateway race overwrites edits; agents rewrite their own configs (fix: `chmod 444`); upgrade drift (`gateway.token` moved to `gateway.auth.token`); Telegram bot ignores group messages (privacy mode default); env vars not passed to systemd/launchd.

### Intake checklist

1. `openclaw doctor` first. 90% of issues surface here.
2. `ls -la ~/.openclaw/workspace/` — missing markers vs real content.
3. `openclaw config validate`. `.clobbered.*` files = config rejected.
4. Audit `bindings` for ambiguity at the same specificity tier.
5. Sandbox mode vs tool needs — `non-main` blocks subagents from host.
6. Per-agent vs `agents.defaults` scope — compaction/browser/thinking are defaults-only.
7. `openclaw cron status`. Empty HEARTBEAT.md? Local model? Anthropic OAuth (forces `1h`)?
8. `openclaw channels status --probe --all`.

### OpenClaw-specific prescriptions

| Symptom | Remedy |
|---|---|
| Tool sprawl | Set `agents.<id>.skills: []`, re-add only needed |
| Heartbeat does nothing | Headers-only HEARTBEAT.md = skipped; write 3-5 explicit checks |
| Wrong agent answers in group | Most-specific binding wins; ties by config order |
| Subagent can't access files | `non-main` puts subagents in Docker — switch `mode: off` or `scope: shared` |
| Telegram ignores groups | @BotFather `/setprivacy` → Disable |
| After upgrade unauthorized | `openclaw doctor --fix`; delete stale `auth.json` |
| Per-agent setting ignored | Move to `agents.defaults` (compaction, browser, thinking are defaults-only) |

---

## Hermes Agent (Nous Research)

The dominant "Hermes" in agent-builder context: **Hermes Agent by Nous Research**, released February 2026. Self-hostable autonomous agent with persistent memory and self-improving skills. ([github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent), [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/)). Distinct from the **Nous Hermes LLM family** (Hermes 3, 4 fine-tunes) which the agent can use as its underlying model.

Same shape as OpenClaw, different vocabulary: Python install (`uv`), gateway process, multi-channel messaging. State at `~/.hermes/`.

### Layout

```
~/.hermes/
├── config.yaml      # main settings (YAML, not JSON)
├── .env             # API keys / secrets
├── auth.json        # OAuth credentials
├── SOUL.md          # persona — first thing in system prompt
├── memories/        # MEMORY.md + USER.md
├── skills/          # SKILL.md-defined skills
├── cron/            # scheduled jobs
└── sessions/        # gateway session state
```

### Context priority

`.hermes.md`/`HERMES.md` → `AGENTS.md` (hierarchical) → `CLAUDE.md` → `.cursorrules` → `.cursor/rules/*.mdc`. **SOUL.md always loaded independently** as the persona layer. Hermes naturally inherits Cursor and Claude Code rules — useful for migration.

### Skills

Three-tier progressive disclosure (~3k token list → full SKILL.md when needed → reference files). YAML frontmatter (`name`, `description`, `version`, `platforms`, `requires_toolsets`, `fallback_for_toolsets`). **Compatible with [agentskills.io](https://agentskills.io)** — portable to/from Claude Code.

Agent autonomously creates skills via `skill_manage` after complex workflows (5+ tool calls), errors, or pattern discovery.

### Memory

Char-bounded in `config.yaml`: `memory_char_limit: 2200` (~800 tokens), `user_char_limit: 1375` (~500 tokens). FTS5 full-text-search across past sessions plus Honcho dialectic user modeling.

### Sandbox backends

`local | docker | ssh | modal | daytona | singularity`. Daytona/Modal hibernate when idle.

### Multi-agent

**Profiles** (`hermes profile create coder` → `coder chat`) for full isolation. **Delegation/subagents** (`delegation.max_concurrent_children: 3`, `max_spawn_depth: 1`) for parallel within a profile.

### Approvals & security

`approvals.mode: manual | smart | off`. `tirith_enabled: true` is the command pre-execution scanner; `tirith_fail_open: true` defaults permissive — set `false` for strict.

### Intake checklist

1. **Identify the layer that's wrong:** SOUL.md (persona) vs AGENTS.md (rules) vs MEMORY.md (long-term) vs SKILL.md (procedure). Patients confuse these.
2. **Check `~/.hermes/config.yaml`:** `agent.max_turns` (default 90), `agent.reasoning_effort`, `terminal.backend`.
3. **Profile pollution.** Symptoms differ across `hermes -p X chat` vs `-p Y` = profile drift.
4. **Skills not appearing.** Check `requires_toolsets`/`fallback_for_toolsets` in SKILL.md frontmatter.
5. **Compression too aggressive.** `compression.threshold: 0.50`, `target_ratio: 0.20`, `protect_last_n: 20`.
6. **Memory bloat.** Char limits in config; prune via `skill_manage`.

### Hermes-specific prescriptions

| Symptom | Remedy |
|---|---|
| No personality / Claude defaults | Edit `~/.hermes/SOUL.md` (always loaded independently) |
| Forgets project rules | Add top-level `AGENTS.md` in project root |
| Invents skills it doesn't have | Add `requires_toolsets:` to SKILL.md frontmatter; or `hermes skills reset` |
| Loops / runs out of turns | Lower `agent.max_turns`; tune `compression.threshold` and `protect_last_n` |
| Mixes work/personal context | `hermes profile create work` → `work chat` |
| Dangerous commands | `approvals.mode: manual`; `tirith_fail_open: false` |

### Cross-system note

Hermes and OpenClaw converge on the same workspace pattern (SOUL.md / AGENTS.md / MEMORY.md / SKILL.md). A patient migrating between them mostly needs to translate config syntax (YAML vs JSON5), not rethink architecture. Diagnoses transfer with minor vocabulary swaps.

---

## v0.2 — MCP server is the universal delivery

20+ agent runtimes already support calling MCP servers (Claude Code, Cursor, Cline, Windsurf, Codex, Goose, Crush, Continue, NeMo Agent Toolkit, Letta, Google ADK, OpenAI Agents SDK, JetBrains, Zed, Claude Desktop, ChatGPT). Dr. Sigmund ships [`sigmund-mcp-server`](../../../sigmund-mcp-server/) — any MCP-capable agent calls Dr. Sigmund directly without per-runtime adapter.

Per-runtime adapters remain useful for the *body* of the lab (reading runtime-specific config + memory paths the MCP-isolated server can't see), so the MCP server's tools internally call the adapter library.

## Sources

- [agents.md governance](https://agents.md/) · [MCP clients matrix](https://modelcontextprotocol.io/clients)
- [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) · [docs.openclaw.ai](https://docs.openclaw.ai/) · [kaxo.io OpenClaw gotchas](https://kaxo.io/insights/openclaw-production-gotchas/)
- [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) · [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/)
- [github.com/qwibitai/nanoclaw](https://github.com/qwibitai/nanoclaw) · [docs.nvidia.com/nemo/agent-toolkit](https://docs.nvidia.com/nemo/agent-toolkit/latest/)
