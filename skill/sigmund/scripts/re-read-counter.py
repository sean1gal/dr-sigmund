#!/usr/bin/env python3
"""re-read-counter.py — count repeated Read tool calls in a Claude Code session.

Detects: Compulsive Re-reading, Token Hemorrhage, Memory Write-Only Syndrome (when
files in MEMORY.md are also among the most re-read).

Usage:
    re-read-counter.py <session.jsonl>           # single Claude Code session log
    re-read-counter.py --dir <project-dir>       # scan all sessions for a project
"""
import json, sys, collections, pathlib, argparse


def parse_session(path: pathlib.Path) -> collections.Counter:
    """Count Read tool calls per file_path in a JSONL session log."""
    counts: collections.Counter = collections.Counter()
    try:
        with path.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = rec.get("message", {})
                content = msg.get("content", [])
                if not isinstance(content, list):
                    continue
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "tool_use" and block.get("name") == "Read":
                        fp = (block.get("input") or {}).get("file_path", "")
                        if fp:
                            counts[fp] += 1
    except OSError as e:
        print(f"# warning: could not read {path}: {e}", file=sys.stderr)
    return counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("session", nargs="?", help="path to a session.jsonl")
    ap.add_argument("--dir", help="scan all .jsonl under this directory")
    ap.add_argument("--threshold", type=int, default=3, help="flag files read more than N times (default 3)")
    args = ap.parse_args()

    counts: collections.Counter = collections.Counter()
    if args.dir:
        root = pathlib.Path(args.dir)
        for p in root.rglob("*.jsonl"):
            counts.update(parse_session(p))
    elif args.session:
        counts = parse_session(pathlib.Path(args.session))
    else:
        ap.print_help()
        return 1

    flagged = [(p, c) for p, c in counts.most_common() if c > args.threshold]
    total_reads = sum(counts.values())
    distinct_files = len(counts)

    print("probe: re-read-counter")
    print(f"status: {'critical' if flagged else 'ok'}")
    print(f"total_reads: {total_reads}")
    print(f"distinct_files: {distinct_files}")
    if flagged:
        print("flagged_files:")
        for p, c in flagged:
            print(f"  - path: {p}")
            print(f"    reads: {c}")
        print("finding: |")
        print(f"  Compulsive Re-reading detected. {len(flagged)} file(s) read more than {args.threshold} times.")
        print(f"  Estimated wasted tokens: ~{sum(c - 1 for _, c in flagged) * 1500} (assuming ~1500 tok/read).")
        print("suggested_diagnoses:")
        print("  - Compulsive Verification Pattern")
        print("  - Token Hemorrhage")
        print("  - Memory Write-Only Syndrome (verify: are these files referenced in MEMORY.md but not consulted?)")
        print("prescription_seed: |")
        print("  - sigmund-token-meter MCP for live alerting")
        print("  - Serena MCP for symbol-level retrieval instead of full-file reads")
        print("  - Anthropic Memory Tool with read-obligation gate in system prompt")
    else:
        print("finding: No re-read pattern detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
