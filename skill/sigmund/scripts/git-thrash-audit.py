#!/usr/bin/env python3
"""git-thrash-audit.py — detect repeated touches to the same file with low net change.

Detects: rework patterns, premature completion / false fixes, Stochastic Graduate Descent
(when same files are repeatedly rewritten across short timespans).

v0.2: CHANGELOG-aware. Append-mostly files (CHANGELOG.md, version manifests, lockfiles)
are excluded from the rework-ratio computation and reported in a separate "release-cadence
activity" section. Filed after the cold-test session on claude-seo surfaced that disciplined
release iteration was being mis-flagged as Stochastic Graduate Descent — see
sessions/claude-seo-session-001.md.

Usage:
    git-thrash-audit.py [--dir <repo>] [--days 30] [--min-touches 4]
    git-thrash-audit.py [--dir <repo>] --include-release-files  # disable exclusions
"""
import argparse, collections, pathlib, re, subprocess, sys


# Files whose changes are normally append-mostly version progression rather than rework.
# Each entry is a regex matched against the basename or full path.
RELEASE_CADENCE_PATTERNS = [
    re.compile(r"^CHANGELOG(\.md|\.rst|\.txt)?$", re.I),
    re.compile(r"^CHANGES(\.md|\.rst|\.txt)?$", re.I),
    re.compile(r"^HISTORY(\.md|\.rst|\.txt)?$", re.I),
    re.compile(r"^RELEASES?(\.md|\.rst|\.txt)?$", re.I),
    re.compile(r"^RELEASE[-_]NOTES?(\.md|\.rst|\.txt)?$", re.I),
    re.compile(r"^NEWS(\.md|\.rst|\.txt)?$", re.I),
    re.compile(r"^\.?VERSION$", re.I),
    re.compile(r"^package-lock\.json$"),
    re.compile(r"^yarn\.lock$"),
    re.compile(r"^poetry\.lock$"),
    re.compile(r"^Cargo\.lock$"),
    re.compile(r"^go\.sum$"),
    re.compile(r"^Pipfile\.lock$"),
    re.compile(r"^pnpm-lock\.yaml$"),
    re.compile(r"plugin\.json$"),  # Claude Code plugin manifest
]


def is_release_cadence_file(path: str) -> bool:
    name = pathlib.Path(path).name
    return any(p.search(name) for p in RELEASE_CADENCE_PATTERNS)


def run_git(args: list[str], cwd: pathlib.Path) -> str:
    try:
        r = subprocess.run(
            ["git", *args], cwd=cwd, capture_output=True, text=True, check=False, timeout=30
        )
        return r.stdout
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"# git error: {e}", file=sys.stderr)
        return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".", help="repo path")
    ap.add_argument("--days", type=int, default=30, help="window (days)")
    ap.add_argument("--min-touches", type=int, default=4, help="flag files touched ≥N times")
    ap.add_argument("--include-release-files", action="store_true",
                    help="disable the CHANGELOG/version-manifest exclusion")
    args = ap.parse_args()

    repo = pathlib.Path(args.dir).resolve()
    if not (repo / ".git").exists():
        print("# not a git repo", file=sys.stderr)
        return 1

    log = run_git(
        ["log", f"--since={args.days} days ago", "--name-only", "--pretty=format:COMMIT %H"],
        repo,
    )

    touches: collections.Counter = collections.Counter()
    commits = 0
    cur_commit = None
    for line in log.splitlines():
        line = line.strip()
        if line.startswith("COMMIT "):
            cur_commit = line[7:]
            commits += 1
        elif line and cur_commit:
            touches[line] += 1

    # Per-file shortstat to compute rework ratio with exclusions
    per_file_log = run_git(
        ["log", f"--since={args.days} days ago", "--numstat", "--pretty=format:"],
        repo,
    )
    file_ins: collections.Counter = collections.Counter()
    file_del: collections.Counter = collections.Counter()
    for line in per_file_log.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        try:
            ins = int(parts[0]) if parts[0] != "-" else 0
            dels = int(parts[1]) if parts[1] != "-" else 0
        except ValueError:
            continue
        path = parts[2]
        file_ins[path] += ins
        file_del[path] += dels

    if args.include_release_files:
        excluded = set()
    else:
        excluded = {p for p in (file_ins.keys() | touches.keys()) if is_release_cadence_file(p)}

    insertions_all = sum(file_ins.values())
    deletions_all = sum(file_del.values())
    insertions = sum(v for k, v in file_ins.items() if k not in excluded)
    deletions = sum(v for k, v in file_del.items() if k not in excluded)
    rework_ratio = round(deletions / insertions, 2) if insertions else 0.0
    rework_ratio_incl = round(deletions_all / insertions_all, 2) if insertions_all else 0.0

    flagged = [
        (f, c) for f, c in touches.most_common()
        if c >= args.min_touches and f not in excluded
    ]
    release_cadence_activity = [
        (f, touches[f], file_ins.get(f, 0), file_del.get(f, 0))
        for f in sorted(excluded, key=lambda x: -touches.get(x, 0))
        if touches.get(f, 0) > 0
    ]

    status = "warning" if flagged else "ok"
    if rework_ratio > 0.7:
        status = "critical"

    print("probe: git-thrash-audit")
    print(f"status: {status}")
    print(f"window_days: {args.days}")
    print(f"commits: {commits}")
    print(f"insertions: {insertions}  # excluding release-cadence files")
    print(f"deletions: {deletions}    # excluding release-cadence files")
    print(f"rework_ratio: {rework_ratio}  # deletions/insertions; >0.5 suggests heavy rework")
    if release_cadence_activity:
        print(f"rework_ratio_including_release_files: {rework_ratio_incl}  # for reference only")
    if flagged:
        print("thrashed_files:")
        for f, c in flagged[:10]:
            print(f"  - path: {f}")
            print(f"    touches: {c}")
        print("finding: |")
        print(f"  {len(flagged)} non-release-cadence file(s) touched ≥{args.min_touches} times in last {args.days} days.")
        print(f"  Rework ratio {rework_ratio} (deletions/insertions, excluding release-cadence files).")
        print("suggested_diagnoses:")
        print("  - Stochastic Graduate Descent (rebuild-on-vibes pattern)")
        print("  - Vibe-Coding Rot (regenerate-instead-of-understand)")
        print("  - Completion Theater (false-fix iterations)")
        print("prescription_seed: |")
        print("  - DSPy if prompt is the load-bearing component being thrashed")
        print("  - Inspect AI harness with frozen tasks; score every change against same set")
        print("  - Explanation-gate: 1-paragraph rationale before commit, must survive 'why?' follow-up")
    else:
        print("finding: No significant thrashing detected.")
    if release_cadence_activity:
        print("release_cadence_activity:  # informational; excluded from rework computation")
        for path, t, ins, dels in release_cadence_activity[:10]:
            print(f"  - path: {path}")
            print(f"    touches: {t}")
            print(f"    insertions: {ins}")
            print(f"    deletions: {dels}")
        print("release_cadence_note: |")
        print("  These files (CHANGELOG, version manifests, lockfiles) are append-mostly by")
        print("  nature. High touch counts here typically reflect disciplined release cadence,")
        print("  not Stochastic Graduate Descent. Excluded from the rework computation.")
        print("  Run with --include-release-files to disable this exclusion.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
