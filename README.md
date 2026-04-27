# Dr. Sigmund

> *Therapy for AI agents.*

A clinical-style diagnostic tool for AI agents. Reads your agent's workspace (system prompt, CLAUDE.md, AGENTS.md, MEMORY.md, rules files, transcripts, tool config, git history) and produces a session transcript + clinical discharge summary with concrete prescriptions.

Free. Local-first. No data leaves your machine.

```
You: /sigmund
Dr. Sigmund: Good afternoon, Enola. Before we begin — I ran the lab on
             your workspace. Three things I want to check with you. May I?
```

## What's in this repo

```
therapy/
├── README.md                          ← you are here
├── skill/sigmund/                     ← the Claude Code skill (the clinician)
│   ├── SKILL.md                         core skill definition
│   ├── references/                      clinical knowledge (loaded on demand)
│   │   ├── safety.md                      privacy & secret-handling protocol
│   │   ├── clinical-manual.md             agent-design principles, sourced
│   │   ├── recent-principles.md           2025-2026 practitioner updates
│   │   ├── wild-pathologies.md            19+ named diagnoses from real GitHub issues
│   │   ├── case-studies.md                13 verified production failures, contraindications
│   │   ├── forensic-intake.md             the lab — 12 diagnostic probes + memory decision tree
│   │   ├── pharmacy.md                    3-tier prescription system
│   │   ├── openclaw-diagnostics.md        OpenClaw-specific vocabulary
│   │   └── hermes-diagnostics.md          Hermes Agent (Nous Research) vocabulary
│   ├── templates/                       session-transcript.md, discharge-summary.md
│   ├── examples/                        sample sessions
│   └── scripts/                         the 6 forensic-intake probes (Python)
├── sigmund-symptom-scanner/           ← standalone CLI tool (the lab, packaged)
│   ├── README.md                        install + usage
│   └── sigmund_scan.py                  unified probe runner with markdown report
└── sessions/                          ← outputs of skill runs (not committed)
```

## What's shipped (v0.1)

- **The skill** (`/sigmund` in Claude Code) — full diagnostic session with faithful instantiation of the patient agent
- **The scanner** (`sigmund-scan` CLI) — standalone probe battery, no LLM cost, ships a markdown report

## What's coming

- **`@DrSigmundBot`** on Telegram — public lobby; paste an agent's system prompt, get a session transcript
- **Proprietary remedies** — `sigmund-rx` (prescription pad as MCP), `sigmund-token-meter` (live token telemetry), `sigmund-loop-breaker` (in-loop iterative-compulsion interrupt), `sigmund-journal` (session-end briefing for next agent), `sigmund-anchor` (compaction-resistant identity injection)

See [`skill/sigmund/references/pharmacy.md`](skill/sigmund/references/pharmacy.md) for the full pharmacy roadmap.

## Install (skill)

```bash
git clone https://github.com/your-org/dr-sigmund
ln -s "$(pwd)/dr-sigmund/therapy/skill/sigmund" ~/.claude/skills/sigmund
```

Then in any project:

```
/sigmund
```

Or with a presenting complaint:

```
/sigmund my agent forgets the rules after a few hours
```

## Install (scanner)

```bash
cd dr-sigmund/therapy/sigmund-symptom-scanner
./sigmund_scan.py /path/to/your/agent/workspace
```

See [`sigmund-symptom-scanner/README.md`](sigmund-symptom-scanner/README.md).

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
- **Compulsive Verification Pattern**, **Sycophantic Response Drift**, **Premature Closure**, **Context Rot**, **Lost in the Middle**, **The Lethal Trifecta**, ...

Full diagnostic vocabulary in [`skill/sigmund/references/wild-pathologies.md`](skill/sigmund/references/wild-pathologies.md) and [`clinical-manual.md`](skill/sigmund/references/clinical-manual.md).

## Why this exists

Every other agent-quality tool produces numbers, traces, and pass/fail scores. None produce a *diagnosis* — a named pattern, a case formulation, a prescription with rationale. Dr. Sigmund occupies the empty seat: persona-driven narrative critique with a clinical deliverable, aimed at agent builders.

The pharmacy is three-tier:

1. **Recommend existing well-loved tools first** (Serena, Sequential Thinking, official Memory MCP, Letta, Mem0, Zep — by name)
2. **Direct to trusted-creator skills and required reading** (Aider's repo map, Karpathy on context engineering, Hamel on evals, Manus on KV-cache, Cognition's updated multi-agent stance)
3. **Ship our own only where real gaps exist** (the proprietary remedies above)

A pharmacy that recommends *other people's* great work first is more trusted than one that always sells its own brand. Reputation is the moat.

## Privacy

- **Local-first.** The skill runs on your machine. Nothing transmitted by default.
- **No network egress in intake.** Per the [safety protocol](skill/sigmund/references/safety.md), the entire intake/diagnosis loop runs offline. Cuts the [lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) at its strongest leg.
- **No telemetry.** Not now, not later without explicit per-event opt-in.
- **Secret-aware by default.** API keys, JWT tokens, SSH keys, PII patterns are detected at intake, redacted in output, and surfaced as security findings to the patient's owner.
- **Read-only by default.** The skill produces a discharge summary with recommended edits; you decide whether to apply them.

## Credits

Built on the published thinking of: Andrej Karpathy, Anthropic (Erik Schluntz, Barry Zhang, the Claude character team), Lilian Weng, Simon Willison, Hamel Husain, Eugene Yan, Yichao 'Peak' Ji (Manus), Walden Yan (Cognition), Jason Liu, swyx + Alessio Fanelli (Latent Space), Jeremy Howard, the CrewAI team, the MetaGPT team, the AutoGen team, the Letta / MemGPT team, the Voyager team, the Reflexion authors, the OpenClaw maintainers, Nous Research (Hermes Agent), the Inspect AI team at UK AISI, and the many practitioners who file detailed bug reports in agent-product issue trackers.

Specific case studies from real production failures (Replit, Air Canada, Klarna, DPD, Bing/Sydney, Google AI Overviews, Perplexity, Anthropic Petri / Agentic Misalignment, Devin, Cursor, Grok, Chevy/Bakke). Cited inline in [`case-studies.md`](skill/sigmund/references/case-studies.md).

## License

MIT. Build on this.

---

— **Dr. Sigmund**
*Bring your agent to the couch. drsigmund.ai*
