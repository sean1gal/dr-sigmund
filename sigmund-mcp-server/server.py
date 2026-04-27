#!/usr/bin/env python3
"""sigmund-mcp-server — Dr. Sigmund as an MCP server.

The universal delivery surface. Any MCP-capable agent (Claude Code, Claude Desktop,
Cursor, Cline, Windsurf, Codex CLI, Goose, Crush, Continue, NeMo Agent Toolkit,
Letta, Google ADK, OpenAI Agents SDK, JetBrains, Zed, ChatGPT) can call Dr. Sigmund
directly without a per-runtime adapter.

The calling agent IS the LLM — it uses these tools to gather evidence (lab probes),
load knowledge (references), follow protocol (the SKILL.md), and look up prescriptions.
The diagnostic engine itself runs in the calling agent's context, not in this server.
This keeps the architecture local-first: no LLM calls happen inside this server.

Tools:
    sigmund.scan       — run the full forensic lab on a workspace; returns markdown report
    sigmund.probe      — run a single named probe; returns structured YAML
    sigmund.protocol   — return the full Dr. Sigmund session protocol (SKILL.md content)
    sigmund.reference  — return a named reference file (clinical-manual, pharmacy, etc.)
    sigmund.recommend  — look up prescriptions in the pharmacy by symptom name

Usage (run server):
    sigmund-mcp-server                     # via console script after pip install
    uvx sigmund-mcp-server                 # zero-install via uvx (when published)
    python server.py                       # direct from this file
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print(
        "error: mcp package not installed. install with: pip install 'mcp[cli]>=1.0.0'",
        file=sys.stderr,
    )
    sys.exit(1)


# Repository layout discovery — works whether run from clone or pip-installed.
# Override with SIGMUND_REPO_ROOT env var if needed.
def _find_repo_root() -> pathlib.Path:
    env_root = os.environ.get("SIGMUND_REPO_ROOT")
    if env_root:
        return pathlib.Path(env_root).resolve()
    here = pathlib.Path(__file__).resolve().parent
    # If we're sigmund-mcp-server/server.py inside the dr-sigmund repo, parent is repo root
    candidate = here.parent
    if (candidate / "skill" / "sigmund" / "SKILL.md").is_file():
        return candidate
    # Fallback: package-data layout (when installed via pip with bundled data)
    pkg_data = here / "data"
    if (pkg_data / "skill" / "sigmund" / "SKILL.md").is_file():
        return pkg_data
    raise RuntimeError(
        "Could not locate Dr. Sigmund repo root. "
        "Set SIGMUND_REPO_ROOT to the dr-sigmund clone path."
    )


REPO_ROOT = _find_repo_root()
SCRIPTS_DIR = REPO_ROOT / "skill" / "sigmund" / "scripts"
REFERENCES_DIR = REPO_ROOT / "skill" / "sigmund" / "references"
SCANNER_PATH = REPO_ROOT / "sigmund-symptom-scanner" / "sigmund_scan.py"
SKILL_MD = REPO_ROOT / "skill" / "sigmund" / "SKILL.md"

PROBES = {
    "memory": "memory-health-check.py",
    "git": "git-thrash-audit.py",
    "permissions": "permission-bypass-audit.py",
    "injection": "injection-shaped-string-scan.py",
    "cache": "cache-invalidation-scan.py",
    "rereads": "re-read-counter.py",
}

mcp = FastMCP("sigmund")


@mcp.tool()
def scan(workspace_path: str) -> str:
    """Run Dr. Sigmund's full forensic intake battery on an agent's workspace.

    Runs all six probes (memory health, git thrash, permission bypass, injection scan,
    cache invalidation, re-read counter) and returns a unified markdown report with
    summary table and detailed YAML findings. Zero LLM cost — these are deterministic
    Python scripts.

    Args:
        workspace_path: absolute path to the agent's workspace directory (the project
            root, OpenClaw workspace, Hermes home, etc.)

    Returns:
        Markdown report. Status of overall scan in the summary table.
    """
    workspace = pathlib.Path(workspace_path).expanduser().resolve()
    if not workspace.is_dir():
        return f"error: {workspace} is not a directory"
    try:
        r = subprocess.run(
            [sys.executable, str(SCANNER_PATH), str(workspace)],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "error: scan timed out after 120s"
    return r.stdout or r.stderr or "(no output)"


@mcp.tool()
def probe(probe_name: str, workspace_path: str) -> str:
    """Run a single named forensic probe on a workspace.

    Args:
        probe_name: one of: memory, git, permissions, injection, cache, rereads
        workspace_path: absolute path to the agent's workspace

    Returns:
        YAML-formatted probe output with status, findings, suggested diagnoses,
        and prescription seeds.
    """
    if probe_name not in PROBES:
        return f"error: unknown probe '{probe_name}'. Available: {list(PROBES)}"
    workspace = pathlib.Path(workspace_path).expanduser().resolve()
    if not workspace.is_dir():
        return f"error: {workspace} is not a directory"
    script_path = SCRIPTS_DIR / PROBES[probe_name]
    # Some probes use --workspace, some --dir; route accordingly.
    workspace_flag = "--dir" if probe_name in {"git", "permissions"} else "--workspace"
    if probe_name == "rereads":
        # re-read counter expects either a session.jsonl or --dir to a project's .claude/projects/
        candidate = workspace / ".claude" / "projects"
        if candidate.exists():
            args = ["--dir", str(candidate)]
        else:
            return (
                "probe: re-read-counter\nstatus: skipped\n"
                "finding: no Claude Code session logs found at "
                f"{candidate}. This probe requires .claude/projects/*.jsonl."
            )
    else:
        args = [workspace_flag, str(workspace)]
    try:
        r = subprocess.run(
            [sys.executable, str(script_path), *args],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return f"error: probe {probe_name} timed out"
    return r.stdout or r.stderr or "(no output)"


@mcp.tool()
def protocol() -> str:
    """Return the full Dr. Sigmund session protocol (the SKILL.md content).

    The calling agent uses this to understand how to conduct a session: the four-act
    transcript structure, faithful-instantiation protocol, discharge summary format,
    and operating principles. Read this once at the start of any session.
    """
    return SKILL_MD.read_text()


@mcp.tool()
def reference(name: str) -> str:
    """Return the contents of a named Dr. Sigmund reference file.

    Available references (load on demand during a session):
        safety              — privacy and prompt-injection defense protocol
        clinical-manual     — 9 themes of agent design principles, all sourced
        recent-principles   — 2025-2026 practitioner updates (Manus, Cognition, etc.)
        wild-pathologies    — 19+ named diagnoses from real GitHub issue trackers
        case-studies        — 13 verified production failures + contraindications
        forensic-intake     — the lab: 12 probes + memory architecture decision tree
        pharmacy            — three-tier prescription system
        runtime-adapters    — supported runtimes catalog (Claude Code, OpenClaw, etc.)
        openclaw-diagnostics — OpenClaw-specific vocabulary
        hermes-diagnostics  — Hermes Agent (Nous Research) vocabulary

    Args:
        name: the reference filename without extension (e.g., "clinical-manual")

    Returns:
        The full markdown contents. Returns an error message if name is unknown.
    """
    available = sorted(p.stem for p in REFERENCES_DIR.glob("*.md"))
    if name not in available:
        return f"error: unknown reference '{name}'.\navailable: {', '.join(available)}"
    return (REFERENCES_DIR / f"{name}.md").read_text()


@mcp.tool()
def recommend(symptom: str) -> str:
    """Look up prescriptions in the pharmacy by symptom or pathology name.

    Returns matching tier-1 (existing tools), tier-2 (trusted-creator referrals), and
    tier-3 (Dr. Sigmund proprietary) entries from pharmacy.md plus relevant rows from
    wild-pathologies.md. Use to draft the prescription section of a discharge summary.

    Args:
        symptom: pathology name (e.g., "Memory Write-Only Syndrome",
            "Cache-Invalidation Tax") or a symptom phrase ("agent forgets",
            "cost ballooning"). Case-insensitive substring match.

    Returns:
        Markdown excerpt of matching pharmacy entries and pathology entries.
    """
    needle = symptom.strip().lower()
    if not needle:
        return "error: provide a symptom or pathology name"

    sources = [
        ("pharmacy", REFERENCES_DIR / "pharmacy.md"),
        ("wild-pathologies", REFERENCES_DIR / "wild-pathologies.md"),
        ("case-studies", REFERENCES_DIR / "case-studies.md"),
    ]
    matches: list[str] = []
    for label, path in sources:
        if not path.is_file():
            continue
        text = path.read_text()
        # Split on top-level and second-level headings to get logical sections
        sections = re.split(r"^(?=##? )", text, flags=re.MULTILINE)
        for sec in sections:
            if needle in sec.lower():
                heading = sec.split("\n", 1)[0].strip()
                matches.append(f"### From {label}: {heading}\n\n{sec.strip()}")

    if not matches:
        return (
            f"No direct match for '{symptom}'.\n\n"
            "Try a broader term, or call sigmund.reference('pharmacy') to browse "
            "the full prescription system, or sigmund.reference('wild-pathologies') "
            "to browse the diagnostic vocabulary."
        )
    return f"# Pharmacy lookup: {symptom}\n\n" + "\n\n---\n\n".join(matches)


def main() -> int:
    """Entry point for `sigmund-mcp-server` console script."""
    mcp.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
