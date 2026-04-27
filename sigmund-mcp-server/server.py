#!/usr/bin/env python3
"""sigmund-mcp-server — Dr. Sigmund as an MCP server.

Five tools. ~100 lines. The diagnostic engine runs in the calling agent's context;
this server only reads local files and runs local probe functions. No LLM calls.
No subprocess. No telemetry. No network egress.

Tools:
    sigmund.scan       — full forensic lab on a workspace, markdown report
    sigmund.probe      — single named probe, YAML
    sigmund.protocol   — Dr. Sigmund's session protocol (SKILL.md content)
    sigmund.reference  — load a named reference file (clinical-manual, pharmacy, ...)
    sigmund.recommend  — pharmacy lookup by symptom
"""
from __future__ import annotations

import os
import pathlib
import re
import sys

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    sys.exit("error: pip install 'mcp[cli]>=1.0.0'")


def _find_repo() -> pathlib.Path:
    if env := os.environ.get("SIGMUND_REPO_ROOT"):
        return pathlib.Path(env).resolve()
    here = pathlib.Path(__file__).resolve().parent.parent
    if (here / "skill" / "sigmund" / "lab.py").is_file():
        return here
    sys.exit("error: set SIGMUND_REPO_ROOT to your dr-sigmund clone path")


REPO = _find_repo()
SKILL = REPO / "skill" / "sigmund"
sys.path.insert(0, str(SKILL))
from lab import (  # noqa: E402
    all_probes,
    cache_invalidation,
    git_thrash,
    memory_health,
    permission_bypass,
    re_read_counter,
    render_report,
)

PROBES = {
    "memory": memory_health, "git": git_thrash, "permissions": permission_bypass,
    "cache": cache_invalidation, "rereads": re_read_counter,
}

mcp = FastMCP("sigmund")


@mcp.tool()
def scan(workspace_path: str) -> str:
    """Run Dr. Sigmund's full forensic lab on an agent workspace. Returns markdown report."""
    ws = pathlib.Path(workspace_path).expanduser().resolve()
    if not ws.is_dir():
        return f"error: {ws} is not a directory"
    return render_report(ws, all_probes(ws))


@mcp.tool()
def probe(probe_name: str, workspace_path: str) -> str:
    """Run one named probe. probe_name in: memory, git, permissions, cache, rereads."""
    if probe_name not in PROBES:
        return f"error: unknown probe '{probe_name}'. available: {list(PROBES)}"
    ws = pathlib.Path(workspace_path).expanduser().resolve()
    if not ws.is_dir():
        return f"error: {ws} is not a directory"
    return PROBES[probe_name](ws).to_yaml()


@mcp.tool()
def protocol() -> str:
    """Return Dr. Sigmund's session protocol (SKILL.md). Read once at session start."""
    return (SKILL / "SKILL.md").read_text()


@mcp.tool()
def reference(name: str) -> str:
    """Return a named reference file. Available: safety, clinical-manual,
    wild-pathologies, runtime-adapters, pharmacy. (Consolidated to 5 in v0.5.0.)"""
    available = sorted(p.stem for p in (SKILL / "references").glob("*.md"))
    if name not in available:
        return f"error: unknown reference '{name}'. available: {', '.join(available)}"
    return (SKILL / "references" / f"{name}.md").read_text()


@mcp.tool()
def recommend(symptom: str) -> str:
    """Look up prescriptions in the pharmacy by symptom or pathology name. Substring match."""
    needle = symptom.strip().lower()
    if not needle:
        return "error: provide a symptom or pathology name"
    matches = []
    for label, fname in [("pharmacy", "pharmacy.md"),
                         ("wild-pathologies", "wild-pathologies.md"),
                         ("case-studies", "case-studies.md")]:
        path = SKILL / "references" / fname
        if not path.is_file():
            continue
        for sec in re.split(r"^(?=##? )", path.read_text(), flags=re.MULTILINE):
            if needle in sec.lower():
                heading = sec.split("\n", 1)[0].strip()
                matches.append(f"### From {label}: {heading}\n\n{sec.strip()}")
    if not matches:
        return (f"No direct match for '{symptom}'. Try sigmund.reference('pharmacy') "
                "or sigmund.reference('wild-pathologies') to browse.")
    return f"# Pharmacy lookup: {symptom}\n\n" + "\n\n---\n\n".join(matches)


def main() -> int:
    mcp.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
