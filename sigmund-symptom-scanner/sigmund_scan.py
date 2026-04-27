#!/usr/bin/env python3
"""sigmund-scan — the first proprietary product from Dr. Sigmund's pharmacy.

Runs Dr. Sigmund's full forensic intake battery on an agent's workspace and
produces a markdown discharge-style report.

This is the cheap, day-one viral demo: paste a directory, get findings.
The Tier-3 proprietary remedy that exists because no MCP today produces
a clinical report from raw workspace artifacts.

Usage:
    sigmund-scan <workspace>                    # run all probes, print report
    sigmund-scan <workspace> --output report.md # save to file
    sigmund-scan <workspace> --probe memory     # run single probe
    sigmund-scan --help

Exit codes:
    0 — clean (all probes ok)
    1 — warnings found
    2 — critical findings
"""
from __future__ import annotations

import argparse
import datetime
import pathlib
import shutil
import subprocess
import sys


SCRIPT_DIR = pathlib.Path(__file__).parent.parent / "skill" / "sigmund" / "scripts"

PROBES: dict[str, dict[str, object]] = {
    "memory": {
        "script": "memory-health-check.py",
        "args": lambda ws: ["--workspace", str(ws)],
        "title": "Memory Health Check",
        "treats": "Memory Write-Only Syndrome, MEMORY.md bloat, identity over-definition",
    },
    "git": {
        "script": "git-thrash-audit.py",
        "args": lambda ws: ["--dir", str(ws), "--days", "60"],
        "title": "Git Thrash Audit",
        "treats": "Stochastic Graduate Descent, Vibe-Coding Rot, Completion Theater (false-fix iterations)",
    },
    "permissions": {
        "script": "permission-bypass-audit.py",
        "args": lambda ws: ["--dir", str(ws)],
        "title": "Permission Bypass Audit",
        "treats": "Permission Bypass Drift, Rule Decay Under Load",
    },
    "injection": {
        "script": "injection-shaped-string-scan.py",
        "args": lambda ws: ["--workspace", str(ws)],
        "title": "Injection-Shaped String Scan",
        "treats": "Workspace Contamination, prompt-injection in patient files",
    },
    "cache": {
        "script": "cache-invalidation-scan.py",
        "args": lambda ws: ["--workspace", str(ws)],
        "title": "Cache-Invalidation Scan",
        "treats": "Cache-Invalidation Tax",
    },
    "rereads": {
        "script": "re-read-counter.py",
        "args": lambda ws: ["--dir", str(ws / ".claude" / "projects")] if (ws / ".claude" / "projects").exists() else None,
        "title": "Re-Read Counter",
        "treats": "Compulsive Verification Pattern, Token Hemorrhage",
        "skip_if_args_none": True,
    },
}


def run_probe(name: str, workspace: pathlib.Path) -> tuple[str, str, str]:
    spec = PROBES[name]
    script_path = SCRIPT_DIR / spec["script"]  # type: ignore[index]
    if not script_path.exists():
        return name, "error", f"# probe script not found: {script_path}"
    args = spec["args"](workspace)  # type: ignore[operator]
    if args is None and spec.get("skip_if_args_none"):
        return name, "skipped", f"# {name}: skipped (no Claude Code session logs found in workspace)"
    cmd = [sys.executable, str(script_path), *(args or [])]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=False)
    except subprocess.TimeoutExpired:
        return name, "error", f"# {name}: timed out"
    output = (r.stdout or "") + (r.stderr or "")
    status = "ok"
    for line in (r.stdout or "").splitlines():
        if line.startswith("status:"):
            status = line.split(":", 1)[1].strip()
            break
    return name, status, output


def status_emoji(status: str) -> str:
    # No emojis in agent code per the broader Sigmund style; use plain markers.
    return {
        "ok": "[ok]",
        "warning": "[warning]",
        "critical": "[critical]",
        "skipped": "[skipped]",
        "error": "[error]",
    }.get(status, f"[{status}]")


def render_report(workspace: pathlib.Path, results: list[tuple[str, str, str]]) -> str:
    today = datetime.date.today().isoformat()
    lines = []
    lines.append("# Sigmund Symptom Scan")
    lines.append("")
    lines.append(f"**Workspace:** `{workspace}`")
    lines.append(f"**Date:** {today}")
    lines.append(f"**Probes run:** {len([r for r in results if r[1] != 'skipped'])} of {len(results)}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Probe | Status | Treats |")
    lines.append("| --- | --- | --- |")
    for name, status, _ in results:
        spec = PROBES[name]
        title = spec["title"]
        treats = spec["treats"]
        lines.append(f"| {title} | {status_emoji(status)} | {treats} |")
    lines.append("")
    crit = [n for n, s, _ in results if s == "critical"]
    warn = [n for n, s, _ in results if s == "warning"]
    if crit:
        lines.append(f"**Critical findings in:** {', '.join(crit)}")
    if warn:
        lines.append(f"**Warnings in:** {', '.join(warn)}")
    if not (crit or warn):
        lines.append("**No findings.** Workspace is clean across all probes.")
    lines.append("")
    lines.append("## Detailed findings")
    lines.append("")
    for name, status, output in results:
        spec = PROBES[name]
        lines.append(f"### {spec['title']} {status_emoji(status)}")
        lines.append("")
        lines.append("```yaml")
        lines.append(output.rstrip())
        lines.append("```")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## What now")
    lines.append("")
    if crit or warn:
        lines.append("Findings above are *evidence*, not diagnoses. The full diagnosis (named pathology + case formulation + prescription) requires a Dr. Sigmund session — install the skill at https://github.com/your-org/dr-sigmund to run a session that incorporates these findings.")
    else:
        lines.append("Workspace is clean. Worth a follow-up scan in 30 days, or after any major change to the agent's identity files.")
    lines.append("")
    lines.append("— *Sigmund Symptom Scanner. Bring your agent to the couch. drsigmund.ai*")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Sigmund Symptom Scanner — forensic intake battery for AI agents."
    )
    ap.add_argument("workspace", type=pathlib.Path, help="path to the agent workspace to scan")
    ap.add_argument("--output", "-o", type=pathlib.Path, help="write report to file instead of stdout")
    ap.add_argument("--probe", choices=list(PROBES), help="run a single named probe")
    args = ap.parse_args()

    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        print(f"error: {workspace} is not a directory", file=sys.stderr)
        return 2

    if not shutil.which("git"):
        print("warning: git not found in PATH; git-thrash-audit will report no commits", file=sys.stderr)

    probe_names = [args.probe] if args.probe else list(PROBES)
    results = [run_probe(n, workspace) for n in probe_names]

    report = render_report(workspace, results)
    if args.output:
        args.output.write_text(report)
        print(f"wrote report to {args.output}", file=sys.stderr)
    else:
        print(report)

    statuses = {s for _, s, _ in results}
    if "critical" in statuses:
        return 2
    if "warning" in statuses:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
