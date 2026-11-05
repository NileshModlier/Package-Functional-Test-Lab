"""Checks for the proposal drafter and the review gate."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ai_assistant import (  # noqa: E402
    CASES,
    _proposal,
    main,
    read_cases,
    validate,
)
from check_reviewed import check  # noqa: E402


def test_unknown_term_is_invalid():
    proposal = _proposal(
        "REQ-INT-003",
        "Store biometric_signature",
        "exploratory",
        ["Store biometric_signature on the record."],
        ["biometric_signature is saved."],
        "Introduces biometric_signature.",
    )
    assert validate(proposal, "Enrolled Passed Failed", []) == "invalid"


def test_copied_title_is_duplicate():
    cases = read_cases()
    related = next(case for case in cases if "REQ-INT-003" in case["requirements"])
    proposal = _proposal(
        "REQ-INT-003",
        related["title"],
        "negative",
        [related["title"]],
        [related["title"]],
        "Restatement of an existing case.",
    )
    assert validate(proposal, related["text"], cases) == "duplicate"


def test_propose_requires_eight_to_ten_requirements():
    assert main(["propose", "--requirements", "REQ-INT-001"]) == 1


def test_review_gate_passes_the_catalog():
    assert check() == []


def test_ai_case_without_a_reviewer_fails():
    path = CASES / "TC-INT-099.yaml"
    path.write_text(
        "id: TC-INT-099\nsource: ai-draft\nreviewed_by: null\n"
        "requirement_ids:\n  - REQ-INT-003\n",
        encoding="utf-8",
    )
    try:
        problems = check()
        assert any("no reviewer" in item for item in problems)
    finally:
        path.unlink()


def test_accepted_cases_are_new_files():
    drafts = list(CASES.glob("TC-*.yaml"))
    ai_cases = [path for path in drafts if "source: ai-draft" in path.read_text(encoding="utf-8")]
    assert len(ai_cases) == 8
    assert (CASES / "TC-INT-001.yaml").is_file()
    assert "source: ai-draft" not in (CASES / "TC-INT-001.yaml").read_text(encoding="utf-8")
