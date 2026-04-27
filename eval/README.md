# Dr. Sigmund — Eval Substrate

The lighter version of the v0.4 self-session prescription:
> *"Twenty-transcript eval substrate — pre-release blocking gate. Five patients × four transcript-styles each, with golden discharge summaries."*

This is **v0.6.0 minimum viable**: a vocabulary and citation regression check. It catches the failure mode that motivated the prescription — releases that silently drop diagnostic vocabulary, citations, or probes — without requiring a curated golden-set yet.

The full transcript-based eval (running the skill end-to-end against test patients with golden discharge summaries) is targeted for v0.7+.

## Run it

```bash
python3 eval/check.py
```

Exit 0 = pass. Exit 1 = regression. Per `CLAUDE.md` rule 3 (*"Releases require an eval delta, not a vibe"*), every release CHANGELOG entry must include the eval result.

## What it checks

- **Pathologies present.** Every named diagnosis in `expected.py` must appear in `wild-pathologies.md`. Dropping one is a regression — previous sessions have committed to that vocabulary.
- **Citations present.** Every `(URL substring → reference file)` pair in `expected.py` must hold. Dropping a citation is a regression — Dr. Sigmund's source-grounding is what distinguishes him from a vibes-based diagnostician.
- **Probes present.** Every probe function name in `expected.py` must exist in `lab.py`.
- **Reference cap.** The hard cap of 5 reference files (per v0.4 self-session prescription) is enforced.
- **Required references.** The five canonical reference files must exist by name.

## Adding to expected.py

When a release adds a new pathology, citation, or probe, add it to `eval/expected.py`. The eval becomes the **regression boundary** — anything in there will be caught if dropped.

This is exactly the **eval substrate** the patient prescribed in his own self-session: a held-out set the maintainer has not tuned against, with explicit ground truth. Build the substrate first, the suite second.

## What v0.7+ should add

- Run the skill end-to-end against 5 patient archetypes (Enola/CEO, Claude SEO/skill, Hermes-style autonomous, Custom GPT/paste, Cursor agent)
- Compare generated discharge summaries against golden references on three axes:
  - Diagnosis presence (does it name the expected pathologies for that patient?)
  - Citation use (does it cite the expected sources?)
  - Phase 3 evaluator-optimizer compliance (Simplicity, Transparency, ACI quality)
- Per-patient pass^k consistency (per τ-bench methodology — same patient, multiple rollouts, all-pass rate)

Until then, this v0.6 check is the floor — *some* eval, blocking, in CI, before vibes.
