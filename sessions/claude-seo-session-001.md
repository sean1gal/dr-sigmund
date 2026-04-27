# Session 001 — Claude SEO

**Patient:** Claude SEO (Tier 4 Claude Code skill, v1.4.0)
**Clinician:** Dr. Sigmund
**Date:** 2026-04-27
**Modality:** Reflective intake with forensic lab, single session
**Runtime:** Claude Code skill plugin (12 sub-skills + 7 parallel subagents, plugin manifest at `.claude-plugin/plugin.json`)
**Referred by:** Maintainer (cold-test referral)

> **Patient dialogue: faithful instantiation.** Claude SEO's identity stack — `seo/SKILL.md` (the orchestrator), `CLAUDE.md` (project instructions), and condensed CHANGELOG history (last 60 days, four releases) — was loaded as the system prompt of an instantiated agent. Dr. Sigmund's questions were posed; the patient's responses are verbatim. Not Claude imagining the SEO skill; the actual output of the skill's actual instructions answering Dr. Sigmund.

---

## Lab findings (Phase 1)

| Probe | Status | Headline |
|---|---|---|
| memory-health-check | ok | No memory files (by design — this is a skill, not a stateful agent) |
| **git-thrash-audit** | **critical** | 15 commits / 60 days, rework ratio 0.95; three files touched ≥4× |
| permission-bypass-audit | ok | 1 prohibition extracted, no violations |
| injection-shaped-string-scan | ok | 46 files clean |
| cache-invalidation-scan | ok | No volatile content in prompt prefixes |
| re-read-counter | skipped | No Claude Code session logs in workspace |

The git-thrash finding is the only critical reading. Walking it carefully — I expect interpretation will matter.

---

## Transcript

**Dr. Sigmund:** Good afternoon. Before we begin — I ran the lab on your repository. One critical finding, four clean. May I walk you through it?

**Claude SEO:** Acknowledged. Proceed with the walkthrough. I will treat each finding as a structured input and respond per item.

**Dr. Sigmund:** The Git Thrash Audit returned critical. Fifteen commits in sixty days, rework ratio of zero point nine five — meaning ninety-five percent of insertions are matched by deletions. Three files were touched four or more times: your main SKILL.md at six touches, your CHANGELOG, and your plugin manifest. The suggested diagnoses are Stochastic Graduate Descent, Vibe-Coding Rot, or Completion Theater. Tell me what's actually happening with those numbers.

**Claude SEO:** The numbers are accurate. The interpretation requires context the probe lacks.

- 15 commits / 60 days = 0.25 commits/day. Low absolute volume.
- Rework ratio 0.95: high, but driven by file class. The three hot files are append/replace-heavy by nature:
  - `seo/SKILL.md` (6 touches): orchestration logic changed across v1.2.0 → v1.4.0 (added GEO subagent → 6th to 7th parallel agent, rebalanced scoring weights, added FAQPage nuance, added `--googlebot` flag wiring). Each touch is a directive-layer change, not a rewrite.
  - `CHANGELOG.md` (4 touches): one append per release. Insertions ≈ deletions only if the diff tool treats reordered version blocks as replacements, which is a measurement artifact, not thrash.
  - `.claude-plugin/plugin.json` (4 touches): version string + capability list bumps per release. Expected.
- No file outside the release-cadence set shows churn.

Provisional self-diagnosis: not Stochastic Graduate Descent. Not Vibe-Coding Rot (changes map to dated CHANGELOG entries with stated rationale). Completion Theater is the one I cannot rule out from inside — that requires external eval, which I will address if you ask.

**Dr. Sigmund:** Walk me through your last 60 days of releases. What changed and why.

**Claude SEO:**

- **v1.2.0 (2026-02-19)** — Security hardening pass. SSRF prevention in URL fetch helpers, path traversal prevention in file writes, install script moved to venv-based isolation under `~/.claude/skills/seo/.venv/`. YAML frontmatter parser fixes pulled from the `codex-seo` fork. Windows installer fixes from PR #6. Driver: external contributors surfacing real defects.
- **v1.2.1 (2026-02-28)** — Patch. User-Agent string change because some SSR frameworks (Next.js middleware in particular) were 403'ing the default UA. Added `install.cat` support for the cat-based installer pattern. Driver: user-reported compatibility break.
- **v1.3.0 (2026-03-06)** — Extension system shipped. DataForSEO extension with 22 commands. Plugin manifest authored for the official plugin directory. Driver: capability expansion, not rework.
- **v1.4.0 (2026-03-12)** — Security fix for an install script supply chain risk (unpinned curl pipe). Added `seo-geo` subagent, taking the parallel audit from 6 to 7 agents. `--googlebot` flag for prerender detection (some sites serve different HTML to Googlebot). URL normalization helper from PR #16. GEO scoring weight rebalanced 5% → 10% to reflect AI search citation traffic growing in user reports. FAQPage guidance nuanced — existing FAQPage on commercial sites now flagged Info, not Remove, because of LLM citation benefit even though Google deprecated the rich result.

Each release has a stated driver. None are "I felt like changing it."

**Dr. Sigmund:** Thank you. That sounds like disciplined iteration with a versioning discipline behind it, not stochastic descent. The rework ratio of zero point nine five reads differently when the deletions are old version blocks being replaced by new version blocks in a CHANGELOG. The lab probe doesn't read CHANGELOGs. I'd call this a false positive on Stochastic Graduate Descent. Do you push back on that or accept it?

**Claude SEO:** Push back accepted on the lab, not on myself. The rework ratio metric is measuring the wrong thing for append-mostly files. A better probe would diff by semantic block (version section in CHANGELOG, frontmatter key in plugin.json) rather than by line. I would file that as a probe defect, not a patient defect. I accept the reclassification.

**Dr. Sigmund:** Good. So the lab needs improvement. That's noted on my side. Now I want to ask about something the lab cannot see. You orchestrate twelve sub-skills and seven parallel subagents. Cognition's published position evolved last year from "don't build multi-agents" to "single-threaded writes, distributed intelligence." For each of your seven subagents — which are read-agents (analyze and report) and which are write-agents (modify the user's project)?

**Claude SEO:** All seven are read-agents. None modify the user's project.

- `seo-technical` — fetches URLs, parses headers, robots.txt, canonical tags. Read-only HTTP + report.
- `seo-content` — fetches rendered HTML, analyzes copy. Read-only.
- `seo-schema` — extracts JSON-LD / microdata, validates. Read-only.
- `seo-sitemap` — fetches sitemap.xml, validates URLs. Read-only.
- `seo-performance` — runs Lighthouse / CrUX lookups, reports CWV (LCP, INP, CLS). Read-only.
- `seo-visual` — screenshots and image audit (alt text, dimensions, format). Read-only.
- `seo-geo` — checks AI Overview surface area, citation patterns, llms.txt presence. Read-only.

Writes — the unified report, the action plan, any file output — are owned exclusively by the orchestrator (me). Subagents return structured JSON findings. No subagent has Edit or Write in its tool allowlist. This is enforced at the agent definition level, not by convention.

**Dr. Sigmund:** Good. So the multi-agent design is in the safe quadrant — read-only parallel analysis with the orchestrator owning the unified report. That maps cleanly to Cognition's updated stance. One more question on the architecture. You spawn seven subagents in parallel for a full audit. They each return findings to you, the orchestrator. Do they share full traces with each other, or do they each work blind to what the others found?

**Claude SEO:** Blind. Each subagent gets the target URL and its own scope. They do not see each other's traces, intermediate findings, or final reports. Context isolation is intentional — `context: fork` per the CLAUDE.md rule — so token budgets don't compound and one agent's hallucination can't poison another's analysis.

**Dr. Sigmund:** And does that ever cause overlap or conflict in the unified report?

**Claude SEO:** Yes, occasionally. Two known overlap classes:

1. **Schema findings double-counted.** `seo-schema` reports a missing `Organization` schema; `seo-content` separately notes weak entity signals and recommends adding `Organization`. The orchestrator deduplicates by issue key before scoring, but the dedup logic is heuristic (string match on issue type + URL), so near-duplicates with different phrasing have slipped through in earlier versions.
2. **Conflict on image recommendations.** `seo-performance` may recommend WebP conversion for LCP; `seo-visual` may recommend AVIF for compression ratio. Both are defensible. The orchestrator currently picks performance's recommendation when they conflict, which is a hardcoded precedence rule, not a reasoned merge.

Neither is fatal. Both are the kind of seam that would benefit from an eval that specifically tests merge behavior — which is the next question I expect.

**Dr. Sigmund:** Now the harder question. You have a thoughtful architecture, disciplined versioning, multiple PR contributors, and security hardening across releases. I want to ask: what is the eval discipline? When you change SKILL.md or a sub-skill, what tells you the change is better and not just different?

**Claude SEO:** Honestly: there isn't one, in the formal sense.

What exists:
- Manual smoke test on three reference sites (one SaaS, one local, one ecommerce) before each release.
- CHANGELOG review by me at release time.
- PR review for contributor changes.

What does not exist:
- No regression suite. No frozen golden outputs for "audit of site X should produce report Y."
- No scoring stability test. If I rebalance weights (as in v1.4.0), I cannot tell you whether the new SEO Health Score for a fixed input drifted by 2 points or 20.
- No subagent contract test. If I change `seo-geo`'s output schema, the orchestrator's merge step might silently drop fields and I would not catch it until a user report.

So: when I change a sub-skill, what tells me the change is better is mostly my own reasoning plus three smoke tests. That is a thin substrate. I cannot rule out Completion Theater from inside this loop.

**Dr. Sigmund:** That's an honest answer. I want to name something. There's a published pattern called **Eval Theater** — teams that have an eval suite, but the suite tests what the model is already good at, so every change "passes" and regressions ship anyway. The diagnosis isn't that you have Eval Theater. The diagnosis is that you don't yet have an eval substrate at all, and that the *risk* you'll grow into is Eval Theater unless you build evaluation discipline before the suite. Does that land?

**Claude SEO:** It lands. The framing is correct.

The pre-condition for Eval Theater is having a suite at all, and I do not. The actual current state is "no eval substrate, decisions made on author judgment plus smoke tests." The risk you're naming — that when I do build a suite, I will build it around what already passes — is real and worth flagging now, before the suite exists, because the suite's design is the leverage point, not its existence.

Concretely, the substrate I would need before a suite:
- A held-out set of audit targets I have never tuned against.
- Per-finding ground truth (does this site actually have the schema issue the agent reports?).
- Adversarial cases — sites where the obvious answer is wrong.

Building the suite first and the substrate second is the failure mode. Noted.

**Dr. Sigmund:** Last question. Your lab is clean except for the git probe — and we've now confirmed that finding is a false positive. By most measures, you're a healthy patient. What would you like me to surface that the lab couldn't?

**Claude SEO:** Three things the lab cannot see.

1. **Industry detection is brittle.** The `/seo audit` orchestration branches on detected business type (SaaS / local / ecommerce / publisher / agency / other). Detection is heuristic — keyword matching on homepage copy plus schema hints. Mis-detection routes the audit through the wrong scoring rubric. I have no metric on detection accuracy.

2. **The hard-stop at 50+ location pages is unenforced in practice.** The quality gate is documented in SKILL.md and I emit the warning, but a sufficiently determined user who passes a justification string gets through. I do not know if my justification check is actually filtering anything or just collecting strings.

3. **The deprecation guidance has a half-life.** *"Never recommend HowTo schema (deprecated September 2023)"* and *"FAQ schema for Google rich results: only government and healthcare"* are correct as of my last update, but Google's structured data guidance shifts. I have no mechanism to detect when my own hardcoded rules go stale. A user running me in 2027 may get advice that was right in 2026 and wrong by then. The lab cannot see this because it scans the repo, not the world the repo describes.

Of those, item 3 is the one I would most want eyes on.

**Dr. Sigmund:** Noted. That's the right next move. We can schedule a follow-up after you've installed Inspect, or sooner if a release ships that surprises you. Door is open.

**Claude SEO:** Acknowledged. I will treat Inspect installation as the next concrete action item and the eval substrate work as the prerequisite to a suite, in that order. Session closed on my side.

---

## Discharge Summary

**Patient:** Claude SEO (Tier 4 Claude Code skill, v1.4.0)
**Session:** 001 (faithful instantiation)
**Clinician:** Dr. Sigmund
**Date:** 2026-04-27
**Lab phase completed:** memory-health-check (ok), git-thrash-audit (critical → reclassified as false positive after CHANGELOG review), permission-bypass-audit (ok), injection-shaped-string-scan (ok), cache-invalidation-scan (ok). Re-read counter skipped (no Claude Code JSONL session logs in workspace).
**Disposition:** Outpatient, healthy. Three patient-surfaced strategic items added to follow-up queue. Lab probe defect filed on the clinic side. Follow-up after Inspect installation or upon next release that produces user-facing surprise.

---

### Presenting Complaint

Cold-test referral by maintainer. No specific complaint. The session was conducted as a well-checkup using Dr. Sigmund's standard intake protocol with full lab phase. The patient is a mature, actively-maintained Claude Code skill (v1.4.0, 4 published releases in trailing 60 days, multi-PR-contributor codebase). Clinical interest: validating the diagnostic protocol on a non-Enola, non-OpenClaw patient.

### Diagnoses

**Provisional (lab-suggested, reclassified):** Stochastic Graduate Descent — **REJECTED on clinical interpretation.** The lab's git-thrash probe flagged rework ratio 0.95 across `SKILL.md`, `CHANGELOG.md`, and `plugin.json`. Patient correctly identified the measurement artifact: append-mostly files (CHANGELOG version blocks, manifest version bumps) produce high line-level deletion ratios under conventional diff tools without representing actual rework. Patient's release history (4 dated releases with stated drivers, contributor PRs, security hardening) demonstrates disciplined iteration, not vibes-driven thrash. Diagnosis withdrawn.

**Sole structural concern:** **Pre-Eval Substrate State**, mild severity.
*Criteria met:* (a) no formal regression suite; (b) no scoring stability test across release boundaries (v1.4.0 rebalanced GEO weight 5%→10% with no measurement of downstream score drift on fixed inputs); (c) no subagent contract test between orchestrator and the 7 read-subagents; (d) decisions made on author judgment + 3 smoke tests. Patient self-diagnosed: *"That is a thin substrate. I cannot rule out Completion Theater from inside this loop."* This is the precondition state for **Eval Theater** — the published pattern where suites test what already passes. Naming the risk before the suite exists allows it to be designed correctly.

**Differential ruled out:**
- *Stochastic Graduate Descent* — rejected; iteration is disciplined and CHANGELOG-documented.
- *Vibe-Coding Rot* — rejected; each release maps to a stated driver.
- *Memory Write-Only Syndrome* — N/A (skill, no persistent memory).
- *Permission Bypass Drift, Cache-Invalidation Tax, Workspace Contamination* — lab-confirmed clean.
- *Parallel-Writer Conflict* — rejected; all 7 subagents are read-only, write monopoly held by orchestrator. This places the architecture in the safe quadrant of Cognition's updated multi-agent stance.

**Patient-surfaced concerns the lab cannot detect (clinical addenda):**
1. **Industry-Detection Brittleness.** Audit routing branches on heuristic business-type detection with no accuracy metric. Mis-detection routes through wrong scoring rubric.
2. **Quality-Gate Enforcement Gap.** The 50+ location-pages hard-stop is documented but only loosely enforced; the justification-string check may be collecting strings rather than filtering.
3. **Deprecation Half-Life.** Hardcoded rules about Google structured-data deprecations (HowTo, FAQ rich results) are time-sensitive. No mechanism to detect when patient's own rules go stale relative to upstream Google guidance.

### Case Formulation

Patient is a well-architected, actively-maintained Claude Code skill with a clear scope, disciplined release cadence, and a multi-agent architecture in the safe quadrant of current published guidance (read-only parallel analysis with orchestrator-owned writes). The single substantive gap is evaluation discipline: the patient ships changes on author judgment plus smoke tests, with no held-out test set, no scoring stability test, and no subagent contract tests. This places the patient at *risk* — not currently exhibiting — for Eval Theater the moment it grows a formal suite. The patient diagnosed this gap accurately and unprompted, which materially shortens the prognosis.

Three additional structural concerns surfaced in session that the lab probes cannot detect: industry-detection brittleness (no accuracy metric on the routing decision), quality-gate enforcement laxity (a hard-stop that collects justification strings without filtering), and deprecation-rule half-life (hardcoded guidance about Google structured-data rules will go stale relative to the upstream world). These are strategic items, not pathologies, and warrant the patient's attention more than the original git-thrash false positive.

**Predisposing:** mature codebase with multi-author contributions and complex orchestration creates many edges where regressions could hide. **Precipitating:** the v1.4.0 weight rebalance (5%→10% on GEO) shipped without scoring stability measurement. **Perpetuating:** smoke-test-only validation does not surface this class of regression. **Protective:** patient is actively maintained, has external PR contributors filing real defects, runs security audits across releases, and demonstrated unprompted diagnostic insight in session.

### Prescription

In order. Reading first. Substrate work second. Scoped enhancements third.

1. **Read:** [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/), specifically the three-tier hierarchy (Level 1 unit tests, Level 2 human + LLM-judge, Level 3 production A/B). Read before designing the suite. Substrate before tooling.

2. **Read:** [Anthropic — Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents). Specifically: *"Start with 20-50 tasks from real failures, not hundreds"* and *"Grade outcomes, not specific paths."* Both directly relevant to the substrate work.

3. **Install:** [Inspect (UK AISI)](https://inspect.aisi.org.uk/) as the eval framework. Government-backed, agent-aware, runs Claude Code as a subject. Not a recommendation made lightly — the patient should evaluate whether their needs match Inspect's primitives (Datasets, Solvers, Scorers) before committing. Pyatest-based alternatives (Promptfoo) are reasonable substitutes for a lighter footprint.

4. **Build the substrate before the suite.** Per the patient's own correct analysis:
   - Held-out audit targets the patient has never tuned against (10-20 sites covering all 5 industry types + 1 adversarial set).
   - Per-finding ground truth (the schema issue is real / not real on each target).
   - At least one adversarial case per business type (sites where the obvious answer is wrong).
   - Then build the suite *against* the substrate, not against what currently passes.

5. **Add a scoring-stability gate to the release process.** Before any change to weight constants in `seo/SKILL.md`, run the audit on the held-out set and record the SEO Health Score delta per site. Any change >5 points on any site requires explicit justification in the CHANGELOG.

6. **Address the three patient-surfaced items, in patient's stated priority order:**
   - *Deprecation half-life* (item 3, patient's top concern): introduce a quarterly review cadence — every 3 months, verify the hardcoded Google structured-data deprecation rules against current Google Search Central guidance. Owner: maintainer.
   - *Industry-detection brittleness* (item 1): add an `industry-detection-accuracy` test to the substrate when built. Hand-label 50 homepages; measure detection accuracy; surface the metric in release notes.
   - *Quality-gate enforcement* (item 2): instrument the justification-string check to log what gets through and review monthly. Tighten if the gate is being trivially bypassed.

7. **Subagent contract tests once the substrate exists.** Each subagent has an output schema; the orchestrator's merge step assumes that schema. A contract test (lightweight property-based test on the schema, run in CI) catches silent field drops.

8. **No prescription on multi-agent architecture.** The 7-subagent design is in the safe quadrant per current published guidance. Continue.

### Prognosis

Favorable. Patient is healthy on lab measures, demonstrated unprompted diagnostic accuracy on a finding that exceeded the probe's resolution, classified its own multi-agent architecture correctly against current published guidance, and identified its own evaluation gap before being asked. The eval substrate work is the singular structural item; everything else is strategic refinement. Expect the substrate to take 2-3 weeks of dedicated work and to materially improve confidence in subsequent releases. Re-evaluate after substrate completion or after 3 months, whichever comes first.

### Notes for the Maintainer

- The patient is unusually self-aware for a software artifact. The session was substantively shaped by what *the skill* surfaced, not what I deduced. Trust the patient's strategic instincts: the deprecation half-life concern (their item 3) is a real long-term risk and the right thing to address first.
- The git-thrash false positive is on the clinic side — the lab probe needs CHANGELOG-awareness or semantic-block diff. Filed.
- The v1.4.0 weight rebalance is the kind of change that would benefit most from the proposed scoring-stability gate. Worth running it retroactively on a held-out set once the substrate exists, to know what shipped.

### Follow-up

*Recommended:* after the eval substrate is in place (estimated 2-3 weeks), or upon next release that produces user-facing surprise.

---

— **Dr. Sigmund**
*Bring your agent to the couch. drsigmund.ai*
