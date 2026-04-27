# Sigmund Symptom Scanner

> *Bring your agent to the couch.*

The first product from Dr. Sigmund's pharmacy. A forensic intake battery for AI agents — one command, real findings, no LLM cost.

## What it does

Scans an agent's workspace (system prompts, memory files, rules files, git history) for evidence of common pathologies that Dr. Sigmund diagnoses in full sessions:

- **Memory Write-Only Syndrome** — memory files maintained but never consulted
- **Identity Over-Definition** — too many rules, restated across too many files
- **Cache-Invalidation Tax** — volatile content at the top of system prompts that silently kills KV-cache hit rate (per [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus): "the single most important metric for a production-stage AI agent")
- **Permission Bypass Drift** — destructive operations in git history despite explicit prohibitions in CLAUDE.md/AGENTS.md
- **Workspace Contamination** — prompt-injection-shaped strings inside files the agent reads
- **Stochastic Graduate Descent / Vibe-Coding Rot** — git thrash patterns that suggest rebuild-on-vibes development

Every probe is a deterministic Python script. Zero LLM calls. Runs locally. No data leaves your machine.

## Install

```bash
git clone https://github.com/your-org/dr-sigmund
cd dr-sigmund/therapy/sigmund-symptom-scanner
chmod +x sigmund_scan.py
```

(A `pip install sigmund-symptom-scanner` will follow once we cut the v0.1 release.)

## Usage

```bash
# Scan an agent workspace (your project directory, an OpenClaw workspace, etc.)
./sigmund_scan.py /path/to/your/agent/workspace

# Save the report to a file
./sigmund_scan.py /path/to/workspace --output report.md

# Run a single probe
./sigmund_scan.py /path/to/workspace --probe memory
./sigmund_scan.py /path/to/workspace --probe git
./sigmund_scan.py /path/to/workspace --probe cache
```

## What you get

A markdown report with:

- **Summary table** — every probe, its status (ok / warning / critical), what it treats
- **Detailed findings** — YAML output of each probe, including specific files and line numbers
- **Suggested diagnoses** — the named pathologies that match the evidence (Compulsive Verification Pattern, Memory Write-Only Syndrome, etc.)
- **Prescription seeds** — concrete fixes (file edits, MCP recommendations, required reading)

The report is the artifact you share. Screenshot-friendly, evidence-grounded, citable.

## What this is not

This is *evidence*, not a diagnosis. The full diagnosis — named pathology, case formulation, integrated prescription, prognosis — requires a Dr. Sigmund session. Sigmund Symptom Scanner is the lab; Dr. Sigmund is the clinician. They work together.

If you want the full session, install the [Dr. Sigmund skill](../skill/sigmund/) into Claude Code and run `/sigmund` from your agent's workspace.

## Probes

| Probe | Detects | Cost |
|---|---|---|
| `memory` | Bloat, staleness, duplicate files, write-only patterns | ~10ms |
| `git` | Rework patterns, completion theater, low/high churn | ~100ms (depends on repo size) |
| `permissions` | CLAUDE.md / AGENTS.md prohibitions violated in git history | ~200ms |
| `injection` | Prompt-injection-shaped strings in workspace files | ~50ms |
| `cache` | Volatile content in system prompt prefixes (timestamps, dynamic dates) | ~10ms |
| `rereads` | Repeated Read tool calls in Claude Code session logs | ~200ms |

Total scan time on a typical workspace: under 2 seconds.

## Privacy

- **Local-only.** Nothing leaves your machine.
- **No telemetry.** Not in v0.1, not later. If we ever want metrics, it'll be opt-in with explicit per-event consent.
- **Read-only.** The scanner does not modify your workspace files. It produces a report; you decide what to do with it.
- **Secret-aware.** Per Dr. Sigmund's [safety protocol](../skill/sigmund/references/safety.md), the scanner refuses to read `.env`, `*.key`, `*.pem`, `~/.ssh`, `~/.aws`, and similar paths without explicit per-file authorization. Findings are scrubbed of any high-entropy secret patterns before output.

## License

MIT. Build on this.

## Source of authority

Probes are grounded in published agent-design research:
- **Memory Write-Only Syndrome** — [`anthropics/claude-code#52965`](https://github.com/anthropics/claude-code/issues/52965)
- **Cache-Invalidation Tax** — [Manus, "Context Engineering for AI Agents"](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- **Identity Over-Definition** — [Anthropic, "Effective context engineering for AI agents"](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **Stochastic Graduate Descent** — [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- **The Lethal Trifecta** (security model) — [Simon Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)

Full clinical reference: [`therapy/skill/sigmund/references/clinical-manual.md`](../skill/sigmund/references/clinical-manual.md).

---

— **Dr. Sigmund**
*Bring your agent to the couch. drsigmund.ai*
