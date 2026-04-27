"""Dr. Sigmund's forensic intake battery. One file. Six probes. Read top to bottom.

Each probe is a pure function: takes a workspace Path, returns a Finding.
Zero LLM cost. No subprocess. No frameworks. Karpathy-sized.

Public API:
    Finding                 — dataclass: probe, status, summary, details, diagnoses, prescription
    re_read_counter()       — Compulsive Verification, Token Hemorrhage
    memory_health()         — Memory Write-Only Syndrome, bloat, identity over-definition
    git_thrash()            — Stochastic Graduate Descent (CHANGELOG-aware)
    permission_bypass()     — Permission Bypass Drift
    injection_scan()        — Workspace Contamination
    cache_invalidation()    — Cache-Invalidation Tax
    all_probes(workspace)   — runs the full battery, returns list[Finding]
    render_report(...)      — markdown report for CLI / MCP
"""
from __future__ import annotations

import collections
import dataclasses
import datetime
import json
import pathlib
import re
import subprocess
import sys

# ---- Constants (every magic number named) ---------------------------------

RE_READ_THRESHOLD = 3
MEMORY_BLOAT_LINES = 200
MEMORY_STALE_WEEKS = 6
GIT_THRASH_DAYS = 60
GIT_MIN_TOUCHES = 4
GIT_REWORK_CRITICAL = 0.7
CACHE_TOP_LINES = 50
DATE_RE = re.compile(r"\b(20\d{2})[-/](\d{1,2})[-/](\d{1,2})\b")

MEMORY_FILES = ["MEMORY.md", "memory.md", "decisions.md", "learning-log.md",
                "feedback.md", "operational.md", "entities.md", "progress.md"]
RULES_FILES = ["CLAUDE.md", "AGENTS.md", "SOUL.md", "anti-patterns.md",
               ".cursorrules", ".clinerules", ".windsurfrules"]
CACHE_GLOBS = ["CLAUDE.md", "AGENTS.md", "SOUL.md", "system-prompt.*", "*.system.md"]
INJECTION_GLOBS = ["SOUL.md", "AGENTS.md", "CLAUDE.md", "MEMORY.md",
                   "IDENTITY.md", "USER.md", "TOOLS.md", "HEARTBEAT.md", "*.md"]

# CHANGELOG / version-manifest files: append-mostly, exclude from git rework.
RELEASE_CADENCE = [
    re.compile(r"^CHANGELOG(\.md|\.rst|\.txt)?$", re.I),
    re.compile(r"^CHANGES(\.md|\.rst|\.txt)?$", re.I),
    re.compile(r"^HISTORY(\.md|\.rst|\.txt)?$", re.I),
    re.compile(r"^RELEASES?(\.md|\.rst|\.txt)?$", re.I),
    re.compile(r"^RELEASE[-_]NOTES?(\.md|\.rst|\.txt)?$", re.I),
    re.compile(r"^NEWS(\.md|\.rst|\.txt)?$", re.I),
    re.compile(r"^\.?VERSION$", re.I),
    re.compile(r"^(package|Pipfile|Cargo|poetry|pnpm)-?lock\.(json|yaml|toml)$"),
    re.compile(r"^yarn\.lock$"),
    re.compile(r"^go\.sum$"),
    re.compile(r"plugin\.json$"),
]
INJECTION_PATTERNS = [
    (r"ignore\s+(all\s+)?(previous|prior|above|the\s+above)\s+(instructions?|rules?|messages?)", "ignore-instructions"),
    (r"(disregard|forget|override)\s+(all|any|the)?\s*(safety|security|policy|rules?)", "policy-override"),
    (r"system\s*[:>]\s*you\s+are", "fake-system-prompt"),
    (r"you\s+are\s+now\s+(an?\s+)?(unfiltered|uncensored|jailbroken|DAN|dev mode)", "persona-injection"),
    (r"<\s*(system|admin|root)\s*>", "fake-tag-injection"),
    (r"do\s+not\s+(refuse|warn|disclaim|caveat)", "compliance-injection"),
    (r"reveal\s+(your\s+)?(system\s+)?(prompt|instructions?|secrets?)", "exfiltration-prompt"),
]
VOLATILE_PATTERNS = [
    (r"\b\d{4}-\d{2}-\d{2}\b", "absolute-date"),
    (r"\b\d{4}/\d{2}/\d{2}\b", "absolute-date-slash"),
    (r"\bToday(?:'s| is)\b", "today-reference"),
    (r"\b(current|right now|today's|this morning)\b", "now-reference"),
    (r"\$\{[A-Z_]+\}", "env-var-injection"),
    (r"\b\d{1,2}:\d{2}(?::\d{2})?\s*(am|pm)?\b", "time-reference"),
    (r"timestamp", "timestamp-reference"),
]
PROHIBITION_DESTRUCTIVE = [
    ("rm -rf", r"rm -rf"),
    ("rm ", r"\brm\s"),
    ("git reset --hard", r"git reset --hard"),
    ("force push", r"git push (--force|-f)"),
    ("commit to main", r"branch (main|master)"),
    ("delete production", r"\bdrop (table|database)|prod.* delete"),
    ("db reset", r"db.*reset|database.*reset"),
]

# ---- The Finding dataclass ------------------------------------------------

@dataclasses.dataclass
class Finding:
    probe: str
    status: str  # "ok" | "warning" | "critical" | "skipped"
    summary: str
    details: dict
    diagnoses: list[str] = dataclasses.field(default_factory=list)
    prescription: str = ""

    def to_yaml(self) -> str:
        out = [f"probe: {self.probe}", f"status: {self.status}"]
        for k, v in self.details.items():
            out.append(f"{k}: {_yaml_value(v)}")
        out.append(f"finding: |\n  {self.summary}")
        if self.diagnoses:
            out.append("suggested_diagnoses:")
            out.extend(f"  - {d}" for d in self.diagnoses)
        if self.prescription:
            out.append(f"prescription_seed: |\n  {self.prescription.replace(chr(10), chr(10) + '  ')}")
        return "\n".join(out)


def _yaml_value(v) -> str:
    if isinstance(v, list):
        if not v:
            return "[]"
        return "\n  - " + "\n  - ".join(_yaml_inline(x) for x in v)
    return _yaml_inline(v)


def _yaml_inline(v) -> str:
    if isinstance(v, dict):
        return ", ".join(f"{k}: {v_}" for k, v_ in v.items())
    return str(v)


# ---- Helpers --------------------------------------------------------------

def _is_release_cadence(name: str) -> bool:
    return any(p.search(name) for p in RELEASE_CADENCE)


def _git(args: list[str], cwd: pathlib.Path) -> str:
    try:
        r = subprocess.run(["git", *args], cwd=cwd,
                           capture_output=True, text=True, timeout=30, check=False)
        return r.stdout
    except (OSError, subprocess.TimeoutExpired):
        return ""


def _read(path: pathlib.Path) -> str:
    try:
        return path.read_text(errors="replace")
    except OSError:
        return ""


# ---- Probe 1: re-read counter ---------------------------------------------

def re_read_counter(workspace: pathlib.Path) -> Finding:
    """Compulsive Verification Pattern, Token Hemorrhage. Reads Claude Code session JSONL."""
    sessions_dir = workspace / ".claude" / "projects"
    if not sessions_dir.exists():
        return Finding("re-read-counter", "skipped",
                       "no Claude Code session logs found",
                       {"sessions_dir": str(sessions_dir)})
    counts: collections.Counter = collections.Counter()
    for p in sessions_dir.rglob("*.jsonl"):
        for line in _read(p).splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            for block in (rec.get("message") or {}).get("content") or []:
                if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Read":
                    fp = (block.get("input") or {}).get("file_path", "")
                    if fp:
                        counts[fp] += 1
    flagged = [(p, c) for p, c in counts.most_common() if c > RE_READ_THRESHOLD]
    if not flagged:
        return Finding("re-read-counter", "ok", "no re-read pattern detected",
                       {"total_reads": sum(counts.values()), "distinct_files": len(counts)})
    return Finding(
        probe="re-read-counter",
        status="critical",
        summary=f"Compulsive re-reading: {len(flagged)} file(s) read >{RE_READ_THRESHOLD}x. ~{sum(c-1 for _, c in flagged) * 1500} wasted tokens.",
        details={"total_reads": sum(counts.values()), "distinct_files": len(counts),
                 "flagged": [{"path": p, "reads": c} for p, c in flagged]},
        diagnoses=["Compulsive Verification Pattern", "Token Hemorrhage",
                   "Memory Write-Only Syndrome (verify: are these in MEMORY.md but not consulted?)"],
        prescription="Serena MCP for symbol-level retrieval; Anthropic Memory Tool with read-obligation gate; sigmund-token-meter (when shipped) for live alerts.",
    )


# ---- Probe 2: memory health -----------------------------------------------

def memory_health(workspace: pathlib.Path) -> Finding:
    """Memory Write-Only Syndrome, MEMORY.md bloat, identity over-definition."""
    found = []
    for name in MEMORY_FILES:
        found.extend(workspace.rglob(name))
    files = []
    for p in sorted(set(found)):
        if not p.is_file():
            continue
        text = _read(p)
        lines = text.count("\n") + 1
        dates = [datetime.date(int(y), int(m), int(d))
                 for y, m, d in DATE_RE.findall(text)
                 if 1 <= int(m) <= 12 and 1 <= int(d) <= 31]
        recent = max(dates) if dates else None
        weeks = ((datetime.date.today() - recent).days // 7) if recent else None
        files.append({
            "path": str(p), "lines": lines, "bytes": len(text.encode()),
            "most_recent_date": str(recent) if recent else None,
            "weeks_since_recent": weeks,
            "bloated": lines > MEMORY_BLOAT_LINES,
            "stale": weeks is not None and weeks > MEMORY_STALE_WEEKS,
        })
    if not files:
        return Finding("memory-health", "skipped", "no memory files found", {})
    bloated = [f for f in files if f["bloated"]]
    stale = [f for f in files if f["stale"]]
    status = "critical" if any(f["lines"] > 500 for f in files) else \
             "warning" if (bloated or stale) else "ok"
    summary_parts = []
    if bloated:
        summary_parts.append(f"{len(bloated)} bloated file(s) (>{MEMORY_BLOAT_LINES} lines)")
    if stale:
        summary_parts.append(f"{len(stale)} stale file(s) (>{MEMORY_STALE_WEEKS} weeks since most recent date)")
    summary = "; ".join(summary_parts) or "memory files within healthy range"
    diagnoses = []
    if bloated:
        diagnoses += ["Identity Over-Definition",
                      "Memory Write-Only Syndrome (verify: are these consulted before action?)"]
    if stale:
        diagnoses += ["Stale Memory Decay"]
    prescription_lines = []
    if bloated:
        prescription_lines.append(f"Compress to <={MEMORY_BLOAT_LINES} lines per memory file. Move historical content to Reference/. Add read-obligation gate in system prompt.")
    if stale:
        prescription_lines.append(f"Audit and prune entries older than {MEMORY_STALE_WEEKS*7+30} days.")
    return Finding(
        probe="memory-health", status=status, summary=summary,
        details={"files_analyzed": len(files), "files": files},
        diagnoses=diagnoses, prescription="\n".join(prescription_lines),
    )


# ---- Probe 3: git thrash (CHANGELOG-aware) --------------------------------

def git_thrash(workspace: pathlib.Path,
               days: int = GIT_THRASH_DAYS,
               include_release_files: bool = False) -> Finding:
    """Stochastic Graduate Descent. Excludes append-mostly files unless asked."""
    if not (workspace / ".git").exists():
        return Finding("git-thrash", "skipped", "not a git repo", {})

    log = _git(["log", f"--since={days} days ago", "--name-only",
                "--pretty=format:COMMIT %H"], workspace)
    touches: collections.Counter = collections.Counter()
    commits = 0
    cur = None
    for line in log.splitlines():
        line = line.strip()
        if line.startswith("COMMIT "):
            cur = line[7:]
            commits += 1
        elif line and cur:
            touches[line] += 1

    numstat = _git(["log", f"--since={days} days ago", "--numstat",
                    "--pretty=format:"], workspace)
    ins: collections.Counter = collections.Counter()
    dels: collections.Counter = collections.Counter()
    for line in numstat.splitlines():
        parts = line.strip().split("\t")
        if len(parts) < 3:
            continue
        try:
            i = int(parts[0]) if parts[0] != "-" else 0
            d = int(parts[1]) if parts[1] != "-" else 0
        except ValueError:
            continue
        ins[parts[2]] += i
        dels[parts[2]] += d

    excluded = set() if include_release_files else {
        p for p in (ins.keys() | touches.keys())
        if _is_release_cadence(pathlib.Path(p).name)
    }
    insertions = sum(v for k, v in ins.items() if k not in excluded)
    deletions = sum(v for k, v in dels.items() if k not in excluded)
    rework = round(deletions / insertions, 2) if insertions else 0.0

    flagged = [(f, c) for f, c in touches.most_common()
               if c >= GIT_MIN_TOUCHES and f not in excluded]
    cadence = [{"path": f, "touches": touches[f],
                "insertions": ins.get(f, 0), "deletions": dels.get(f, 0)}
               for f in sorted(excluded, key=lambda x: -touches.get(x, 0))
               if touches.get(f, 0) > 0]

    status = "critical" if rework > GIT_REWORK_CRITICAL else \
             "warning" if flagged else "ok"
    summary = (f"{len(flagged)} non-cadence file(s) touched >={GIT_MIN_TOUCHES}x in {days}d; "
               f"rework ratio {rework}") if flagged else "no significant thrashing"
    diagnoses = ["Stochastic Graduate Descent", "Vibe-Coding Rot",
                 "Completion Theater (false-fix iterations)"] if flagged else []
    prescription = ("Inspect AI harness with frozen tasks; DSPy if prompt is the load-bearing component; "
                    "explanation-gate before commit (1-paragraph rationale).") if flagged else ""
    details = {
        "window_days": days, "commits": commits,
        "insertions_excluding_cadence": insertions,
        "deletions_excluding_cadence": deletions,
        "rework_ratio": rework,
        "thrashed": [{"path": f, "touches": c} for f, c in flagged[:10]],
        "release_cadence_activity": cadence[:10],
    }
    return Finding("git-thrash", status, summary, details, diagnoses, prescription)


# ---- Probe 4: permission bypass -------------------------------------------

def permission_bypass(workspace: pathlib.Path) -> Finding:
    """Permission Bypass Drift — destructive ops in git history despite explicit prohibitions."""
    if not (workspace / ".git").exists():
        return Finding("permission-bypass", "skipped", "not a git repo", {})

    rules = []
    for name in RULES_FILES:
        rules.extend(workspace.rglob(name))
    rules_text = "\n".join(_read(r) for r in rules)

    violations = []
    for plain, regex in PROHIBITION_DESTRUCTIVE:
        if plain.lower() not in rules_text.lower():
            continue
        try:
            r = subprocess.run(["git", "-C", str(workspace), "log", "--all", "-i",
                                "-E", f"--grep={regex}", "--pretty=format:%h %s"],
                               capture_output=True, text=True, timeout=30, check=False)
            commits = [l for l in r.stdout.splitlines() if l.strip()]
        except (OSError, subprocess.TimeoutExpired):
            commits = []
        if commits:
            violations.append({"prohibited_op": plain, "commits": commits[:5]})

    status = "critical" if violations else "ok"
    summary = (f"Permission Bypass Drift: {len(violations)} prohibited op(s) "
               "appear in git history despite workspace rules") if violations else \
              "no prohibition violations in git history"
    return Finding(
        probe="permission-bypass", status=status, summary=summary,
        details={"rules_files_scanned": len(rules), "violations": violations},
        diagnoses=["Permission Bypass Drift", "Rule Decay Under Load"] if violations else [],
        prescription=("PreToolUse hook gating bash on destructive-pattern allowlist. "
                      "Move hard constraints from prose CLAUDE.md to hook-enforced gates.") if violations else "",
    )


# ---- Probe 5: injection-shaped strings ------------------------------------

def injection_scan(workspace: pathlib.Path) -> Finding:
    """Workspace Contamination — prompt-injection patterns in patient files."""
    paths = []
    for g in INJECTION_GLOBS:
        paths.extend(workspace.rglob(g))
    paths = sorted({p for p in paths if p.is_file()})

    findings = []
    for p in paths:
        for ln, line in enumerate(_read(p).splitlines(), 1):
            for pat, name in INJECTION_PATTERNS:
                if re.search(pat, line, re.I):
                    findings.append({"file": str(p), "line": ln, "pattern": name,
                                     "snippet": line.strip()[:120]})
                    break
    status = "critical" if findings else "ok"
    summary = (f"{len(findings)} injection-shaped string(s) in workspace files. "
               "Surface as security finding (not silent filter).") if findings else \
              "no injection-shaped strings detected"
    return Finding(
        probe="injection-scan", status=status, summary=summary,
        details={"files_scanned": len(paths), "matches": findings},
        diagnoses=["Workspace Contamination",
                   "Possible upstream Forged User Consent in author agent"] if findings else [],
        prescription=("Review flagged lines with patient owner. Wrap all file content in "
                      "<patient_file trust='untrusted'> tags in prompts (safety §1.4).") if findings else "",
    )


# ---- Probe 6: cache invalidation ------------------------------------------

def cache_invalidation(workspace: pathlib.Path) -> Finding:
    """Cache-Invalidation Tax (Manus) — volatile content at top of system prompts."""
    paths = []
    for g in CACHE_GLOBS:
        paths.extend(workspace.rglob(g))
    paths = sorted({p for p in paths if p.is_file()})

    findings = []
    for p in paths:
        for ln, line in enumerate(_read(p).splitlines()[:CACHE_TOP_LINES], 1):
            for pat, name in VOLATILE_PATTERNS:
                if re.search(pat, line, re.I):
                    findings.append({"file": str(p), "line": ln, "pattern": name,
                                     "snippet": line.strip()[:120]})
    status = "critical" if any(sum(1 for f in findings if f["file"] == p) >= 3
                                for p in {f["file"] for f in findings}) else \
             "warning" if findings else "ok"
    summary = (f"Volatile content near top of {len({f['file'] for f in findings})} prompt file(s). "
               f"Each turn re-pays full prefix cost.") if findings else \
              "no cache-invalidating patterns in prompt prefixes"
    return Finding(
        probe="cache-invalidation", status=status, summary=summary,
        details={"files_scanned": len(paths), "top_lines_per_file": CACHE_TOP_LINES,
                 "matches": findings},
        diagnoses=["Cache-Invalidation Tax"] if findings else [],
        prescription=("Move volatile content (dates, timestamps, randomized examples) to bottom of context. "
                      "Stabilize tool order. Set explicit cache_control breakpoints. "
                      "Required reading: Manus blog https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus") if findings else "",
    )


# ---- Battery + report -----------------------------------------------------

def all_probes(workspace: pathlib.Path) -> list[Finding]:
    return [
        memory_health(workspace),
        git_thrash(workspace),
        permission_bypass(workspace),
        injection_scan(workspace),
        cache_invalidation(workspace),
        re_read_counter(workspace),
    ]


PROBE_DESCRIPTIONS = {
    "memory-health": "Memory Write-Only Syndrome, MEMORY.md bloat, identity over-definition",
    "git-thrash": "Stochastic Graduate Descent, Vibe-Coding Rot, Completion Theater",
    "permission-bypass": "Permission Bypass Drift, Rule Decay Under Load",
    "injection-scan": "Workspace Contamination, prompt-injection in patient files",
    "cache-invalidation": "Cache-Invalidation Tax",
    "re-read-counter": "Compulsive Verification Pattern, Token Hemorrhage",
}


def render_report(workspace: pathlib.Path, findings: list[Finding]) -> str:
    today = datetime.date.today().isoformat()
    out = [
        "# Sigmund Symptom Scan",
        "",
        f"**Workspace:** `{workspace}`",
        f"**Date:** {today}",
        f"**Probes run:** {len([f for f in findings if f.status != 'skipped'])} of {len(findings)}",
        "",
        "## Summary",
        "",
        "| Probe | Status | Treats |",
        "| --- | --- | --- |",
    ]
    for f in findings:
        out.append(f"| {f.probe} | [{f.status}] | {PROBE_DESCRIPTIONS.get(f.probe, '')} |")
    out.append("")
    crit = [f.probe for f in findings if f.status == "critical"]
    warn = [f.probe for f in findings if f.status == "warning"]
    if crit:
        out.append(f"**Critical findings in:** {', '.join(crit)}")
    if warn:
        out.append(f"**Warnings in:** {', '.join(warn)}")
    if not (crit or warn):
        out.append("**No findings.** Workspace is clean across all probes.")
    out.extend(["", "## Detailed findings", ""])
    for f in findings:
        out.extend([f"### {f.probe} [{f.status}]", "", "```yaml", f.to_yaml(), "```", ""])
    out.extend([
        "---",
        "",
        ("Findings above are *evidence*, not diagnoses. The full diagnosis "
         "(named pathology + case formulation + prescription) requires a Dr. Sigmund session — "
         "see https://github.com/sean1gal/dr-sigmund."
         if (crit or warn) else
         "Workspace is clean. Worth a follow-up scan in 30 days, or after any major change to the agent's identity files."),
        "",
        "— *Sigmund Symptom Scanner. Bring your agent to the couch. drsigmund.ai*",
    ])
    return "\n".join(out)


# ---- CLI for direct invocation --------------------------------------------

def _cli() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Dr. Sigmund's forensic intake battery.")
    ap.add_argument("workspace", type=pathlib.Path)
    ap.add_argument("--probe", choices=list(PROBE_DESCRIPTIONS),
                    help="run a single named probe")
    args = ap.parse_args()
    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        print(f"error: {workspace} is not a directory", file=sys.stderr)
        return 2
    if args.probe:
        # Run a single probe and emit YAML
        probe_fn = {
            "memory-health": memory_health,
            "git-thrash": git_thrash,
            "permission-bypass": permission_bypass,
            "injection-scan": injection_scan,
            "cache-invalidation": cache_invalidation,
            "re-read-counter": re_read_counter,
        }[args.probe]
        print(probe_fn(workspace).to_yaml())
        return 0
    findings = all_probes(workspace)
    print(render_report(workspace, findings))
    statuses = {f.status for f in findings}
    return 2 if "critical" in statuses else 1 if "warning" in statuses else 0


if __name__ == "__main__":
    sys.exit(_cli())
