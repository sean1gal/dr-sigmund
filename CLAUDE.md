# CLAUDE.md — workspace rules for the dr-sigmund repository

Loaded by Claude Code at the workspace root. Three rules, named, enforced.

## The three rules

### 1. Sources are read before cited

If a URL or paper appears in a Dr. Sigmund reference file as a citation — Karpathy, Anthropic, Manus, Cognition, Hamel, swyx, GitHub issues, anything — it must have been *fetched and read at integration time*, not paraphrased from training data. Direct quotes are required for any quoted material; the source URL must reach the actual quoted passage.

The mechanism: when adding or modifying a reference file with a citation, the citation is invalid until the source has been fetched (WebFetch in Claude Code) and a direct quote or specific structural claim from the source appears in the cite-adjacent text.

### 2. Probes flagging critical do not ship without remediation or removal

If `python skill/sigmund/lab.py <known-clean-patient>` returns a probe with `status: critical` on a workspace that should be clean, the release is blocked until the probe is fixed or removed. Disclosure in the CHANGELOG is **not** an acceptable substitute.

The mechanism: the dr-sigmund repository itself is the canonical "known-clean patient" for the probes. If the lab on this repo returns critical and the maintainer's hand has not been on a fix-or-remove keyboard within one session, the release does not ship.

### 3. Releases require an eval delta, not a vibe

A release is shipped only when the maintainer can answer, in the CHANGELOG, the question *"what changed in measurable diagnostic behavior between the prior release and this one?"* If the answer is *"sharper writing"* or *"more references"* without a measurable behavior change, the release is a documentation patch, not a v.X.Y bump.

The mechanism: when the eval substrate exists (open question on the v0.5 punch list — see [`skill/sigmund/MEMORY.md`](skill/sigmund/MEMORY.md)), every release CHANGELOG entry must include the delta against a fixed eval set. Until then, every release CHANGELOG entry must explicitly note the absence of an eval baseline as a known shipping risk.

## Three rules, hard cap

If a fourth rule is genuinely needed, it replaces an existing rule by amendment in this same file. Net rules count stays at three. The cap is structural, not aspirational — applied per Anthropic's *Building Effective Agents* Poka-yoke principle.

## When this file is wrong

If this CLAUDE.md grows a *"Note: rule 2 is sometimes hard to apply when..."* sub-bullet, the rule is being abandoned in slow motion. The corrective: amend the rule itself, or remove it. Don't accumulate exception language. (This is the Disclosure-as-Remediation tell applied recursively to this file.)

---

## Provenance (placed at bottom — KV-cache stable)

Created v0.4.0 as the first repo-root identity file the project has ever had. Per the self-session that surfaced Identity Under-Specification at the workspace level, the skill artifact was over-specified (~4000 lines of references) but the development environment around it had no rules-of-engagement.

Rule 1 exists because the v0.3.0 release cited six URLs the maintainer pointed at without actually reading them. v0.3.1 corrected by re-fetching all six. The corrective release within hours of the half-baked release is the audit trail.

Rule 2 exists because three releases (v0.1.0 through v0.3.1) shipped `injection_scan` flagging critical on knowledge files that *describe* injection patterns. The disclaimer was treated as if it discharged the obligation. The self-session that produced this CLAUDE.md named this **Disclosure-as-Remediation**; it is a published diagnosis in `wild-pathologies.md`. The probe was removed in v0.4.0 as the first action after the session.

Rule 3 exists because four releases shipped on the same day with no offline eval suite. The maintainer's read-through served as the eval, in production, after publish. The self-session named this **Stochastic Graduate Descent** — Dr. Sigmund's own diagnosis applied to himself.

This provenance section is intentionally below the rules (and below the meta-rule about exception language) because a CLAUDE.md is loaded by Claude Code on every session start and the stable prefix matters for KV-cache hit rate (per Manus, the single most important production-stage metric). Volatile content — historical references with dates — goes at the bottom. The rules themselves stay at top, prefix-stable.
