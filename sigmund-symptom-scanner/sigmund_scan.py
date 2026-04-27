#!/usr/bin/env python3
"""sigmund-scan — forensic intake battery for AI agents.

Thin CLI over skill/sigmund/lab.py. The lab is the engine; this script is
just argparse + stdout.

Usage:
    sigmund-scan <workspace>                 # full battery, markdown report
    sigmund-scan <workspace> --probe memory  # single named probe, YAML
    sigmund-scan <workspace> -o report.md    # write to file

Exit codes: 0 clean, 1 warnings, 2 critical.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

# Add the lab module to the path. Works from clone or symlinked install.
_HERE = pathlib.Path(__file__).resolve().parent
_LAB = _HERE.parent / "skill" / "sigmund"
if str(_LAB) not in sys.path:
    sys.path.insert(0, str(_LAB))

from lab import (  # noqa: E402
    PROBE_DESCRIPTIONS,
    all_probes,
    cache_invalidation,
    git_thrash,
    memory_health,
    permission_bypass,
    re_read_counter,
    render_report,
)

PROBES = {
    "memory": memory_health,
    "git": git_thrash,
    "permissions": permission_bypass,
    "cache": cache_invalidation,
    "rereads": re_read_counter,
}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Sigmund Symptom Scanner — forensic intake battery for AI agents.",
    )
    ap.add_argument("workspace", type=pathlib.Path)
    ap.add_argument("--output", "-o", type=pathlib.Path)
    ap.add_argument("--probe", choices=list(PROBES))
    args = ap.parse_args()

    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        print(f"error: {workspace} is not a directory", file=sys.stderr)
        return 2

    if args.probe:
        finding = PROBES[args.probe](workspace)
        print(finding.to_yaml())
        return {"critical": 2, "warning": 1}.get(finding.status, 0)

    findings = all_probes(workspace)
    report = render_report(workspace, findings)
    if args.output:
        args.output.write_text(report)
        print(f"wrote report to {args.output}", file=sys.stderr)
    else:
        print(report)

    statuses = {f.status for f in findings}
    return 2 if "critical" in statuses else 1 if "warning" in statuses else 0


if __name__ == "__main__":
    sys.exit(main())
