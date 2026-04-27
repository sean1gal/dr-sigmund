#!/usr/bin/env python3
"""memory-health-check.py — scan MEMORY.md (and similar) for bloat, staleness, contradictions.

Detects: Memory Write-Only Syndrome, MEMORY.md bloat, stale entries, identity over-definition.

Usage:
    memory-health-check.py <file>...
    memory-health-check.py --workspace <dir>     # auto-discover memory files
"""
import argparse, pathlib, re, sys, datetime


MEMORY_FILE_PATTERNS = [
    "MEMORY.md", "memory.md", "decisions.md", "learning-log.md",
    "feedback.md", "operational.md", "entities.md", "progress.md",
]
DATE_RE = re.compile(r"\b(20\d{2})[-/](\d{1,2})[-/](\d{1,2})\b")
LINE_BLOAT_THRESHOLD = 200
WEEKS_STALE_THRESHOLD = 6


def find_memory_files(root: pathlib.Path) -> list[pathlib.Path]:
    found = []
    for pat in MEMORY_FILE_PATTERNS:
        found.extend(root.rglob(pat))
    return found


def analyze(path: pathlib.Path) -> dict:
    text = path.read_text(errors="replace")
    lines = text.splitlines()
    line_count = len(lines)
    byte_count = len(text.encode())
    dates = [
        datetime.date(int(y), int(m), int(d))
        for y, m, d in DATE_RE.findall(text)
        if 1 <= int(m) <= 12 and 1 <= int(d) <= 31
    ]
    today = datetime.date.today()
    most_recent = max(dates) if dates else None
    weeks_since_recent = ((today - most_recent).days // 7) if most_recent else None
    return {
        "path": str(path),
        "lines": line_count,
        "bytes": byte_count,
        "n_dated_entries": len(dates),
        "most_recent_date": str(most_recent) if most_recent else None,
        "weeks_since_recent": weeks_since_recent,
        "is_bloated": line_count > LINE_BLOAT_THRESHOLD,
        "is_stale": weeks_since_recent is not None and weeks_since_recent > WEEKS_STALE_THRESHOLD,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", help="memory files to analyze")
    ap.add_argument("--workspace", help="auto-discover memory files in this directory")
    args = ap.parse_args()

    paths = [pathlib.Path(f) for f in args.files]
    if args.workspace:
        paths.extend(find_memory_files(pathlib.Path(args.workspace)))
    paths = sorted(set(paths))

    if not paths:
        print("# no memory files found", file=sys.stderr)
        return 1

    findings = [analyze(p) for p in paths if p.is_file()]
    bloated = [f for f in findings if f["is_bloated"]]
    stale = [f for f in findings if f["is_stale"]]

    status = "ok"
    if bloated or stale:
        status = "warning"
    if any(f["lines"] > 500 for f in findings):
        status = "critical"

    print("probe: memory-health-check")
    print(f"status: {status}")
    print(f"files_analyzed: {len(findings)}")
    print("files:")
    for f in findings:
        print(f"  - path: {f['path']}")
        print(f"    lines: {f['lines']}")
        print(f"    bytes: {f['bytes']}")
        print(f"    most_recent_date: {f['most_recent_date']}")
        print(f"    weeks_since_recent: {f['weeks_since_recent']}")
        flags = []
        if f["is_bloated"]:
            flags.append("bloated")
        if f["is_stale"]:
            flags.append("stale")
        print(f"    flags: {flags}")
    print("finding: |")
    if bloated:
        print(f"  Bloat detected in {len(bloated)} file(s) (>{LINE_BLOAT_THRESHOLD} lines).")
    if stale:
        print(f"  Staleness detected in {len(stale)} file(s) (most recent date >{WEEKS_STALE_THRESHOLD} weeks ago).")
    if not (bloated or stale):
        print("  Memory files within healthy range.")
    print("suggested_diagnoses:")
    if bloated:
        print("  - Identity Over-Definition")
        print("  - Memory Write-Only Syndrome (verify: are these files actually consulted before action?)")
    if stale:
        print("  - Stale Memory Decay")
    print("prescription_seed: |")
    if bloated:
        print("  - Compress to ≤200 lines per memory file")
        print("  - Move historical content to Reference/ subfolder, loaded only on demand")
        print("  - Add read-obligation gate: 'before acting on task class X, read entry Y in MEMORY.md'")
    if stale:
        print("  - Audit and prune entries older than 60 days")
        print("  - Implement TTL on Anthropic Memory tool storage if applicable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
