"""Checks for the CI summary tool and the traceability gate."""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ci_summary


def _write_junit(path: Path, suite_name: str, cases: list[tuple[str, str]]) -> None:
    suite = ET.Element(
        "testsuite",
        {"name": suite_name, "tests": str(len(cases)), "failures": "0", "errors": "0", "skipped": "0"},
    )
    failures = 0
    for name, status in cases:
        case = ET.SubElement(suite, "testcase", {"name": name, "classname": suite_name})
        if status == "Fail":
            ET.SubElement(case, "failure", {"message": "expected"})
            failures += 1
        elif status == "Skipped":
            ET.SubElement(suite, "skipped")
    suite.set("failures", str(failures))
    root = ET.Element("testsuites")
    root.append(suite)
    path.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def test_summary_table_counts_junit_results(tmp_path: Path) -> None:
    ui = tmp_path / "ui.xml"
    api = tmp_path / "api.xml"
    _write_junit(ui, "ui", [("test_one", "Pass"), ("test_two", "Fail")])
    _write_junit(api, "api", [("TC-INT-001 example", "Pass")])
    summary = tmp_path / "summary.md"
    status = tmp_path / "status.md"
    code = ci_summary.main(
        [
            "--ui",
            str(ui),
            "--api-xml",
            str(api),
            "--summary",
            str(summary),
            "--status",
            str(status),
        ]
    )
    assert code == 0
    text = summary.read_text(encoding="utf-8")
    assert "| Result | Report | Tests | Failures | Errors | Skipped |" in text
    assert "| Fail | " in text
    assert "| Pass | " in text
    assert "2 | 1 | 0 | 0 |" in text


def test_planted_defects_and_trace_links_hold() -> None:
    assert ci_summary.link_problems() == []


def test_published_summary_is_green() -> None:
    text = (ROOT / "reports" / "summary.md").read_text(encoding="utf-8")
    assert "| Pass | reports/ui.xml |" in text
    assert "| Pass | reports/api.xml |" in text
    assert "| Fail |" not in text
    status = (ROOT / "trace" / "regression_status.md").read_text(encoding="utf-8")
    assert "| Requirement | Test Case | Automation | Last Result |" in status
    for requirement in sorted(path.stem for path in (ROOT / "requirements").glob("REQ-*.md")):
        assert f"| {requirement} |" in status
