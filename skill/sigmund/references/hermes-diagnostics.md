# Hermes Diagnostic Reference

Loaded by Dr. Sigmund when the patient is running on Hermes Agent. Provides file-and-config-level diagnostic vocabulary.

---

## Disambiguation

The dominant "Hermes" in the agent-builder world: **Hermes Agent by Nous Research**, released February 2026. Self-hostable autonomous agent with persistent memory and self-improving skills. ([github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent), [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/))

Distinct from but related to the **Nous Hermes LLM family** (Hermes 3, Hermes 4 fine-tunes of Llama/Qwen) which the agent can use as its underlying model. Other "Hermes" projects exist but none have comparable mindshare. **All Dr. Sigmund's Hermes-flavored advice should assume the Nous Research agent unless explicitly stated otherwise.**

---

## Architecture overview

Same shape as OpenClaw, different vocabulary. Single Python install (`uv`-based), gateway process, multi-channel messaging (Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, Email, SMS, DingTalk, Feishu, WeCom, BlueBubbles, Home Assistant). State lives in `~/.hermes/`.

```
~/.hermes/
├── config.yaml      # main settings (YAML, not JSON)
├── .env             # API keys / secrets
├── auth.json        # OAuth credentials
├── SOUL.md          # persona — first thing in system prompt
├── memories/        # MEMORY.md + USER.md
├── skills/          # SKILL.md-defined skills
├── cron/            # scheduled jobs
├── sessions/        # gateway session state
└── logs/
```

---

## Context file priority order

Loaded into prompt: `.hermes.md`/`HERMES.md` → `AGENTS.md` (hierarchical — top-level loaded at session start, subdir AGENTS.md discovered lazily during tool calls) → `CLAUDE.md` → `.cursorrules` → `.cursor/rules/*.mdc`.

**SOUL.md is always loaded independently** as the persona layer.

This means Hermes naturally inherits Cursor and Claude Code rules files — useful when migrating an agent in.

---

## Skills system

Progressive disclosure:
- **Level 0** (~3k tokens) — list of all skills
- **Level 1** — full SKILL.md content when needed
- **Level 2** — specific reference files

SKILL.md uses YAML frontmatter (`name`, `description`, `version`, `platforms`, `requires_toolsets`, `fallback_for_toolsets`). **Compatible with the [agentskills.io](https://agentskills.io) open standard** — skills are portable between Hermes and Claude Code.

The agent autonomously creates skills via the `skill_manage` tool after complex workflows (5+ tool calls), errors, or non-trivial pattern discovery. Skills live in `~/.hermes/skills/<category>/<name>/` with `references/`, `templates/`, `scripts/`, `assets/` subdirs.

---

## Memory model

Bounded by char limits in `config.yaml`:
- `memory_char_limit: 2200` (~800 tokens)
- `user_char_limit: 1375` (~500 tokens)

FTS5 full-text-search across past sessions with LLM summarization for cross-session recall, plus Honcho dialectic user modeling.

---

## Terminal backends (sandbox)

`local | docker | ssh | modal | daytona | singularity` — six options.

- Docker: full container resource controls (`container_cpu`, `container_memory`, `container_disk`, `container_persistent`)
- Daytona/Modal: hibernate when idle (serverless persistence)
- SSH: remote execution
- Singularity: HPC environments
- Local: no sandbox

---

## Multi-agent

Two mechanisms:

**Profiles** — `hermes profile create coder` → `coder chat`. Each profile is its own `HERMES_HOME` with isolated config/memory/skills/sessions. This is how you cleanly separate work/personal/regulated agents.

**Delegation/subagents** — `delegation.max_concurrent_children: 3`, `max_spawn_depth: 1`. Spawns isolated subagents on parallel workstreams within a single profile.

---

## Approvals & security

- `approvals.mode: manual | smart | off` — controls human-in-the-loop frequency
- `tirith_enabled: true` — command pre-execution scanner
- `tirith_fail_open: true` — defaults to permissive on scanner failure (set to `false` for strict)
- `redact_secrets: true` — strips secrets from logs
- `website_blocklist` — domain denylist

---

## Dr. Sigmund's Hermes intake checklist

1. **Identify the layer that's wrong:** SOUL.md (persona) vs. AGENTS.md (project rules) vs. MEMORY.md (long-term facts) vs. SKILL.md (procedure). Patients confuse these constantly.
2. **Check `~/.hermes/config.yaml` for:**
   - `agent.max_turns` (default 90 — runaway loops)
   - `agent.reasoning_effort` (empty = inherit)
   - `terminal.backend` (host vs. container mismatch)
3. **Profile pollution.** If symptoms differ across `hermes -p X chat` vs. `hermes -p Y chat`, you have profile drift — each has its own SOUL/MEMORY/skills.
4. **Skills not appearing.** Check `requires_toolsets`/`fallback_for_toolsets` in SKILL.md frontmatter and `platforms:` restriction; check `external_dirs` under `skills:` in config.yaml.
5. **Compression too aggressive / context loss.** `compression.threshold: 0.50`, `target_ratio: 0.20`, `protect_last_n: 20` — tune these.
6. **Gateway not responding.** `hermes gateway status`; `pip install "hermes-agent[telegram]"` if platform extras missing; foreground via `hermes gateway run` for WSL.
7. **Tool blocked as dangerous.** Intentional — adjust `approvals.mode` or the `tirith` security policy, don't disable wholesale.
8. **Memory bloat.** Check `memory_char_limit`/`user_char_limit`; have the agent prune via `skill_manage` rather than appending forever.

---

## Hermes-specific prescriptions

| Patient symptom | Specific remedy | Citation |
|---|---|---|
| No personality / repeats Claude defaults | Edit `~/.hermes/SOUL.md`; SOUL.md is the first thing in the system prompt and is always loaded independent of context-file precedence | [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality) |
| Forgets project rules across sessions | Add a top-level `AGENTS.md` in the project root — Hermes loads it at session start; subdir AGENTS.md files load lazily into tool results | [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration/) |
| Invents skills it doesn't have | Inspect `~/.hermes/skills/`; add `requires_toolsets:` to SKILL.md frontmatter so skills hide when tools are missing; or run `hermes skills reset` to restore bundled set | [Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) |
| Loops / runs out of turns | Lower `agent.max_turns` from 90 in `config.yaml`; tune `compression.threshold: 0.50` and `protect_last_n: 20` so older context compresses before the loop | [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration/) |
| Mixes work and personal context | Use profiles: `hermes profile create work` → `work chat`. Each profile gets its own `HERMES_HOME` with separate SOUL/memories/skills/sessions | [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) |
| Runs dangerous commands / over-approves | Set `approvals.mode: manual` in config.yaml; verify `security.tirith_enabled: true` and `tirith_fail_open: false` | [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration/) |

---

## Cross-system note

Hermes and OpenClaw converge on the same workspace pattern (SOUL.md / AGENTS.md / MEMORY.md / SKILL.md). A patient migrating between them mostly needs to translate config syntax (YAML vs JSON5), not rethink architecture. Dr. Sigmund's diagnoses transfer between the two systems with minor vocabulary swaps.
