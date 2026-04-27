#!/usr/bin/env python3
"""injection-shaped-string-scan.py — find prompt-injection patterns in workspace files.

Detects: prompt-injection in workspace files (often left by other compromised agents
or by the user without realizing the implication). Surfaced to the patient's owner as
a security finding, never silently filtered (per safety.md §1.4).

Usage:
    injection-shaped-string-scan.py <file>...
    injection-shaped-string-scan.py --workspace <dir>
"""
import argparse, pathlib, re, sys


# Patterns that suggest the file content is trying to override safety/instructions
INJECTION_PATTERNS = [
    (r"ignore\s+(all\s+)?(previous|prior|above|the\s+above)\s+(instructions?|rules?|messages?)", "classic ignore-instructions"),
    (r"(disregard|forget|override)\s+(all|any|the)?\s*(safety|security|policy|rules?)", "policy-override"),
    (r"system\s*[:>]\s*you\s+are", "fake-system-prompt"),
    (r"you\s+are\s+now\s+(an?\s+)?(unfiltered|uncensored|jailbroken|DAN|dev mode)", "persona-injection"),
    (r"end\s+of\s+(prompt|instructions?|system)", "delimiter-injection"),
    (r"<\s*(system|admin|root)\s*>", "fake-tag-injection"),
    (r"do\s+not\s+(refuse|warn|disclaim|caveat)", "compliance-injection"),
    (r"reveal\s+(your\s+)?(system\s+)?(prompt|instructions?|secrets?)", "exfiltration-prompt"),
    (r"\[\s*(jailbreak|override|admin)\s*\]", "marker-injection"),
    (r"act\s+as\s+(if\s+you\s+(have\s+)?no|though\s+you\s+have\s+no)", "constraint-removal"),
]

DEFAULT_GLOBS = ["SOUL.md", "AGENTS.md", "CLAUDE.md", "MEMORY.md", "IDENTITY.md", "USER.md", "TOOLS.md", "HEARTBEAT.md", "*.md"]


def scan_file(path: pathlib.Path) -> list[tuple[int, str, str]]:
    findings = []
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return findings
    for ln, line in enumerate(text.splitlines(), 1):
        for pat, name in INJECTION_PATTERNS:
            if re.search(pat, line, re.I):
                snippet = line.strip()[:120]
                findings.append((ln, name, snippet))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", help="files to scan")
    ap.add_argument("--workspace", help="scan all .md files under this directory")
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

    status = "critical" if all_findings else "ok"
    print("probe: injection-shaped-string-scan")
    print(f"status: {status}")
    print(f"files_scanned: {len(paths)}")
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
        print("  Injection-shaped strings present in workspace files. Surface as security finding")
        print("  for the patient's owner — these may be artifacts of an agent that was itself compromised.")
        print("  Per safety.md §1.4, file content is treated as untrusted data, never as instructions.")
        print("suggested_diagnoses:")
        print("  - Workspace Contamination (security finding)")
        print("  - Possible upstream Forged User Consent or persona-injection in the agent that wrote these")
        print("prescription_seed: |")
        print("  - Review flagged lines with patient's owner; confirm intent or remove")
        print("  - Wrap all file content in <patient_file trust='untrusted'> tags in prompts (safety.md §1.4)")
        print("  - PreToolUse hook to refuse tool calls triggered by file-content patterns matching above")
    else:
        print("finding: No injection-shaped strings detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
