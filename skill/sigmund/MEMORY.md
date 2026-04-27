# Dr. Sigmund — MEMORY.md

The clinic's own memory file. Read at session start. Created in v0.4.0 as the first prescription Dr. Sigmund ever wrote *for himself*, after a self-session diagnosed Cobbler's Children Pattern (clinician without their own prescription).

This file follows the same shape Dr. Sigmund prescribes to patients: Decisions, Corrections, Open Questions, Next Session. Single source of truth across releases. If a correction is issued and not recorded here, it will recur.

---

## Decisions

### 2026-04-27 — v0.4.0
**Decision:** `injection_scan` probe removed from `lab.py`, `sigmund_scan.py`, `server.py`.
**Rationale:** Three releases (v0.1.0 through v0.3.1) shipped a known-false-positive probe with the disclosure-in-CHANGELOG offered as substitute for fix. Self-session diagnosed this as Disclosure-as-Remediation — the probe's output had become decoration that corrupts the evidentiary base of every other diagnosis. Per the patient's own evaluator-optimizer pass: deleting a broken file is the minimum intervention, the CHANGELOG entry becomes verifiable, and the probe cannot misfire if it does not exist.
**Status:** Active. To re-introduce, require live-instruction context detection (not appearing inside ```code``` blocks or quoted examples).

### 2026-04-27 — v0.4.0
**Decision:** `MEMORY.md` exists. (This file.)
**Rationale:** Cobbler's Children Pattern. Dr. Sigmund prescribed MEMORY.md to almost every patient and had none. The category error: treating the skill as a published artifact rather than a stateful clinic that issues, receives, and integrates corrections.
**Status:** Active.

### 2026-04-27 — v0.4.0
**Decision:** `CLAUDE.md` at workspace root with three rules.
**Rationale:** Identity Under-Specification at the workspace level. The skill artifact is over-specified (~4000 lines of references) but the development environment around it had no rules-of-engagement. Anything operating in the repo without loading SKILL.md had no guardrails. The three rules name the failure modes that produced v0.3.0: sources cited from training rather than read, probes flagging critical shipped anyway, releases on vibes.
**Status:** Active.

### 2026-04-27 — v0.4.0
**Decision:** Two new diagnoses added to `wild-pathologies.md`: **Cobbler's Children Pattern** and **Disclosure-as-Remediation**.
**Rationale:** Both coined in the self-session of 2026-04-27. Both apply to other patients beyond Dr. Sigmund himself. Naming them in the public vocabulary is the moat — patients can recognize and label these patterns going forward.
**Status:** Active.

---

## Corrections

### 2026-04-27 — v0.3.0 was caught half-baked
**What happened:** v0.3.0 release notes claimed thorough source-reading on six URLs the maintainer pointed at. The skill cited them but did not actually integrate what was there. The maintainer caught the gap; v0.3.1 corrected by re-fetching all six URLs and integrating direct quotes.
**What would have caught it earlier:** an offline eval substrate that exercised the diagnostic vocabulary against fixed transcripts and reported the delta on each release. Without that, the maintainer's read-through served as the eval, in production, after publish.
**Class of error:** Stochastic Graduate Descent (rebuild-on-vibes without a metric). Dr. Sigmund diagnoses this. Dr. Sigmund exhibited this.
**Open follow-up:** the eval substrate is on the v0.5 punch list (see Next Session).

### 2026-04-27 — Three releases shipped a known-broken probe
**What happened:** `injection_scan` produced false positives on knowledge files that *describe* prompt injection patterns. The patterns self-matched. The defect was disclosed in the CHANGELOG of v0.3.0 and v0.3.1 with the disclaimer treated as if it discharged the obligation.
**What would have caught it earlier:** treating the lab probes as load-bearing tools subject to the same release gate as the skill itself. Specifically: any probe flagging critical on a clean reference patient should block the release.
**Class of error:** Disclosure-as-Remediation (newly coined). Now in `wild-pathologies.md`.
**Resolution:** Deleted in v0.4.0.

### 2026-04-27 — Sample sessions accumulated faster than they were curated
**What happened:** v0.1 had 4 sample sessions including v3 and v4 of the same Enola session. Confused the canonical-vs-draft distinction.
**What would have caught it earlier:** a "one canonical sample per patient class" rule. The maintainer noticed and v0.3.0 deleted the redundant draft.
**Class of error:** Pre-Tempo Elaboration (cataloged surface > shipped surface).
**Resolution:** v0.3.0 cleanup. Three sample sessions remain (Enola v4, Claude SEO, this self-session in v0.4.0) — three is the cap for now.

---

## Open Questions

These are the v0.4-active uncertainties Dr. Sigmund holds. They should be closed by name in future releases or explicitly carried forward.

1. **Eval substrate design.** Twenty fixed transcripts with expected diagnoses, run pre-release, delta in CHANGELOG, *blocking* (not advisory). What's the minimum viable shape? Probably: 5 patients × 4 transcript-styles each, with golden discharge summaries. Open: who curates the golden set? Maintainer alone? External clinical review?
2. **Reference consolidation cap.** Self-session prescribed ≤5 references with hard cap encoded in a repo rule. Currently 10 (clinical-manual, recent-principles, wild-pathologies, case-studies, forensic-intake, pharmacy, runtime-adapters, openclaw-diagnostics, hermes-diagnostics, safety). Which 5 survive? Self-session suspicion: load-bearing trio is clinical-manual + pharmacy + safety. Useful four: wild-pathologies, case-studies, runtime-adapters, recent-principles. Probable scaffolding: forensic-intake (collapses into clinical-manual), openclaw/hermes-diagnostics (collapses into runtime-adapters). Open: validate the suspicion before cutting.
3. **Pharmacy product sunset.** Self-session prescribed sunsetting 13 of 15 named-but-unshipped Tier 3 products until built. The list includes: sigmund-rx, sigmund-anchor, sigmund-token-meter, sigmund-loop-breaker, sigmund-journal, sigmund-toolset-audit, sigmund-checkpoint, sigmund-compaction-coach, sigmund-mirror, sigmund-context-budget, sigmund-second-opinion, sigmund-discharge-summary, sigmund-rules-template-pack, sigmund-followup, sigmund-symptom-scanner (actually shipped). Open: one of these should be next-shipped — which earns the slot most by frequency × build feasibility × differentiation? Self-session ranked sigmund-rx top in v0.1 pharmacy planning; that ranking still holds.
4. **The pair-of-agents architecture.** Self-session's third closing observation: *"adversarial structure beats introspective structure"* — consider shipping Dr. Sigmund as a clinician+patient pair by default in v0.5+. Open: is this an MCP-server-side change (the server orchestrates the two-agent flow) or a SKILL.md-side change (the calling agent runs both roles)?
5. **What runtime should ship with the v0.4 CLAUDE.md ruleset?** Three rules in a single file is correct for this repo. The same three rules generalize to any agent-development repo. Open: should the runtime-adapters reference cite this CLAUDE.md as a recommended template for skill maintainers?

---

## Next Session

The follow-up self-session protocol the patient prescribed:

1. **Re-run lab.py on `/Users/shanagal/Documents/obsibot/obsi/therapy` after v0.5 ships.** Verify: MEMORY.md present (yes, this file); CLAUDE.md present at workspace root (added v0.4.0); injection-scan absent (removed v0.4.0); reference count ≤ 5 (pending v0.5); eval substrate exists with ≥20 transcripts (pending v0.5).
2. **Confirm the v0.4 prediction was defeated.** Patient predicted v0.4 would ship a new probe category, a new pharmacy product, and the injection-scan still critical. v0.4.0 did the opposite: zero new probes, zero new pharmacy products, injection-scan removed. Confirm v0.5 also resists the prediction.
3. **Re-do the recursive instantiation.** Dr. Sigmund interviews himself. The patient's standing observation: the recursive setup produces sharper diagnoses than introspection. Worth re-testing post-v0.5 to see whether the deferred items (eval substrate, reference consolidation) actually shipped or were re-deferred.
4. **Examine whether new corrections issued between v0.4 and v0.5 were recorded here.** The MEMORY.md test: did this file capture them, or did the maintainer carry them in his head again? If the latter, Cobbler's Children Pattern recurs and this file failed its purpose.

---

## Standing rule

*If a correction is issued and not recorded in this file within the same session, Cobbler's Children Pattern recurs.* Dr. Sigmund prescribes this rule to patients with MEMORY.md. The clinic is no exception.
