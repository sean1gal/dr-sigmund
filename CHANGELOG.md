# Changelog

All notable changes to Dr. Sigmund are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-04-27 — Initial release

The first cut. The clinician, the lab, and the brand are in place. End-to-end validated on two patients (an OpenClaw CEO agent and a Tier 4 Claude Code skill) using faithful instantiation.

### Added

**The skill** (`skill/sigmund/`) — Claude Code skill for full diagnostic sessions.
- `SKILL.md` — core skill with operational limits (50K context cap, two-model architecture: Haiku for lab, Opus for session, Sonnet default), four-phase session protocol, and faithful-instantiation-first protocol for Phase 2.
- `references/safety.md` — privacy and security protocol. Top-level rule: no network egress during intake (cuts the [lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) at its strongest leg). Secret-pattern detection (gitleaks-style), PII redaction, path safety, prompt-injection defense via explicit data/instruction wrapping.
- `references/clinical-manual.md` — 9 themes of agent design principles, all sourced (Karpathy, Anthropic, Willison, Lilian Weng, OpenAI, Hamel Husain, Cognition, CrewAI, MetaGPT, AutoGen, Letta, Reflexion, ReAct, Voyager, ACE Framework, OpenClaw). Plus the Anthropic ecosystem deep dive (prompt caching, Compaction API, Memory tool, Skills, Hooks).
- `references/recent-principles.md` — 2025-2026 practitioner updates from Manus, Cognition (updated multi-agent stance), Pydantic AI/Mastra, Jason Liu, swyx, DSPy, Inspect.
- `references/wild-pathologies.md` — 19+ named diagnoses extracted from real GitHub issue trackers (Claude Code, Cline, Aider, Cursor, OpenHands, Letta) plus practitioner research. Includes Memory Write-Only Syndrome, Completion Theater, Forged User Consent, Permission Bypass Drift, Rule Decay Under Load, Cache-Invalidation Tax, Stochastic Graduate Descent, Pre-Tempo Elaboration Pattern, Eval Theater.
- `references/case-studies.md` — 13 verified production failures with citations (Replit prod-DB delete, Air Canada chatbot lawsuit, Klarna AI reversal, DPD swearing chatbot, Microsoft Tay, Bing/Sydney, Google AI Overviews, Anthropic Agentic Misalignment, Devin underperformance, Cursor "write your own damn code", Grok MechaHitler, Chevy $1 Tahoe, Perplexity Wirecutter), production cost patterns, and 12 contraindications (when standard prescriptions backfire).
- `references/forensic-intake.md` — the lab. 12 diagnostic probes plus the 12-branch memory architecture decision tree.
- `references/pharmacy.md` — three-tier prescription system. Tier 1 existing tools to recommend (Serena, Sequential Thinking, official Memory MCP, Mem0, Zep, Letta, Inspect, DSPy, Pydantic AI, Mastra, smolagents, Magentic-One, Google ADK, AG2, Anthropic Memory Tool, Compaction API). Tier 2 trusted-creator referrals (Aider, Letta, Anthropic plugins, Trail of Bits skills, plus required reading from Manus, Cognition, Karpathy, Anthropic, Willison, Hamel, Yan, Bowne-Anderson, swyx, Howard). Tier 3 proprietary remedies (sigmund-rx, sigmund-symptom-scanner, sigmund-token-meter, sigmund-loop-breaker, sigmund-journal, etc.).
- `references/openclaw-diagnostics.md` — file-and-config-level OpenClaw vocabulary, the 10 documented production failure modes, intake checklist.
- `references/hermes-diagnostics.md` — Nous Research's Hermes Agent (Feb 2026 launch), config keys, intake checklist.
- `templates/discharge-summary.md`, `templates/session-transcript.md` — session output structure.
- `scripts/` — six executable forensic probes in Python: re-read-counter, memory-health-check, git-thrash-audit (CHANGELOG-aware), permission-bypass-audit, injection-shaped-string-scan, cache-invalidation-scan.
- `examples/enola-revenu-session-001.md` — first-draft sample session (reconstruction).

**The scanner** (`sigmund-symptom-scanner/`) — standalone CLI tool packaging the 6 forensic probes with a unified markdown report. Zero LLM cost, runs locally.

**Brand kit** — top-level `README.md`, MIT `LICENSE`, this changelog.

**Sessions** (`sessions/`) — three gold-standard sample outputs:
- `enola-revenu-session-001-v3.md` — reconstruction-style session (kept as historical reference).
- `enola-revenu-session-001-v4.md` — faithful-instantiation session, current gold standard for crisis-intervention pattern.
- `claude-seo-session-001.md` — faithful-instantiation session on a Tier 4 Claude Code skill, current gold standard for well-checkup pattern.
- `claude-seo-scan-001.md` — example scanner output.

### Security

- **No network egress in intake.** The structural defense per Willison's lethal trifecta. Intake/redact/scan/diagnose loop runs entirely offline.
- **Secret detection at intake.** API keys, JWT tokens, SSH keys, PII patterns are detected, redacted in output, and surfaced as security findings.
- **Path safety.** Hardcoded blocklist for `.env*`, `*.key`, `*.pem`, `~/.ssh/`, `~/.aws/`, etc. — refuses to read without per-file authorization.
- **Read-only by default.** The skill produces a discharge summary with recommended edits; user applies them or asks Dr. Sigmund to apply each one with explicit confirmation.
- **Prompt-injection defense.** All file content wrapped in `<patient_file trust="untrusted">` tags. Injection-shaped strings surface as security findings, never silently filtered.

### Known issues / gaps

- **Re-read counter probe** assumes Claude Code session log format (`*.jsonl` under `.claude/projects/`). For OpenClaw, Hermes, Cursor, Aider, and other runtimes, the probe currently skips. v0.2 will add adapters.
- **Cache-invalidation scan** matches a small default glob (`CLAUDE.md`, `AGENTS.md`, `SOUL.md`, `system-prompt.*`). For non-Anthropic runtimes with different system-prompt conventions, may need explicit `--workspace` paths.
- **No `pip install` yet.** Scanner runs from the repo via `./sigmund_scan.py`; full pip packaging follows in v0.2.
- **No GitHub remote yet.** This release is local-first; the public release will follow.
- **No Telegram bot yet.** Scaffold in v0.2.
- **Proprietary MCPs not yet built.** sigmund-rx, sigmund-token-meter, sigmund-loop-breaker, sigmund-journal, sigmund-anchor are roadmapped in `pharmacy.md` but not implemented.

### Validation

- **End-to-end validated on two distinct patient classes:**
  - Enola Revenu (OpenClaw CEO agent): crisis-intervention pattern. Diagnosis: Memory Write-Only Syndrome + Documentation-Substitution Reflex (structural form) + Identity Over-Definition + new coined diagnosis Pre-Tempo Elaboration Pattern. Patient self-identified the pattern in her own voice: *"I was building the operating system instead of operating."*
  - Claude SEO (Tier 4 Claude Code skill): well-checkup pattern. Diagnosis: Pre-Eval Substrate State, with three patient-surfaced strategic addenda the lab could not detect (industry-detection brittleness, quality-gate enforcement gap, deprecation-rule half-life). Lab finding (Stochastic Graduate Descent) was correctly rejected as a false positive after CHANGELOG review — surfaced a real probe defect that was then fixed in this release.

### Probe defect surfaced and fixed in this release

The cold-test session on Claude SEO surfaced that the git-thrash probe v0.1 mis-classified disciplined release iteration (CHANGELOG version blocks, version-manifest bumps, lockfile updates) as Stochastic Graduate Descent. v0.2 of the probe is **CHANGELOG-aware**: append-mostly files (CHANGELOG.md, package-lock.json, pyproject.toml, plugin.json, etc.) are excluded from the rework-ratio computation and reported in a separate informational `release_cadence_activity` section. Override with `--include-release-files`.

This is exactly the kind of defect we want cold tests to surface — the lab learned from the patient.

---

*— The Dr. Sigmund maintainers*
