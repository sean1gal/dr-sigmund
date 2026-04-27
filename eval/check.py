#!/usr/bin/env python3
"""Dr. Sigmund eval — vocabulary and citation regression check.

Runs the lighter version of the eval substrate the v0.4 self-session
prescribed. Fails if:
  - A pathology name was dropped from wild-pathologies.md
  - A required citation was dropped from any reference
  - A probe was dropped from lab.py
  - The reference file count exceeds the hard cap of 5
  - A required reference file is missing

Exit codes:
  0  all checks pass
  1  one or more regressions detected

Run before every release. Per CLAUDE.md rule 3:
  "Releases require an eval delta, not a vibe."
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
REFS = REPO / "skill" / "sigmund" / "references"
LAB = REPO / "skill" / "sigmund" / "lab.py"

sys.path.insert(0, str(HERE))
from expected import (  # noqa: E402
    EXPECTED_CITATIONS,
    EXPECTED_PATHOLOGIES,
    EXPECTED_PROBES,
    EXPECTED_REFERENCES,
    MAX_REFERENCE_FILES,
)


def _load_lab():
    sys.path.insert(0, str(LAB.parent))
    import lab  # type: ignore[import-not-found]
    return lab


def check_pathologies() -> list[str]:
    text = (REFS / "wild-pathologies.md").read_text()
    return sorted(p for p in EXPECTED_PATHOLOGIES if p not in text)


def check_citations() -> list[str]:
    missing = []
    for citation, ref_file in EXPECTED_CITATIONS.items():
        path = REFS / ref_file
        if not path.is_file() or citation not in path.read_text():
            missing.append(f"{citation!r} missing from {ref_file}")
    return sorted(missing)


def check_probes() -> list[str]:
    lab = _load_lab()
    actual = {n for n in dir(lab) if callable(getattr(lab, n)) and not n.startswith("_")}
    return sorted(p for p in EXPECTED_PROBES if p not in actual)


def check_reference_files() -> tuple[list[str], int]:
    actual = {p.name for p in REFS.glob("*.md")}
    missing = sorted(EXPECTED_REFERENCES - actual)
    return missing, len(actual)


def main() -> int:
    failures = []

    missing_pathologies = check_pathologies()
    if missing_pathologies:
        failures.append(f"PATHOLOGIES MISSING ({len(missing_pathologies)}):")
        for p in missing_pathologies:
            failures.append(f"  - {p}")

    missing_citations = check_citations()
    if missing_citations:
        failures.append(f"CITATIONS MISSING ({len(missing_citations)}):")
        for c in missing_citations:
            failures.append(f"  - {c}")

    missing_probes = check_probes()
    if missing_probes:
        failures.append(f"PROBES MISSING from lab.py ({len(missing_probes)}):")
        for p in missing_probes:
            failures.append(f"  - {p}")

    missing_refs, ref_count = check_reference_files()
    if missing_refs:
        failures.append(f"REFERENCE FILES MISSING ({len(missing_refs)}):")
        for r in missing_refs:
            failures.append(f"  - {r}")
    if ref_count > MAX_REFERENCE_FILES:
        failures.append(
            f"REFERENCE COUNT CAP EXCEEDED: {ref_count} files, cap is {MAX_REFERENCE_FILES} "
            "(per v0.4 self-session prescription). Retire one before adding a sixth."
        )

    if failures:
        print("EVAL FAILED")
        print("=" * 60)
        for line in failures:
            print(line)
        print("=" * 60)
        print(f"\n{len(failures)} regression(s) detected.")
        return 1

    print("EVAL PASSED")
    print(f"  pathologies:    {len(EXPECTED_PATHOLOGIES)} present")
    print(f"  citations:      {len(EXPECTED_CITATIONS)} present")
    print(f"  probes:         {len(EXPECTED_PROBES)} present in lab.py")
    print(f"  reference files: {ref_count} (cap {MAX_REFERENCE_FILES})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
