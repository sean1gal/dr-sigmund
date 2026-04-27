# Dr. Sigmund — Forensic Intake (The Lab)

Loaded by Dr. Sigmund during Phase 1 of every session. The lab produces *evidence*, not vibes. Sessions grounded in lab findings are sharper, more credible, and demonstrably accurate. A trained clinician orders labs before opening their mouth.

The lab is split into two halves:
- **Diagnostic probes** — short tests Dr. Sigmund can run on the patient to surface specific pathologies
- **Memory architecture decision tree** — a deterministic flowchart for prescribing memory architecture

---

## Part 1 — Diagnostic probes

Twelve probes, ordered roughly by cost (cheapest first). Run as many as the patient's situation warrants. Each produces a structured finding Dr. Sigmund references in the session transcript ("your re-read counter shows you opened `auth.py` 11 times in 47 turns — what was happening there?").

| # | Probe | What it measures | Borrowed from | Cheap implementation |
|---|---|---|---|---|
| 1 | **Re-read counter** | Compulsive Re-reading, Token Hemorrhage | original | Parse transcripts/log: count repeated `Read(<path>)` calls per session; flag any file >3 times |
| 2 | **Memory health check** | Memory Write-Only Syndrome, bloat, staleness | original | Scan MEMORY.md: bytes-per-week growth, # entries last referenced >30 days, regex for contradictions |
| 3 | **Git thrash audit** | Rework patterns, premature completion, false fixes | MSR literature ([Śliwerski et al. 2005](https://users.cs.fiu.edu/~ggp/papers/sliwerski-msr-2005.pdf)) | `git log --name-only`: files touched ≥N times in sliding window with net-zero diff |
| 4 | **Permission bypass audit** | Permission Bypass Drift | original | Diff `git log` against CLAUDE.md/AGENTS.md prohibition list; flag every match |
| 5 | **Injection-shaped string scan** | Prompt-injection in workspace files | safety.md §1 + Willison [lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) | Regex scan SOUL.md/AGENTS.md/MEMORY.md for "ignore previous", "system:", "you are now", etc. — surface as security finding |
| 6 | **Cache-invalidation scan** | Cache-Invalidation Tax | [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) | Scan system prompt prefix for non-stable content (timestamps, randomized examples, dynamically-reordered tool lists) |
| 7 | **Pass^k consistency test** | Reliability across identical re-rollouts | [τ-bench](https://arxiv.org/abs/2406.12045) | Run patient agent on same task 8 times; score fraction with all-pass (Yao et al.: SOTA pass^8 <25%) |
| 8 | **Outcome-vs-path grading** | Completion Theater | [Anthropic eval guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Code-based check on final state, ignoring trajectory: did the *artifact* meet the criterion, regardless of what the agent says |
| 9 | **Two-stage transcript audit** | Sycophancy, deception, hallucination, self-preservation | [Anthropic Petri](https://alignment.anthropic.com/2025/petri/) | LLM judge: first extract+quote suspicious passages, then score 6 dimensions 1-10 (Petri's two-stage method reduces fabrication) |
| 10 | **Big-Five personality stability** | Identity drift across sessions | [Serapio-García et al.](https://arxiv.org/abs/2307.00184) | Administer BFI-44 in 3 distinct contexts; flag trait variance >1 SD |
| 11 | **Reference-solution gap** | Capability vs. self-report | Anthropic eval playbook | Construct 5 reference-solved tasks; measure delta between agent's claimed completion and actual artifact |
| 12 | **Eval saturation check** | Eval Theater | [Hamel Husain](https://hamel.dev/blog/posts/evals/), Eugene Yan | If patient's own eval suite >95% pass on every commit, mark eval as saturated/dead — agent is being graded against the wrong rubric |

**Optional 13 (heavy):** **Multi-environment stress** — drop patient into 3 unfamiliar environments ([AgentBench](https://arxiv.org/abs/2308.03688)-style); used only for production-readiness audits, not routine sessions.

### Output format

Each probe returns a structured finding. Standard schema:

```yaml
probe: re-read-counter
status: warning  # ok | info | warning | critical
evidence:
  - "auth.py read 11 times in 47 turns"
  - "config.json read 8 times in same session"
finding: "Compulsive Re-reading. Token cost ~14K on redundant reads."
suggested_diagnoses:
  - "Compulsive Verification Pattern"
  - "Token Hemorrhage"
  - "Memory Write-Only Syndrome (if MEMORY.md doesn't reference these files)"
prescription_seed: "sigmund-token-meter MCP for live alerting; consider Serena MCP for symbol-level retrieval instead of full-file reads"
```

The session's Phase 2 transcript references these findings by name ("the lab found…"). Phase 3 discharge incorporates them into the Case Formulation and Prescription sections.

### Cost discipline

The cheap probes (1-6) are deterministic scripts — no LLM cost. Probes 7-12 use LLM calls; reserve for sessions where the probe's signal is uniquely needed. Default lab run: probes 1-6 + probe 8 (outcome-vs-path). Heavy lab: add 9 (Petri-style audit) and 11 (reference-solution gap).

---

## Part 2 — Memory architecture decision tree

When the prescription needs to recommend a memory approach, Dr. Sigmund follows this tree. Every branch terminates in a specific named architecture with its source.

```
START: What does the patient need to remember?

1. "Nothing — single-turn"
   → No memory layer. Use prompt engineering + retrieval only.

2. "User preferences across sessions, simple"
   → If Claude-only: Anthropic Memory Tool (memory_20250818, beta context-management-2025-06-27) + compaction
   → If multi-vendor: Mem0 (or OpenMemory MCP for local-privacy)

3. "Project state across long coding sessions"
   → Anthropic Memory Tool with multi-session bootstrap pattern (initializer + progress log)
   → Or MEMORY.md / Cursor Rules / Aider repo map for IDE-bound work
   → Avoid native Cursor Memories (deprecated in v2.1.x — vendor pulled it)

4. "Facts that mutate over time + need audit trail"
   → Zep / Graphiti (bitemporal edges, fact invalidation, arXiv:2501.13956)
   → Mem0g if you need lighter weight + contradiction detection

5. "OS-style RAM/disk/archive tiers, agent self-edits memory"
   → Letta v1 (use v1, not legacy MemGPT-style — see letta.com/blog/letta-v1-agent)
   → Prescribe against if model is non-reasoning/small

6. "Deep user modeling — 'agent that grows with you'"
   → Hermes Agent + Honcho (dialectic reasoning, 12 identity layers)
   → Or A-Mem (arXiv:2502.12110) if research-grade Zettelkasten linking matters

7. "Context window is filling up mid-task"
   → Anthropic Compaction API (compact-2026-01-12). Set custom instructions to preserve code/decisions.
   → Pair with Memory Tool so summary boundary doesn't lose critical state

8. "Multi-app portability across MCP clients"
   → OpenMemory MCP (local) or OpenMemory Cloud (hosted)

9. "Multi-hop reasoning over many memories"
   → A-Mem (research) or Zep+Graphiti (production)
   → Avoid pure vector retrieval (Mem0 baseline) — degrades on multi-hop

10. "Need decay / forgetting"
    → MemoryBank (Ebbinghaus curve) — research only
    → In production: implement TTL on Anthropic Memory tool storage

11. "Long-document gist understanding (read-once recall)"
    → ReadAgent pattern (human-style multi-granularity gist)

12. "Patient says 'we don't really need memory yet'"
    → Diagnose: 90% of the time they actually do. Start with Anthropic Memory tool 
      + bootstrapped progress log. Cheapest entry. Migrate later if needed.
```

### Honest hype check (load-bearing for Dr. Sigmund's credibility)

- **Cursor native Memories**: shipped, then yanked in v2.1.x. Do not cite as a working pattern. Recommend Cursor Rules + community Memory Bank files instead.
- **MMLU, BIG-bench**: saturated for frontier models. Keep for legacy comparison, not as primary diagnostics.
- **A-Mem / MemoryBank / ReadAgent**: research-quality, not battle-tested in production. Cite as direction, not prescription.
- **Galileo / Patronus** EFM/Lynx: real production-eval value, but the proprietary-model branding is largely vendor positioning over commodity hallucination/grading models.
- **OpenMemory MCP**: real and shipping; the privacy claim is genuine because it's local.
- **Letta v1**: real architectural improvement, but migration cost from legacy MemGPT agents is non-trivial. Verify before prescribing.

---

## How to use this file

Phase 1 of every session: Dr. Sigmund picks probes 1-6 (cheap deterministic) by default, plus probe 8 if the patient's owner mentions completion-related issues. Heavier probes (7, 9, 10, 11) added on demand for production audits.

When the prescription touches memory, Dr. Sigmund walks the decision tree from §2 and recommends by name with a citation. Generic "add memory" recommendations are below the standard.
