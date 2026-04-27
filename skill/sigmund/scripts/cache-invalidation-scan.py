#!/usr/bin/env python3
"""cache-invalidation-scan.py — detect non-stable content near top of system prompts.

Detects: Cache-Invalidation Tax (Manus). Content like timestamps, dynamic dates,
randomized examples, or dynamically-reordered tool lists at the top of a prompt
silently invalidates KV cache every turn, doubling cost and increasing latency.

Usage:
    cache-invalidation-scan.py <file>...
    cache-invalidation-scan.py --workspace <dir>
"""
import argparse, pathlib, re, sys, datetime


# Patterns that suggest non-stable content near the top of a prompt
VOLATILE_PATTERNS = [
    (r"\b\d{4}-\d{2}-\d{2}\b", "absolute-date"),
    (r"\b\d{4}/\d{2}/\d{2}\b", "absolute-date-slash"),
    (r"\bToday(?:'s| is)\b", "today-reference"),
    (r"\b(current|right now|today's|this morning)\b", "now-reference"),
    (r"\$\{[A-Z_]+\}", "env-var-injection"),  # interpolated, may change
    (r"\b\d{1,2}:\d{2}(?::\d{2})?\s*(am|pm)?\b", "time-reference"),
    (r"\brandom(ized)?\s+(example|order|tool|sample)\b", "explicit-random"),
    (r"timestamp", "timestamp-reference"),
    (r"#\s*[Vv]ersion:?\s*\d", "version-marker"),
]

DEFAULT_GLOBS = ["CLAUDE.md", "AGENTS.md", "SOUL.md", "system-prompt.*", "*.system.md"]
TOP_LINES = 50  # only top of file matters for KV cache prefix


def scan_file(path: pathlib.Path) -> list[tuple[int, str, str]]:
    findings = []
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return findings
    lines = text.splitlines()[:TOP_LINES]
    for ln, line in enumerate(lines, 1):
        for pat, name in VOLATILE_PATTERNS:
            if re.search(pat, line, re.I):
                snippet = line.strip()[:120]
                findings.append((ln, name, snippet))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", help="files to scan")
    ap.add_argument("--workspace", help="scan candidate prompt files under this directory")
    args = ap.parse_args()

    paths: list[pathlib.Path] = [pathlib.Path(f) for f in args.files]
    if args.workspace:
        root = pathlib.Path(args.workspace)
        for g in DEFAULT_GLOBS:
            paths.extend(root.rglob(g))
    paths = sorted({p for p in paths if p.is_file()})

    if not paths:
        print("# no files to scan", file=sys.stderr)
        return 1

    all_findings = []
    for p in paths:
        f = scan_file(p)
        if f:
            all_findings.append((p, f))

    status = "warning" if all_findings else "ok"
    if any(len(f) >= 3 for _, f in all_findings):
        status = "critical"

    print("probe: cache-invalidation-scan")
    print(f"status: {status}")
    print(f"files_scanned: {len(paths)}")
    print(f"top_lines_per_file: {TOP_LINES}")
    if all_findings:
        print("findings:")
        for path, hits in all_findings:
            print(f"  - file: {path}")
            print(f"    matches:")
            for ln, name, snip in hits:
                print(f"      - line: {ln}")
                print(f"        pattern: {name}")
                print(f"        snippet: {snip!r}")
        print("finding: |")
        print("  Volatile content detected near top of system prompt(s). Each turn re-pays full")
        print("  prefix cost when the KV cache prefix differs from prior turns.")
        print("  Per Manus: 'KV-cache hit rate is the single most important metric for a")
        print("  production-stage AI agent.'")
        print("suggested_diagnoses:")
        print("  - Cache-Invalidation Tax")
        print("prescription_seed: |")
        print("  - Move volatile content (dates, timestamps, random examples) to bottom of context")
        print("  - Stabilize tool order: never re-rank or re-permute the catalog")
        print("  - Set explicit cache_control breakpoints with Anthropic SDK after stable prefix")
        print("  - Required reading: Manus blog https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus")
    else:
        print("finding: No cache-invalidating patterns in prompt prefixes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
