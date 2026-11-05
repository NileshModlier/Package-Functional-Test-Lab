"""Fail the build when an accepted AI case was not reviewed.

Existing catalog cases have no source field and are left unchanged.
Only cases marked source ai-draft, and files still under proposals/, are checked.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "cases"
PROPOSALS = ROOT / "proposals"
TC_RE = re.compile(r"^TC-(INT|VER|TRI)-\d{3}$")
REQ_RE = re.compile(r"^REQ-(INT|VER|TRI)-\d{3}$")


def _field(text: str, name: str) -> str:
    match = re.search(rf"^{name}:\s*(.*)$", text, re.M)
    return match.group(1).strip() if match else ""


def _requirements(text: str) -> list[str]:
    match = re.search(r"^requirement_ids:\n((?:[ \t]*- .*\n)+)", text, re.M)
    if not match:
        return []
    return re.findall(r"REQ-(?:INT|VER|TRI)-\d{3}", match.group(1))


def check() -> list[str]:
    problems = []
    seen = set()
    for path in sorted(CASES.glob("TC-*.yaml")):
        text = path.read_text(encoding="utf-8")
        source = _field(text, "source")
        if source != "ai-draft":
            continue
        case_id = _field(text, "id")
        reviewer = _field(text, "reviewed_by")
        requirements = _requirements(text)
        if not reviewer or reviewer == "null":
            problems.append(f"{path.name} has no reviewer")
        if not requirements:
            problems.append(f"{path.name} lacks a requirement")
        if not source:
            problems.append(f"{path.name} lacks a source")
        if not TC_RE.match(case_id) or path.stem != case_id:
            problems.append(f"{path.name} has an invalid id")
        if case_id in seen:
            problems.append(f"{case_id} is duplicated")
        seen.add(case_id)
        for requirement in requirements:
            if not REQ_RE.match(requirement):
                problems.append(f"{path.name} has an invalid requirement {requirement}")
            if not (ROOT / "requirements" / f"{requirement}.md").is_file():
                problems.append(f"{path.name} cites missing {requirement}")
    if PROPOSALS.is_dir():
        for path in sorted(PROPOSALS.glob("*.yaml")):
            if path.name == "metrics.yaml":
                continue
            text = path.read_text(encoding="utf-8")
            status = _field(text, "status")
            if status == "accepted":
                problems.append(f"{path.name} was accepted but is still in proposals/")
            if status not in {"proposed", "rejected"}:
                problems.append(f"{path.name} has status {status or 'missing'}")
        rejected = PROPOSALS / "rejected"
        if rejected.is_dir():
            for path in sorted(rejected.glob("*.yaml")):
                text = path.read_text(encoding="utf-8")
                if _field(text, "status") != "rejected":
                    problems.append(f"{path.name} is not rejected")
                if not _field(text, "rejection_reason"):
                    problems.append(f"{path.name} has no rejection reason")
                if not _field(text, "reviewed_by") or _field(text, "reviewed_by") == "null":
                    problems.append(f"{path.name} has no reviewer")
    return problems


def main() -> int:
    problems = check()
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print("review gate passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
