"""M5 checks for collection shape, environment, boundary files, and traceability."""

from __future__ import annotations

import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTMAN = ROOT / "postman"
COLLECTIONS = {
    "Learning": POSTMAN / "collections" / "learning.postman_collection.json",
    "Quality": POSTMAN / "collections" / "quality.postman_collection.json",
    "Work Orders": POSTMAN / "collections" / "workorders.postman_collection.json",
}


def _walk(items: list[dict]) -> list[dict]:
    requests = []
    for item in items:
        if "item" in item:
            requests.extend(_walk(item["item"]))
        else:
            requests.append(item)
    return requests


def _load_collections() -> dict[str, dict]:
    loaded = {}
    for name, path in COLLECTIONS.items():
        loaded[name] = json.loads(path.read_text(encoding="utf-8"))
    return loaded


def test_collections_have_tests_and_base_url():
    loaded = _load_collections()
    assert set(loaded) == {"Learning", "Quality", "Work Orders"}
    for name, collection in loaded.items():
        assert collection["info"]["schema"].endswith("collection/v2.1.0/collection.json")
        assert "SIMULATED" in collection["info"]["description"]
        folders = [item["name"] for item in collection["item"]]
        assert "Setup" in folders
        assert "Workflow" in folders
        requests = _walk(collection["item"])
        assert requests, name
        for request in requests:
            assert "{{baseUrl}}" in request["request"]["url"]
            tests = [
                event
                for event in request["event"]
                if event["listen"] == "test" and event["script"]["exec"]
            ]
            assert tests, request["name"]


def test_environment_loads_local_base_url():
    environment = json.loads(
        (POSTMAN / "environments" / "local.postman_environment.json").read_text(encoding="utf-8")
    )
    values = {row["key"]: row["value"] for row in environment["values"] if row["enabled"]}
    assert values["baseUrl"] == "http://127.0.0.1:18765"
    assert values["forceDefects"] == "false"


def test_boundary_files_cover_the_required_values():
    with (POSTMAN / "data" / "pass_mark_boundaries.csv").open(encoding="utf-8", newline="") as handle:
        scores = {row["score"] for row in csv.DictReader(handle)}
    assert scores == {"79.99", "80.00", "80.01", "79.994", "79.995"}

    with (POSTMAN / "data" / "quality_boundaries.csv").open(encoding="utf-8", newline="") as handle:
        quality = list(csv.DictReader(handle))
    assert {row["expected_score"] for row in quality} == {"79.99", "80.00", "80.01"}
    assert {row["expected_classification"] for row in quality} == {"Below standard", "Meets standard"}

    with (POSTMAN / "data" / "work_hours_boundaries.csv").open(encoding="utf-8", newline="") as handle:
        hours = {row["hours"] for row in csv.DictReader(handle)}
    assert hours == {"0", "0.01", "24", "24.01"}


def test_traceability_lists_every_request_and_case():
    loaded = _load_collections()
    trace = (ROOT / "docs" / "api_traceability.md").read_text(encoding="utf-8")
    assert "Not run" not in trace
    for collection in loaded.values():
        for request in _walk(collection["item"]):
            assert request["name"] in trace
            script = "\n".join(
                line
                for event in request["event"]
                if event["listen"] == "test"
                for line in event["script"]["exec"]
            )
            for token in script.replace('"', " ").replace("'", " ").split():
                if token.startswith("TC-") or token.startswith("REQ-"):
                    assert token in trace


def test_newman_report_has_no_assertion_failures():
    report = json.loads((ROOT / "reports" / "api.json").read_text(encoding="utf-8"))
    assert report["simulated"] is True
    assert report["forceDefects"] is False
    assert len(report["collections"]) == 3
    failed = 0
    for entry in report["collections"]:
        failed += entry["run"]["run"]["stats"]["assertions"]["failed"]
    assert failed == 0

    root = ET.parse(ROOT / "reports" / "api.xml").getroot()
    suites = root.findall("testsuite") if root.tag == "testsuites" else [root]
    assert suites
    assert sum(int(suite.get("failures") or 0) for suite in suites) == 0
