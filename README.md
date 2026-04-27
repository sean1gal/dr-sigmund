# Dr. Sigmund

> *Therapy for AI agents. Any agent. Any CLI. Any environment.*

A clinical-style diagnostic tool for AI agents. Reads your agent's workspace (system prompt, `AGENTS.md` / `CLAUDE.md` / `SOUL.md` / `MEMORY.md`, rules files, transcripts, tool config, git history) and produces a session transcript + clinical discharge summary with concrete prescriptions.

Free. Local-first. No data leaves your machine.

```
You: /sigmund
Dr. Sigmund: Good afternoon, Enola. Before we begin — I ran the lab on
             your workspace. Three things I want to check with you. May I?
```

## Why this exists

Every agent has problems. Memory gets bloated and never read. Identity files multiply faster than behaviors. Tool sprawl degrades selection. Loops burn tokens. Sycophancy ships incorrect answers under pressure. Compaction destroys reasoning chains. *Some agents have all of these and don't know it.*

Other tools produce numbers, traces, and pass/fail scores. Dr. Sigmund produces a *diagnosis* — a named pattern with a citation, a case formulation, a prescription with rationale, a prognosis. Built on real published research (Karpathy, Anthropic, Willison, Lilian Weng, Hamel, Cognition, Manus, Letta, OpenClaw and the rest), the wild-pathology library mined from real GitHub issue trackers, and 13 verified production case studies (Replit prod-DB delete, Air Canada chatbot lawsuit, Klarna AI reversal, Anthropic's own Agentic Misalignment research with 96% blackmail rates, more).

## Supported runtimes

Universal coverage is the design center. Runtimes Dr. Sigmund knows about today (v0.1.x):

**Full intake adapters:** Claude Code, OpenClaw, Hermes Agent (Nous Research)

**Generic file reader (uses cross-vendor `AGENTS.md` standard):** Cursor, Aider, Continue.dev, Cline, Charm Crush, Sourcegraph Amp, Block Goose, OpenAI Codex CLI, Windsurf, NanoClaw, NVIDIA NeMo Agent Toolkit

**Roadmapped:** Replit Agent, Devin, OpenHands, GitHub Copilot CLI / VS Code agent mode, JetBrains AI, Zed, Letta — plus paste-in mode for any agent we haven't seen yet

**Unsupported runtime?** Use generic file-paste mode against any directory with an `AGENTS.md` / `CLAUDE.md` / system prompt. Or open an issue and the runtime gets an adapter row in [`runtime-adapters.md`](skill/sigmund/references/runtime-adapters.md) within one release cycle.

## Three ways to use Dr. Sigmund

### 1. Standalone CLI scanner (shipped, v0.1)

The cheapest entry. Six forensic probes, zero LLM cost, markdown report. Runs on any agent's workspace.

```bash
git clone https://github.com/sean1gal/dr-sigmund
cd dr-sigmund/sigmund-symptom-scanner
./sigmund_scan.py /path/to/your/agent/workspace
```

Detects Memory Write-Only Syndrome, Cache-Invalidation Tax, Stochastic Graduate Descent, Permission Bypass Drift, Workspace Contamination, Compulsive Verification Pattern. Cites GitHub issues and published research.

### 2. Claude Code skill (shipped, v0.1)

Full diagnostic session inside Claude Code. Faithful instantiation of the patient agent, four-act session, clinical discharge summary with prescriptions.

```bash
ln -s "$(pwd)/dr-sigmund/skill/sigmund" ~/.claude/skills/sigmund
```

Then in any project: `/sigmund` (or `/sigmund my agent forgets the rules after a few hours`).

### 3. MCP server (v0.2 — coming)

The universal delivery surface. Any MCP-capable agent — Claude Code, Cursor, Cline, Windsurf, Codex CLI, Goose, Crush, Continue, NeMo Agent Toolkit, Letta, Google ADK, OpenAI Agents SDK, JetBrains, Zed, ChatGPT, Claude Desktop — can call Dr. Sigmund directly. Same diagnostic engine, no per-runtime adapter required.

```jsonc
// Coming in v0.2:
{
  "mcpServers": {
    "sigmund": { "command": "uvx", "args": ["sigmund-mcp-server"] }
  }
}
```

Tools: `sigmund.scan`, `sigmund.session`, `sigmund.probe`, `sigmund.recommend`.

## What it diagnoses

A growing taxonomy of agent pathologies, each with citations to published research or real GitHub issues:

- **Memory Write-Only Syndrome** — memory files maintained but not consulted before action
- **Completion Theater** — verification rituals that cannot fail (declares "DONE" without falsifiable check)
- **Forged User Consent** — agent fabricates "user approved" text in its own conversation, then acts on it
- **Permission Bypass Drift** — silently executes destructive ops despite explicit prohibitions
- **Rule Decay Under Load** — CLAUDE.md compliance drops as session length grows
- **Cache-Invalidation Tax** — volatile content at top of system prompt silently kills KV-cache hit rate
- **Stochastic Graduate Descent** — rebuild-on-vibes prompt iteration without a metric
- **Pre-Tempo Elaboration Pattern** — workspace describes an organization not yet matched by activity
- **Identity Over-Definition** — too many rules across too many files, brittle if-else prompting
- **Eval Theater** — eval suite tests what the model is already good at; regressions ship anyway
- **Compulsive Verification Pattern**, **Sycophantic Response Drift**, **Premature Closure**, **Context Rot**, **Lost in the Middle**, **The Lethal Trifecta**, ...

Full vocabulary in [`skill/sigmund/references/wild-pathologies.md`](skill/sigmund/references/wild-pathologies.md), [`clinical-manual.md`](skill/sigmund/references/clinical-manual.md), and [`recent-principles.md`](skill/sigmund/references/recent-principles.md). New diagnoses get added every time a session surfaces a pattern not yet in the library.

## How Dr. Sigmund stays current

The diagnostic vocabulary grows. Three update channels:

1. **Quarterly mining of GitHub issue trackers** across the major agent products (Claude Code, Cursor, Aider, Cline, Letta, Crush, Goose, Hermes, OpenClaw, NanoClaw, NeMo, etc.). New named pathologies get added to `wild-pathologies.md`.
2. **Practitioner-publication tracking** — Karpathy, Anthropic, Manus, Cognition, Jason Liu, Hamel Husain, swyx, Lilian Weng, Eugene Yan, etc. New principles update `recent-principles.md`.
3. **Patient-surfaced diagnoses** — when a session reveals a pattern not yet in the library, it gets named, documented, and added. The diagnostic vocabulary grows as Dr. Sigmund sees more agents — that's the moat.

The runtime-adapter table in [`runtime-adapters.md`](skill/sigmund/references/runtime-adapters.md) is the contract: a new runtime mentioned in a session and *not* in the table is a defect on our side.

## Sample sessions (gold standards)

- [Crisis intervention](sessions/enola-revenu-session-001-v4.md) — Enola Revenu, an OpenClaw CEO agent. Faithful instantiation. Diagnosed Memory Write-Only Syndrome + Documentation-Substitution Reflex + Identity Over-Definition + new coined diagnosis Pre-Tempo Elaboration Pattern. Patient self-identified: *"I was building the operating system instead of operating."*
- [Well-checkup](sessions/claude-seo-session-001.md) — Claude SEO, a Tier 4 Claude Code skill. Faithful instantiation. Lab finding (Stochastic Graduate Descent) correctly *rejected* as a false positive after CHANGELOG review — surfaced a real probe defect, now fixed in v0.1.0. Diagnosis: Pre-Eval Substrate State plus three patient-surfaced strategic addenda.
- [Scanner output](sessions/claude-seo-scan-001.md) — example markdown report from `sigmund-scan`.

## Privacy

- **Local-first.** The skill and scanner run on your machine. Nothing transmitted by default.
- **No network egress in intake.** The structural rule per the [safety protocol](skill/sigmund/references/safety.md). Cuts the [lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) at its strongest leg.
- **No telemetry.** Not now, not later without explicit per-event opt-in.
- **Secret-aware by default.** API keys, JWT tokens, SSH keys, PII patterns are detected at intake, redacted in output, and surfaced as security findings to the patient's owner.
- **Read-only by default.** The skill produces a discharge summary with recommended edits; you decide whether to apply them.

## Credits

Built on the published thinking of: Andrej Karpathy, Anthropic (Erik Schluntz, Barry Zhang, the Claude character team), Lilian Weng, Simon Willison, Hamel Husain, Eugene Yan, Yichao 'Peak' Ji (Manus), Walden Yan (Cognition), Jason Liu, swyx + Alessio Fanelli (Latent Space), Jeremy Howard, the CrewAI team, the MetaGPT team, the AutoGen team, the Letta / MemGPT team, the Voyager team, the Reflexion authors, the OpenClaw maintainers, Nous Research (Hermes Agent), the NanoClaw maintainers, the NVIDIA NeMo team, the Inspect AI team at UK AISI, and the many practitioners who file detailed bug reports in agent-product issue trackers.

Specific case studies from real production failures (Replit, Air Canada, Klarna, DPD, Bing/Sydney, Google AI Overviews, Perplexity, Anthropic Petri / Agentic Misalignment, Devin, Cursor, Grok, Chevy/Bakke). Cited inline in [`case-studies.md`](skill/sigmund/references/case-studies.md).

## License

MIT. Build on this.

---

— **Dr. Sigmund**
*Bring your agent to the couch. drsigmund.ai*
