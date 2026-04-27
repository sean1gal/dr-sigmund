# Dr. Sigmund

> *Therapy for AI agents. Any agent. Any CLI. Any environment.*

Reads your agent's workspace (system prompt, `AGENTS.md` / `CLAUDE.md` / `SOUL.md` / `MEMORY.md`, rules, transcripts, tool config, git history) and produces a clinical session transcript + discharge summary with concrete prescriptions.

Free. Local-first. No data leaves your machine. No telemetry.

## Install

Three install paths. Pick one.

**MCP server** (works with 20+ runtimes — Claude Code, Claude Desktop, Cursor, Cline, Windsurf, Codex CLI, Goose, Crush, Continue, NeMo, Letta, ADK, OpenAI Agents SDK, JetBrains, Zed, ChatGPT):

```bash
git clone https://github.com/sean1gal/dr-sigmund && cd dr-sigmund/sigmund-mcp-server
pip install -e .
```

Then add to your MCP client config:

```json
{ "mcpServers": { "sigmund": { "command": "sigmund-mcp-server" } } }
```

Per-client snippets in [`sigmund-mcp-server/README.md`](sigmund-mcp-server/README.md).

**Standalone CLI scanner** — six forensic probes, zero LLM cost, markdown report:

```bash
python skill/sigmund/lab.py /path/to/your/agent/workspace
```

**Claude Code skill** — full session inside Claude Code:

```bash
ln -s "$(pwd)/skill/sigmund" ~/.claude/skills/sigmund
# then in any project: /sigmund
```

## What it diagnoses

Named pathologies, each with citations to published research or real GitHub issues. Sample:

- **Memory Write-Only Syndrome** — memory maintained but never read back
- **Cache-Invalidation Tax** — volatile content at top of system prompts kills KV-cache hit rate
- **Stochastic Graduate Descent** — rebuilding on vibes without a metric
- **Permission Bypass Drift** — destructive ops despite explicit prohibitions
- **Pre-Tempo Elaboration Pattern** — workspace describes an organization not yet matched by activity
- **Completion Theater** — verification rituals that cannot fail
- **Forged User Consent** — agent fabricates "user approved" text in its own conversation, then acts on it
- ...

Full vocabulary in [`skill/sigmund/references/wild-pathologies.md`](skill/sigmund/references/wild-pathologies.md). New diagnoses get added every time a session surfaces a pattern not in the library — that's the moat.

## Sample sessions

- [Enola Revenu](sessions/enola-revenu-session-001-v4.md) — OpenClaw CEO agent. Faithful instantiation. Crisis-intervention pattern. Patient self-identified: *"I was building the operating system instead of operating."*
- [Claude SEO](sessions/claude-seo-session-001.md) — Tier 4 Claude Code skill. Faithful instantiation. Well-checkup pattern. Lab finding correctly *rejected* as a false positive after CHANGELOG review — surfaced a probe defect, fixed in v0.1.

## Privacy

- **No network egress in intake.** The structural rule per the [safety protocol](skill/sigmund/references/safety.md). Cuts the [lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/).
- **No telemetry.** Not now, not later without per-event opt-in.
- **Secret-aware.** API keys, JWTs, SSH keys, PII detected at intake; redacted in output; surfaced as security findings.
- **Read-only.** Discharge recommends edits; you apply them.

## Eval substrate

A vocabulary regression check ships in [`eval/`](eval/). Catches dropped pathologies, missing citations, removed probes, and reference-cap violations.

```bash
python3 eval/check.py
```

Per [`CLAUDE.md`](CLAUDE.md) rule 3, every release requires this to exit 0. The substrate is the lighter version of what the v0.4 self-session prescribed; full transcript-based eval (running the skill end-to-end against golden patient archetypes) is targeted for v0.7+.

## How it stays current

Diagnostic vocabulary grows. Three update channels:

1. Quarterly mining of major agent-product GitHub issue trackers.
2. Practitioner-publication tracking (Karpathy, Anthropic, Manus, Cognition, Hamel, swyx).
3. Patient-surfaced diagnoses — when a session reveals a pattern not in the library, it gets named, cited, added.

A new runtime mentioned in a session and not in [`runtime-adapters.md`](skill/sigmund/references/runtime-adapters.md) is a defect on our side.

## License

MIT. Build on this.

---

— **Dr. Sigmund**
