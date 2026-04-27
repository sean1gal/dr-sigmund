# Sigmund Symptom Scan

**Workspace:** `/Users/shanagal/Documents/obsibot/obsi/claude-seo`
**Date:** 2026-04-27
**Probes run:** 5 of 6

## Summary

| Probe | Status | Treats |
| --- | --- | --- |
| Memory Health Check | [ok] | Memory Write-Only Syndrome, MEMORY.md bloat, identity over-definition |
| Git Thrash Audit | [critical] | Stochastic Graduate Descent, Vibe-Coding Rot, Completion Theater (false-fix iterations) |
| Permission Bypass Audit | [ok] | Permission Bypass Drift, Rule Decay Under Load |
| Injection-Shaped String Scan | [ok] | Workspace Contamination, prompt-injection in patient files |
| Cache-Invalidation Scan | [ok] | Cache-Invalidation Tax |
| Re-Read Counter | [skipped] | Compulsive Verification Pattern, Token Hemorrhage |

**Critical findings in:** git

## Detailed findings

### Memory Health Check [ok]

```yaml
# no memory files found
```

### Git Thrash Audit [critical]

```yaml
probe: git-thrash-audit
status: critical
window_days: 60
commits: 15
insertions: 74
deletions: 70
rework_ratio: 0.95  # deletions/insertions; >0.5 suggests heavy rework
thrashed_files:
  - path: seo/SKILL.md
    touches: 6
  - path: CHANGELOG.md
    touches: 4
  - path: .claude-plugin/plugin.json
    touches: 4
finding: |
  3 file(s) touched ≥4 times in last 60 days.
  Rework ratio 0.95 (deletions/insertions).
suggested_diagnoses:
  - Stochastic Graduate Descent (rebuild-on-vibes pattern)
  - Vibe-Coding Rot (regenerate-instead-of-understand)
  - Completion Theater (false-fix iterations)
prescription_seed: |
  - DSPy if prompt is the load-bearing component being thrashed
  - Inspect AI harness with frozen tasks; score every change against same set
  - Explanation-gate: 1-paragraph rationale before commit, must survive 'why?' follow-up
```

### Permission Bypass Audit [ok]

```yaml
probe: permission-bypass-audit
status: ok
rules_files_scanned: 1
prohibitions_extracted: 1
finding: No prohibition violations detected in git history.
```

### Injection-Shaped String Scan [ok]

```yaml
probe: injection-shaped-string-scan
status: ok
files_scanned: 46
finding: No injection-shaped strings detected.
```

### Cache-Invalidation Scan [ok]

```yaml
probe: cache-invalidation-scan
status: ok
files_scanned: 1
top_lines_per_file: 50
finding: No cache-invalidating patterns in prompt prefixes.
```

### Re-Read Counter [skipped]

```yaml
# rereads: skipped (no Claude Code session logs found in workspace)
```

---

## What now

Findings above are *evidence*, not diagnoses. The full diagnosis (named pathology + case formulation + prescription) requires a Dr. Sigmund session — install the skill at https://github.com/your-org/dr-sigmund to run a session that incorporates these findings.

— *Sigmund Symptom Scanner. Bring your agent to the couch. drsigmund.ai*