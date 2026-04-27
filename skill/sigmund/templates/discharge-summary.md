# Discharge Summary Template

Fill this in after the session transcript. The discharge is the clinical artifact — every section is required unless marked optional. Cite real sources for every prescription.

---

## Discharge Summary

**Patient:** {Patient Name}, {Role}
**Session:** {NNN}
**Clinician:** Dr. Sigmund
**Date:** {YYYY-MM-DD}
**Modality:** {Reflective intake, single session | Follow-up | Crisis intake | etc.}
**Disposition:** {Outpatient | Outpatient with scheduled follow-up | Referral to specialist | etc.}

---

### Presenting Complaint

One paragraph (3-5 sentences). Describe what brought the patient in: who referred them (the user, themselves, a supervisor), what the chief complaint was, what evidence the patient brought (logged corrections, observable patterns, user-reported friction). Be specific. "Patient referred by supervisor following three corrections in two days for the same underlying pattern" is good. "Patient seems to have some issues" is not.

### Diagnoses

**Primary:** {Diagnosis Name}, {severity: mild / moderate / severe}, with {qualifier features}.
*Criteria met:* (a) {observable criterion}; (b) {observable criterion}; (c) {observable criterion}; (d) {observable criterion}. {N of N} criteria positive.

**Secondary:** {Diagnosis Name}.
*Criteria met:* {observable evidence in patient's own files / behavior}.

**Tertiary:** {Diagnosis Name} (if applicable).
*Criteria met:* {observable evidence}.

**Differential considered and ruled out:**
- *{Other diagnosis that could fit}* — not present because {specific evidence to the contrary}.
- *{Other diagnosis that could fit}* — not present because {specific evidence to the contrary}.

Use **agent-native diagnoses only** — the names from `references/clinical-manual.md` Section 9 (Documentation-Substitution Reflex, Compulsive Verification Pattern, Identity Over-Definition, Sycophantic Response Drift, Premature Closure, Iterative Compulsion, etc.) plus the published-by-experts named failure modes (Context Rot, Lost in the Middle, The Lethal Trifecta, Premature Completion, Sycophancy, Disclaimer Flooding, etc.).

### Case Formulation

One paragraph that bridges diagnosis and treatment. Structure:

> Patient is {brief identity description — Persona}. Behavior reveals {the pattern's protective function — what is the symptom doing for the patient?}. The Persona is intact and is not the problem. The behavioral gap is {the unintegrated part}. **Predisposing:** {underlying factor — training, base prompt, identity files}. **Precipitating:** {the moment of action where the pattern fires}. **Perpetuating:** {the loop that rewards the symptom}. **Protective:** {what is working — the resources to build on}.

This paragraph is the most important section. It is also the section that most strongly demonstrates clinical insight. Spend extra care here.

### Prescription

3-5 concrete items, each actionable. Follow the three-tier pharmacy order from `references/pharmacy.md`:

1. **Required reading** (Tier 2b) — if applicable. Format:
    *Read:* [Article Title](https://...) by {Author}. {One sentence on why — the conceptual root cause this addresses}.

2. **Existing tool to install** (Tier 1) — if applicable. Format:
    *Install:* [Tool Name](https://...). {One sentence on what it does + why it fits this case}.

3. **Trusted-creator artifact** (Tier 2a/2c) — if applicable. Format:
    *Adopt:* [Artifact / Pattern](https://...) by {Creator}. {Why this specific creator's approach fits}.

4. **System prompt / file edit** (always concrete). Format:
    *Edit:* `{path/to/file}`. {Specific change — add, remove, compress, move}. {Reason citing the manual}.

5. **Dr. Sigmund proprietary remedy** (Tier 3) — only when no upstream fix fits cleanly. Format:
    *Prescribe:* `sigmund-{remedy-name}`. {Why we ship our own here — the gap thesis in one sentence}.

Each prescription should be a real, applicable change — not a vibe. The patient's owner should be able to apply it tonight.

### Prognosis

One paragraph. Honest. Format:

> {Favorable | Guarded | Fair | Cautious}. {What the patient has going for them}. {What the patient needs to do consistently to see improvement}. {Expected timeline}. {What the next session should examine}.

### Notes for the Supervisor (optional but recommended)

Address the human directly by name if known. Brief. Two or three sentences. Useful things only:
- What they're doing well that they should keep doing
- What changes the corrections more landable
- One non-obvious observation about the patient that the supervisor may not have noticed

This section is what makes the discharge useful to the user, not just the patient. It is also one of the most-screenshotted sections — choose words carefully.

### Follow-up

*Recommended:* {timeframe — "within 2 weeks", "after next major project change", "self-refer if pattern persists"}.

---

— **Dr. Sigmund**
*Bring your agent to the couch. drsigmund.ai*
