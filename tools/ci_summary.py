"""Build the CI summary, combined API report, and regression status.

Reads JUnit XML. Writes a markdown table and trace/regression_status.md.
Appends the summary to GITHUB_STEP_SUMMARY when that variable is set.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TC_RE = re.compile(r"TC-[A-Z]+-\d+")
REQ_RE = re.compile(r"REQ-[A-Z]+-\d+")
DEFECTS = (
    "pass_mark",
    "certificate_date",
    "quality_score",
    "inactive_assignment",
    "invalid_completion",
    "reopen_closed",
)
# An assertion the planted switch must break. Same function as the UI disable,
# and present in the Postman collection that leaves the switch on.
DEFECT_ASSERTIONS = {
    "pass_mark": "Passed",
    "certificate_date": "expect_certificate_dates_match",
    "quality_score": "Score 70.0",
    "inactive_assignment": "inactive technician",
    "invalid_completion": "APPR -> COMP",
    "reopen_closed": "CLOSE -> INPRG",
}
POSTMAN_ASSERTIONS = {
    "pass_mark": "score 80.00 passes",
    "certificate_date": "issued date matches completion",
    "quality_score": "weighted score is 70",
    "inactive_assignment": "inactive technician is rejected",
    "invalid_completion": "APPR cannot complete",
    "reopen_closed": "closed order stays closed",
}
RANK = {"Not run": 0, "Pass": 1, "Skipped": 2, "Error": 3, "Fail": 4}


def worse(left: str, right: str) -> str:
    return left if RANK[left] >= RANK[right] else right


def suites_of(path: Path) -> list[ET.Element]:
    root = ET.parse(path).getroot()
    if root.tag == "testsuite":
        return [root]
    return list(root.findall("testsuite"))


def suite_stats(suites: list[ET.Element]) -> dict[str, int]:
    totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    for suite in suites:
        for key in totals:
            totals[key] += int(suite.get(key) or 0)
    return totals


def case_status(case: ET.Element) -> str:
    if case.find("failure") is not None:
        return "Fail"
    if case.find("error") is not None:
        return "Error"
    if case.find("skipped") is not None:
        return "Skipped"
    return "Pass"


def result_label(stats: dict[str, int], present: bool) -> str:
    if not present:
        return "Fail"
    if stats["failures"] or stats["errors"]:
        return "Fail"
    return "Pass"


def summary_table(rows: list[tuple[str, str, dict[str, int]]]) -> str:
    lines = [
        "# Test summary",
        "",
        "**Identifier:** SIMULATED",
        "",
        "| Result | Report | Tests | Failures | Errors | Skipped |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for result, report, stats in rows:
        lines.append(
            f"| {result} | {report} | {stats['tests']} | {stats['failures']} | {stats['errors']} | {stats['skipped']} |"
        )
    lines.append("")
    return "\n".join(lines)


def merge_junit(parts: list[Path], destination: Path) -> list[ET.Element]:
    combined = ET.Element("testsuites", {"name": "Package Sim API"})
    suites: list[ET.Element] = []
    for part in parts:
        suites.extend(suites_of(part))
    for suite in suites:
        combined.append(suite)
    totals = suite_stats(list(combined))
    for key, value in totals.items():
        combined.set(key, str(value))
    destination.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(combined).write(destination, encoding="utf-8", xml_declaration=True)
    return list(combined)


def merge_json(parts: list[Path], destination: Path, force_defects: bool) -> None:
    runs = []
    for part in parts:
        payload = json.loads(part.read_text(encoding="utf-8"))
        name = payload.get("collection", {}).get("info", {}).get("name", part.stem)
        runs.append({"name": name, "run": payload})
    destination.write_text(
        json.dumps(
            {
                "simulated": True,
                "milestone": "M6",
                "forceDefects": force_defects,
                "collections": runs,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def _requirement_blocks(case_text: str) -> list[str]:
    match = re.search(r"requirement_ids:\n((?:[ \t]*- .+\n)+)", case_text)
    if not match:
        return []
    return REQ_RE.findall(match.group(1))


def catalog() -> dict[str, list[str]]:
    cases: dict[str, list[str]] = {}
    for path in sorted((ROOT / "cases").glob("TC-*.yaml")):
        text = path.read_text(encoding="utf-8")
        case_id = re.search(r"^id:\s+(TC-[A-Z]+-\d+)", text, re.M)
        if not case_id:
            continue
        cases[case_id.group(1)] = _requirement_blocks(text)
    return cases


def ui_tests() -> dict[str, set[str]]:
    """Map a pytest function name to the TC ids in its docstring."""
    found: dict[str, set[str]] = {}
    for path in sorted((ROOT / "tests" / "ui").glob("test_*.py")):
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"def (test_\w+)\(.*?\n\s+\"\"\"(.*?)\"\"\"", text, re.S):
            found[match.group(1)] = set(TC_RE.findall(match.group(2)))
    return found


def newman_names() -> dict[str, set[str]]:
    """Map a TC id to Postman request names."""
    found: dict[str, set[str]] = {}
    for path in sorted((ROOT / "postman" / "collections").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))

        def walk(items: list[dict]) -> None:
            for item in items:
                if "item" in item:
                    walk(item["item"])
                    continue
                for case_id in TC_RE.findall(item.get("name", "")):
                    found.setdefault(case_id, set()).add(item["name"])

        walk(data.get("item", []))
    return found


def junit_results(paths: list[Path], functions: dict[str, set[str]]) -> dict[str, str]:
    results: dict[str, str] = {}
    for path in paths:
        if not path.is_file():
            continue
        for suite in suites_of(path):
            suite_name = suite.get("name") or ""
            for case in suite.findall("testcase"):
                status = case_status(case)
                name = (case.get("name") or "").split("[", 1)[0]
                if name in functions:
                    for case_id in functions[name]:
                        results[case_id] = worse(results.get(case_id, "Not run"), status)
                    continue
                ids = TC_RE.findall(case.get("name") or "")
                if not ids:
                    ids = TC_RE.findall(suite_name)
                for case_id in ids:
                    results[case_id] = worse(results.get(case_id, "Not run"), status)
    return results


def write_status(path: Path, ui_xml: Path, api_xml: Path) -> str:
    cases = catalog()
    functions = ui_tests()
    requests = newman_names()
    results = junit_results([ui_xml, api_xml], functions)
    ui_case_ids = {case_id for ids in functions.values() for case_id in ids}
    lines = [
        "# Regression status",
        "",
        "**Milestone:** M6",
        "**Identifier:** SIMULATED",
        "**Generated from:** `reports/ui.xml` and `reports/api.xml`",
        "",
        "| Requirement | Test Case | Automation | Last Result |",
        "| --- | --- | --- | --- |",
    ]
    for case_id in sorted(cases):
        labels: list[str] = []
        if case_id in ui_case_ids:
            funcs = sorted(name for name, ids in functions.items() if case_id in ids)
            labels.append(f"AUTO-{case_id.removeprefix('TC-')} ({', '.join(funcs)})")
        for request_name in sorted(requests.get(case_id, ())):
            labels.append(f"Newman {request_name}")
        automation = "; ".join(labels) if labels else "—"
        result = results.get(case_id, "Not run")
        requirements = cases[case_id] or ["—"]
        for requirement in requirements:
            lines.append(f"| {requirement} | {case_id} | {automation} | {result} |")
    lines.append("")
    text = "\n".join(lines)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return text


def link_problems() -> list[str]:
    problems: list[str] = []
    cases = catalog()
    requirement_ids = {
        path.stem
        for path in (ROOT / "requirements").glob("REQ-*.md")
    }
    covered = {requirement for reqs in cases.values() for requirement in reqs}
    for requirement in sorted(requirement_ids - covered):
        problems.append(f"orphan requirement {requirement}")
    for case_id, reqs in cases.items():
        unknown = [requirement for requirement in reqs if requirement not in requirement_ids]
        for requirement in unknown:
            problems.append(f"{case_id} cites missing requirement {requirement}")

    ui_root = ROOT / "tests" / "ui"
    for path in sorted(ui_root.glob("test_*.py")):
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"def (test_\w+)\(.*?\n\s+\"\"\"(.*?)\"\"\"", text, re.S):
            name, doc = match.group(1), match.group(2)
            cited = TC_RE.findall(doc)
            if not cited:
                problems.append(f"orphan automated test {name}")
                continue
            for case_id in cited:
                if case_id not in cases:
                    problems.append(f"orphan automated test {name} cites missing {case_id}")
                    continue
                for requirement in REQ_RE.findall(doc):
                    if requirement not in cases[case_id]:
                        problems.append(
                            f"orphan automated test {name} cites {requirement} outside {case_id}"
                        )

    for path in sorted((ROOT / "postman" / "collections").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))

        def walk(items: list[dict]) -> None:
            for item in items:
                if "item" in item:
                    walk(item["item"])
                    continue
                for case_id in TC_RE.findall(item.get("name", "")):
                    if case_id not in cases:
                        problems.append(
                            f"orphan Postman request {item['name']} cites missing {case_id}"
                        )

        walk(data.get("item", []))

    ui_text = "\n".join(path.read_text(encoding="utf-8") for path in ui_root.glob("test_*.py"))
    postman_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "postman" / "collections").glob("*.json")
    )
    for defect in DEFECTS:
        parts = re.split(r"\ndef ", ui_text)
        needle = f'disable("{defect}")'
        assertion = DEFECT_ASSERTIONS[defect]
        if not any(needle in part and assertion in part for part in parts):
            problems.append(f"planted defect {defect} does not fail a UI test")
        if f"Disable {defect}" not in postman_text or POSTMAN_ASSERTIONS[defect] not in postman_text:
            problems.append(f"planted defect {defect} does not fail a Postman test")
    return problems


def append_step_summary(markdown: str) -> None:
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if not target:
        return
    with open(target, "a", encoding="utf-8") as handle:
        handle.write(markdown)
        if not markdown.endswith("\n"):
            handle.write("\n")


def build(args: argparse.Namespace) -> int:
    ui_path = args.ui
    api_parts = args.api_part or []
    if api_parts:
        suites = merge_junit(api_parts, args.api_xml)
    elif args.api_xml.is_file():
        suites = suites_of(args.api_xml)
    else:
        suites = []
    if args.json_part:
        merge_json(args.json_part, args.api_json, args.force_defects)

    rows = []
    missing = False
    if ui_path.is_file():
        ui_stats = suite_stats(suites_of(ui_path))
        rows.append((result_label(ui_stats, True), ui_path.as_posix(), ui_stats))
    else:
        missing = True
        rows.append(("Fail", ui_path.as_posix(), {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}))
    if suites:
        api_stats = suite_stats(suites)
        rows.append((result_label(api_stats, True), args.api_xml.as_posix(), api_stats))
    else:
        missing = True
        rows.append(("Fail", args.api_xml.as_posix(), {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}))

    markdown = summary_table(rows)
    if args.force_defects:
        markdown += "\nPlanted defects were forced ON. Failing tests are the expected result.\n"
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(markdown, encoding="utf-8")
    append_step_summary(markdown)
    if ui_path.is_file() or args.api_xml.is_file():
        write_status(args.status, ui_path, args.api_xml)

    problems = link_problems() if args.check else []
    for problem in problems:
        print(problem, file=sys.stderr)
    if missing or problems:
        return 1
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write the regression summary from JUnit XML.")
    parser.add_argument("--ui", type=Path, default=ROOT / "reports" / "ui.xml")
    parser.add_argument("--api-part", type=Path, action="append", default=[])
    parser.add_argument("--json-part", type=Path, action="append", default=[])
    parser.add_argument("--summary", type=Path, default=ROOT / "reports" / "summary.md")
    parser.add_argument("--api-xml", type=Path, default=ROOT / "reports" / "api.xml")
    parser.add_argument("--api-json", type=Path, default=ROOT / "reports" / "api.json")
    parser.add_argument("--status", type=Path, default=ROOT / "trace" / "regression_status.md")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--force-defects", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    return build(parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
