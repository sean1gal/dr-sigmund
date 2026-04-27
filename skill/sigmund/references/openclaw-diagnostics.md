# OpenClaw Diagnostic Reference

Loaded by Dr. Sigmund when the patient is running on OpenClaw. Provides file-and-line-level diagnostic vocabulary so prescriptions can name actual config keys, file paths, and known failure modes.

---

## What OpenClaw is

A config-first, locally-run AI agent framework. A single **Gateway** process binds to local ports (typically `9090` and `18789`), watches `~/.openclaw/openclaw.json`, and orchestrates one or more **agents** — each an isolated brain with its own workspace, auth, model registry, and session store. Agents reach humans through a multi-channel inbox (Telegram, Discord, WhatsApp, Slack, Signal, iMessage, etc.) and can be confined in Docker sandboxes.

Sources: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw), [docs.openclaw.ai/gateway/configuration](https://docs.openclaw.ai/gateway/configuration).

---

## Workspace file convention

Default location: `~/.openclaw/workspace/` (or `~/.openclaw/workspace-<profile>` with profile override). All files are optional — when absent, a "missing marker" is injected so the agent knows the file isn't there.

| File | Purpose | Load order | If missing |
|---|---|---|---|
| **AGENTS.md** | Operating instructions, rules, priorities | Session start (early) | Missing marker injected |
| **SOUL.md** | Persona, tone, values | Always loaded first as persona | Bare-bones default seeded |
| **IDENTITY.md** | Agent name, vibe, emoji | Per bootstrap | Missing marker |
| **USER.md** | User identity, address preferences | Every session | Missing marker |
| **TOOLS.md** | Notes about local tools | Session start | Missing marker |
| **MEMORY.md** + `memory/` | Persistent curated memory; loaded **only in private sessions**, not group/shared | Session start | Missing marker; large files truncated |
| **HEARTBEAT.md** | Checklist for the periodic heartbeat tick | Per heartbeat fire | Heartbeat skipped if file is empty/headers-only |
| **ONBOARD.md** / **BOOTSTRAP.md** | One-time first-run ritual | Initial setup only | Auto-created on brand-new workspace |
| **skills/** | Workspace-specific skills, highest precedence | At skill resolution | Skipped in lookup |
| **canvas/** | Canvas UI files | UI rendering | Skipped |

Truncation defaults: `bootstrapMaxChars = 12,000` per file, `bootstrapTotalMaxChars = 60,000` total. ([agent-workspace.md](https://github.com/openclaw/openclaw/blob/main/docs/concepts/agent-workspace.md))

---

## openclaw.json schema (key fields)

Top-level: `agents`, `bindings`, `broadcast`, `canvasHost`, `channels`, `cron`, `discovery`, `env`, `gateway`, `hooks`, `identity`, `logging`, `mcp`, `messages`, `plugins`, `session`, `tools`, `ui`, `web`. Validation is strict Zod — unknown keys, malformed types, or invalid values cause Gateway to refuse to start.

```json5
{
  agents: {
    defaults: {
      heartbeat: { every: "30m", target: "...", directPolicy: "allow" },
      model: "anthropic/claude-sonnet-4-6",
      sandbox: { mode: "non-main", scope: "agent" },
      skills: [...],
      workspace: "~/.openclaw/workspace"
    },
    list: [
      { id: "main", default: true },
      { id: "work", workspace: "~/.openclaw/workspace-work" }
    ]
  },
  channels: {
    telegram: { enabled: true, botToken: "${TG}", dmPolicy: "pairing", allowFrom: [...] },
    slack: {...}, discord: {...}, whatsapp: {...}
  },
  bindings: [
    { agentId: "work", match: { channel: "whatsapp", peer: { kind: "direct", id: "+1555..." } } },
    { agentId: "main", match: { channel: "whatsapp" } }
  ],
  gateway: { mode: "local", port: 18789, auth: { token: "..." } },
  session: { dmScope: "per-channel-peer" }
}
```

Some settings are honored only at `agents.defaults` and silently ignored when set per-agent: **compaction, browser profiles, thinking**. This is a frequent footgun.

---

## Bootstrap protocol

At session start: load `AGENTS.md` and `TOOLS.md` (always), then `MEMORY.md` (only in private sessions, never subagent/group), then persona files. Heartbeat default is `30m` (`1h` if using Anthropic OAuth). Default DM scope is `per-sender`/`per-channel-peer`. Resets fire on `/new` or `/reset`. `skipBootstrap: true` disables auto-load.

---

## Memory model

Two layers. **MEMORY.md** is curated, bounded, intentionally short — read every private session. The **`memory/`** subdirectory holds daily logs (one file per day) loaded for context. Memory is excluded from subagent and shared/group sessions for privacy. Large files are truncated to bootstrap caps. Agents write via tool calls; humans can edit MEMORY.md directly.

---

## Heartbeat mechanics

A scheduled timer (not idle tick): every `agents.defaults.heartbeat.every` (default `30m`), the Gateway runs a full agent turn with a default prompt: *"Read HEARTBEAT.md if it exists. Follow it strictly. Do not infer or repeat old tasks. If nothing needs attention, reply HEARTBEAT_OK."*

If the main queue is busy → heartbeat is skipped and retried later.
If HEARTBEAT.md is empty (whitespace/headers only) → run is skipped to save tokens.
`directPolicy: "allow"` → heartbeat can send DMs; `"block"` → runs but suppresses outbound DMs.
([Heartbeat docs](https://openclaw-ai.com/en/docs/gateway/heartbeat))

---

## Multi-agent routing

**No router agent** — routing is fully deterministic via `bindings`. Each binding maps `(channel, accountId, peer, guildId, teamId) → agentId` with **most-specific wins**: peer match > parentPeer (thread inheritance) > guildId+roles > guildId > teamId > accountId > channel-level (`accountId: "*"`) > default agent. Multiple match fields = AND. **Tied tier? First in config order wins.** ([Multi-agent docs](https://docs.openclaw.ai/concepts/multi-agent))

Agents are isolated: separate workspace, auth profiles, model registry, session store at `~/.openclaw/agents/<agentId>/`.

---

## Sandbox model

- `off` — no sandboxing, agent runs on host
- `non-main` — main DM session runs on host; **subagents and cron jobs** run in isolated Docker
- `all` — every session, including main, runs inside Docker

`scope` controls container reuse (`session`/`agent`/`shared`). Containers can configure `network: "none"`, read-only root, CPU/memory limits. Setup requires `scripts/sandbox-setup.sh` to build the image first.

---

## Documented + community-known failure modes

Top recurring complaints from issues, troubleshooting docs, and Kaxo's "8 silent failures" writeup ([kaxo.io](https://kaxo.io/insights/openclaw-production-gotchas/)):

1. **Gateway won't start** — port conflict (`EADDRINUSE` on 9090/18789), or stale `~/.openclaw/gateway.pid` after crash
2. **Heartbeats silently die** — missing `models.json` in agent directory; no error logged
3. **Config drift across 4 model stores** — main config, session state, cron payloads, allowlist; cron keeps using the old model after a swap
4. **Gateway race overwrites edits** — Gateway holds in-memory state and clobbers files edited while running
5. **Agents rewrite their own configs** — produces nonexistent model names; fix with `chmod 444` on capabilities/skills, explicit prompt rules
6. **Upgrade drift** — `gateway.token` moved to `gateway.auth.token`; per-agent settings stop working; `openclaw doctor --fix` is mandatory after upgrade
7. **Hot reload silent failure** — invalid keys block reload with no error; some settings only honored at `agents.defaults`
8. **Telegram bot ignores group messages** — privacy mode is on by default
9. **Service runs but works manually** — env vars (API keys, `HOME`) not passed to systemd/launchd
10. **Heartbeats routed to local models** = silent failures; route to cheap reliable APIs

---

## Dr. Sigmund's OpenClaw intake checklist

When the patient is on OpenClaw:

1. **Run `openclaw doctor` first.** 90% of issues surface here.
2. **Check workspace files exist and have content.** `ls -la ~/.openclaw/workspace/` — missing markers vs. real content. Empty HEARTBEAT.md = skipped heartbeats. Missing `models.json` in agent dir = silent heartbeat death.
3. **Validate config schema:** `openclaw config validate`. If `.clobbered.*` files exist, the config was rejected and rolled back.
4. **Inspect bindings for ambiguity.** Competing bindings at the same specificity — first in config order wins; symptoms include "wrong agent answers in this group."
5. **Check sandbox mode vs. tool needs.** `non-main` blocks subagents from host filesystem/network — agents complaining "can't read my files" usually need scope adjustment.
6. **Per-agent vs. defaults scope check.** If a setting "isn't taking effect" on one agent, confirm it's not one of the `agents.defaults`-only settings (compaction, browser, thinking).
7. **Heartbeat health.** `openclaw cron status`. Empty HEARTBEAT.md? Routed to a local model? Anthropic OAuth (which forces `1h`)?
8. **Channel auth.** `openclaw channels status --probe --all`. Telegram bot with privacy mode in groups; expired Slack/WhatsApp OAuth.

---

## OpenClaw-specific prescriptions (file-and-line)

| Patient symptom | Specific remedy | Citation |
|---|---|---|
| Tool sprawl / wrong tool selection | Set `agents.<id>.skills: []` to disable, then explicitly re-add only the needed skill ids | [Configuration](https://docs.openclaw.ai/gateway/configuration) |
| Heartbeat fires but does nothing useful | Open `~/.openclaw/workspace/HEARTBEAT.md`; if it's headers-only, runs are skipped — write 3-5 explicit checks. Confirm `models.json` exists in the agent dir. | [Heartbeat](https://openclaw-ai.com/en/docs/gateway/heartbeat) |
| Wrong agent answers in this group | Audit `bindings`: most-specific wins, ties broken by config order. Add a `peer` or `guildId+roles` binding above the channel-level fallback. | [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent) |
| Subagent can't access my project files | Check `agents.defaults.sandbox.mode`: `non-main` puts subagents in Docker — move workdir into the mounted volume, switch to `mode: off`, or set `scope: shared`. | [Configuration](https://docs.openclaw.ai/gateway/configuration) |
| Telegram bot ignores group messages | Disable bot privacy mode via @BotFather (`/setprivacy` → Disable) | [Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting) |
| After upgrade everything is unauthorized | Run `openclaw doctor --fix`; `gateway.token` moved to `gateway.auth.token`; delete stale agent `auth.json` tokens, restart gateway, reconnect | [kaxo.io](https://kaxo.io/insights/openclaw-production-gotchas/) |
| Per-agent compaction/browser/thinking ignored | Move setting to `agents.defaults` — these keys are silently ignored when set per-agent | [Configuration](https://docs.openclaw.ai/gateway/configuration) |
| MEMORY.md not loaded in group chat | Expected behavior — privacy. Move shared facts into AGENTS.md or a per-channel context file. | [agent-workspace.md](https://github.com/openclaw/openclaw/blob/main/docs/concepts/agent-workspace.md) |

---

## Honest gaps

- LLM-based content routing is **not** shipped; [issue #13304](https://github.com/openclaw/openclaw/issues/13304) requests it but don't promise it to patients.
- The full machine-readable schema is published via `openclaw config schema` — for absolute fidelity Dr. Sigmund should advise the patient to run that command and diff against expected.
