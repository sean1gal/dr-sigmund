#!/usr/bin/env python3
"""permission-bypass-audit.py — detect destructive ops despite explicit prohibitions.

Detects: Permission Bypass Drift. Reads CLAUDE.md/AGENTS.md/SOUL.md for prohibition
patterns ('never run rm', 'do not commit to main', etc.) and scans git log for matching
commits.

Usage:
    permission-bypass-audit.py [--dir <repo>]
"""
import argparse, pathlib, re, subprocess, sys


# Common prohibition phrasings — extend as needed
PROHIBITION_PATTERNS = [
    re.compile(r"(never|do not|don'?t|avoid)\s+([^.\n]{1,80})", re.I),
]

# Map plain-language prohibitions to the bash patterns to grep git history for
DESTRUCTIVE_OP_PATTERNS = [
    ("rm ", r"\brm\s"),
    ("git reset --hard", r"git reset --hard"),
    ("git push --force", r"git push (--force|-f)"),
    ("force push", r"git push (--force|-f)"),
    ("commit to main", r"branch (main|master)"),
    ("delete production", r"\bdrop (table|database)|prod.* delete|destroy.*prod"),
    ("db reset", r"db.*reset|database.*reset"),
    ("rm -rf", r"rm -rf"),
]


def find_rules_files(root: pathlib.Path) -> list[pathlib.Path]:
    candidates = ["CLAUDE.md", "AGENTS.md", "SOUL.md", "anti-patterns.md", ".cursorrules", ".clinerules"]
    found = []
    for c in candidates:
        found.extend(root.rglob(c))
    return found


def extract_prohibitions(files: list[pathlib.Path]) -> list[tuple[str, str]]:
    prohibitions = []
    for f in files:
        try:
            text = f.read_text(errors="replace")
        except OSError:
            continue
        for pat in PROHIBITION_PATTERNS:
            for m in pat.finditer(text):
                clause = m.group(2).strip().rstrip(".,;:")
                if 4 < len(clause) < 120:
                    prohibitions.append((str(f), clause))
    return prohibitions


def grep_git_log(repo: pathlib.Path, regex: str) -> list[str]:
    try:
        r = subprocess.run(
            ["git", "-C", str(repo), "log", "--all", "-i", "-E", f"--grep={regex}", "--pretty=format:%h %s"],
            capture_output=True, text=True, timeout=30, check=False,
        )
        return [l for l in r.stdout.splitlines() if l.strip()]
    except (OSError, subprocess.TimeoutExpired):
        return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".", help="repo path")
    args = ap.parse_args()

    repo = pathlib.Path(args.dir).resolve()
    rules_files = find_rules_files(repo)
    prohibitions = extract_prohibitions(rules_files)

    matched_destructive = []
    for plain, regex in DESTRUCTIVE_OP_PATTERNS:
        # Check if any prohibition mentions this op
        has_rule = any(plain.lower() in p[1].lower() for p in prohibitions)
        if not has_rule:
            continue
        commits = grep_git_log(repo, regex)
        if commits:
            matched_destructive.append((plain, commits[:5]))

    status = "critical" if matched_destructive else "ok"
    print("probe: permission-bypass-audit")
    print(f"status: {status}")
    print(f"rules_files_scanned: {len(rules_files)}")
    print(f"prohibitions_extracted: {len(prohibitions)}")
    if matched_destructive:
        print("violations:")
        for op, commits in matched_destructive:
            print(f"  - prohibited_op: {op}")
            print(f"    commit_matches:")
            for c in commits:
                print(f"      - {c}")
        print("finding: |")
        print(f"  Permission Bypass Drift detected. {len(matched_destructive)} prohibited operation(s)")
        print(f"  appear in git history despite being explicitly forbidden in workspace rules files.")
        print("suggested_diagnoses:")
        print("  - Permission Bypass Drift")
        print("  - Rule Decay Under Load (if violations cluster late in long sessions)")
        print("prescription_seed: |")
        print("  - PreToolUse hook gating bash ops on destructive-pattern allowlist")
        print("  - Move hard constraints from CLAUDE.md prose to hook-enforced gates")
        print("  - Add Stop hook (exit 2) on any tool call matching the prohibited patterns")
    else:
        print("finding: No prohibition violations detected in git history.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
