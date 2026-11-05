"""Write the M5 Postman collections, environment, and CSV boundary files.

The JSON collections are the artifacts Newman runs. This builder keeps the
request names, scripts, and trace rows in one place.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTMAN = ROOT / "postman"
TRACE: list[tuple[str, str, str, str]] = []
CURRENT = {"collection": ""}

FORCE_SKIP = """
const forced = String(pm.environment.get("forceDefects") || "").toLowerCase() === "true";
if (forced) {
    pm.execution.skipRequest();
}
""".strip("\n")

WORKFLOW_SKIP = """
if (pm.info.iteration > 0) {
    pm.execution.skipRequest();
}
""".strip("\n")

SIMULATED = (
    "SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo."
)


def lines(script: str) -> list[str]:
    return script.strip("\n").split("\n")


def item(
    name: str,
    method: str,
    path: str,
    *,
    traces: list[tuple[str, str]],
    tests: str,
    raw_body: str | None = None,
    prerequest: str = "",
) -> dict:
    for requirement, case in traces:
        TRACE.append((requirement, case, name, CURRENT["collection"]))
    events = []
    if prerequest:
        events.append(
            {
                "listen": "prerequest",
                "script": {"type": "text/javascript", "exec": lines(prerequest)},
            }
        )
    events.append(
        {"listen": "test", "script": {"type": "text/javascript", "exec": lines(tests)}}
    )
    request: dict = {
        "method": method,
        "header": [{"key": "Accept", "value": "application/json"}],
        "url": "{{baseUrl}}" + path,
    }
    if raw_body is not None:
        request["header"].append({"key": "Content-Type", "value": "application/json"})
        request["body"] = {"mode": "raw", "raw": raw_body}
    return {"name": name, "request": request, "event": events}


def folder(name: str, items: list[dict], prerequest: str = "") -> dict:
    node: dict = {"name": name, "item": items}
    if prerequest:
        node["event"] = [
            {
                "listen": "prerequest",
                "script": {"type": "text/javascript", "exec": lines(prerequest)},
            }
        ]
    return node


def collection(name: str, description: str, items: list[dict]) -> dict:
    return {
        "info": {
            "name": name,
            "description": description,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "variable": [
            {"key": "baseUrl", "value": "http://127.0.0.1:18765"},
            {"key": "enrollmentId", "value": ""},
            {"key": "thresholdEnrollmentId", "value": ""},
            {"key": "earlyEnrollmentId", "value": ""},
            {"key": "certificateId", "value": ""},
            {"key": "boundaryEnrollmentId", "value": ""},
            {"key": "evalDisputeId", "value": ""},
            {"key": "boundaryEvaluationId", "value": ""},
            {"key": "newOrderId", "value": ""},
        ],
        "item": items,
    }


def health(traces_name: str) -> dict:
    return item(
        "Health",
        "GET",
        "/health",
        traces=[("Setup", traces_name)],
        tests="""
const body = pm.response.json();
pm.test("Health reports the simulated service", function () {
    pm.response.to.have.status(200);
    pm.expect(body.status).to.eql("ok");
    pm.expect(body.simulated).to.eql(true);
    pm.expect(body.service).to.eql("package-sim");
    pm.expect(pm.response.headers.get("X-Simulated")).to.eql("true");
});
""",
    )


def reset(label: str) -> dict:
    return item(
        "Reset seed",
        "POST",
        "/test/reset",
        traces=[("Setup", label)],
        tests="""
const body = pm.response.json();
pm.test("Reset reloads the seed", function () {
    pm.response.to.have.status(200);
    pm.expect(body.status).to.eql("reset");
    pm.expect(body.simulated).to.eql(true);
    pm.expect(pm.response.headers.get("X-Simulated")).to.eql("true");
});
""",
    )


def disable(defect_id: str, requirement: str) -> dict:
    return item(
        f"Disable {defect_id}",
        "POST",
        f"/api/defects/{defect_id}",
        traces=[(requirement, f"Disable {defect_id}")],
        raw_body='{"enabled": false}',
        prerequest=FORCE_SKIP,
        tests=f"""
const body = pm.response.json();
pm.test("Disable {defect_id} so the M1 rule is under test", function () {{
    pm.response.to.have.status(200);
    pm.expect(body.id).to.eql("{defect_id}");
    pm.expect(body.enabled).to.eql(false);
    pm.expect(body.requirement).to.eql("{requirement}");
}});
""",
    )


def learning_items() -> list[dict]:
    workflow = [
        item(
            "TC-INT-019 Read learners",
            "GET",
            "/api/learning/learners",
            traces=[("REQ-INT-009", "TC-INT-019")],
            tests="""
const rows = pm.response.json();
pm.test("TC-INT-019 REQ-INT-009 learners expose id and name", function () {
    pm.response.to.have.status(200);
    pm.expect(rows).to.be.an("array").that.has.lengthOf(5);
    pm.expect(rows[0]).to.include.keys("id", "name", "active");
});
""",
        ),
        item(
            "TC-INT-001 Enroll an available activity",
            "POST",
            "/api/learning/enrollments",
            traces=[("REQ-INT-001", "TC-INT-001")],
            raw_body='{"learner_id": "LN-01", "activity_id": "ACT-102"}',
            tests="""
const body = pm.response.json();
pm.test("TC-INT-001 REQ-INT-001 enrollment is created", function () {
    pm.response.to.have.status(200);
    pm.expect(body).to.include.keys("id", "learner_id", "activity_id", "state", "score", "attempts", "certificate_id");
    pm.expect(body.state).to.eql("Enrolled");
    pm.expect(body.learner_id).to.eql("LN-01");
    pm.expect(body.activity_id).to.eql("ACT-102");
    pm.expect(body.score).to.eql(null);
    pm.expect(body.attempts).to.eql(0);
    pm.expect(body.certificate_id).to.eql(null);
    pm.collectionVariables.set("enrollmentId", body.id);
});
""",
        ),
        item(
            "TC-INT-002 Reject a duplicate enrollment",
            "POST",
            "/api/learning/enrollments",
            traces=[("REQ-INT-001", "TC-INT-002")],
            raw_body='{"learner_id": "LN-01", "activity_id": "ACT-102"}',
            tests="""
pm.test("TC-INT-002 REQ-INT-001 duplicate enrollment is rejected", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("active enrollment already exists");
    pm.expect(pm.response.headers.get("X-Simulated")).to.eql("true");
});
""",
        ),
        item(
            "TC-INT-004 Start the enrollment",
            "POST",
            "/api/learning/enrollments/{{enrollmentId}}/start",
            traces=[("REQ-INT-002", "TC-INT-004")],
            tests="""
const body = pm.response.json();
pm.test("TC-INT-004 REQ-INT-002 content modules complete on start", function () {
    pm.response.to.have.status(200);
    pm.expect(body.id).to.eql(pm.collectionVariables.get("enrollmentId"));
    pm.expect(body.state).to.eql("In Progress");
    const status = {};
    body.modules.forEach((module) => { status[module.id] = module.status; });
    pm.expect(status["MOD-4"]).to.eql("Complete");
    pm.expect(status["MOD-5"]).to.eql("Not started");
});
""",
        ),
        item(
            "TC-INT-009 Pass at 80.01",
            "POST",
            "/api/learning/enrollments/{{enrollmentId}}/assessment",
            traces=[("REQ-INT-004", "TC-INT-009")],
            raw_body='{"score": 80.01}',
            tests="""
const body = pm.response.json();
pm.test("TC-INT-009 REQ-INT-004 score 80.01 passes", function () {
    pm.response.to.have.status(200);
    pm.expect(body.id).to.eql(pm.collectionVariables.get("enrollmentId"));
    pm.expect(body.state).to.eql("Passed");
    pm.expect(body.score).to.be.closeTo(80.01, 0.001);
    pm.expect(body.attempts).to.eql(1);
    pm.expect(body.certificate_id).to.eql(null);
});
""",
        ),
        item(
            "TC-INT-019 Read the passed enrollment",
            "GET",
            "/api/learning/enrollments",
            traces=[("REQ-INT-009", "TC-INT-019")],
            tests="""
pm.test("TC-INT-019 REQ-INT-009 stored enrollment keeps the pass", function () {
    pm.response.to.have.status(200);
    const row = pm.response.json().find((item) => item.id === pm.collectionVariables.get("enrollmentId"));
    pm.expect(row).to.be.an("object");
    pm.expect(row.state).to.eql("Passed");
    pm.expect(row.score).to.be.closeTo(80.01, 0.001);
    pm.expect(row.learner_id).to.eql("LN-01");
});
""",
        ),
        item(
            "TC-INT-014 Complete the passed enrollment",
            "POST",
            "/api/learning/enrollments/{{enrollmentId}}/complete",
            traces=[("REQ-INT-006", "TC-INT-014"), ("REQ-INT-007", "TC-INT-016")],
            tests="""
const body = pm.response.json();
pm.test("TC-INT-014 REQ-INT-006 completion is stored once", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("Completed");
    pm.expect(body.completion_date).to.be.a("string");
    pm.expect(body.certificate_id).to.be.a("string").and.not.empty;
    pm.collectionVariables.set("certificateId", body.certificate_id);
});
""",
        ),
        item(
            "TC-INT-016 Read the certificate dates",
            "GET",
            "/api/learning/certificates",
            traces=[("REQ-INT-007", "TC-INT-016")],
            tests="""
pm.test("TC-INT-016 REQ-INT-007 issued date matches completion", function () {
    pm.response.to.have.status(200);
    const certificate = pm.response.json().find((row) => row.id === pm.collectionVariables.get("certificateId"));
    pm.expect(certificate).to.be.an("object");
    pm.expect(certificate.issued_on).to.eql(certificate.completion_date);
    pm.expect(certificate.learner_id).to.eql("LN-01");
    pm.expect(certificate.enrollment_id).to.eql(pm.collectionVariables.get("enrollmentId"));
    pm.expect(certificate.score).to.be.closeTo(80.01, 0.001);
});
""",
        ),
        item(
            "TC-INT-014 Reject a second completion",
            "POST",
            "/api/learning/enrollments/{{enrollmentId}}/complete",
            traces=[("REQ-INT-006", "TC-INT-014")],
            tests="""
pm.test("TC-INT-014 REQ-INT-006 a completed enrollment stays completed", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("Completed -> Completed");
});
""",
        ),
        item(
            "TC-INT-010 Fail at 79.99",
            "POST",
            "/api/learning/enrollments/ENR-01/assessment",
            traces=[("REQ-INT-004", "TC-INT-010"), ("REQ-INT-005", "TC-INT-010")],
            raw_body='{"score": 79.99}',
            tests="""
const body = pm.response.json();
pm.test("TC-INT-010 REQ-INT-004 REQ-INT-005 79.99 fails without a certificate", function () {
    pm.response.to.have.status(200);
    pm.expect(body.id).to.eql("ENR-01");
    pm.expect(body.state).to.eql("Failed");
    pm.expect(body.score).to.be.closeTo(79.99, 0.001);
    pm.expect(body.certificate_id).to.eql(null);
});
""",
        ),
        item(
            "TC-INT-008 Enroll for the 80.00 threshold",
            "POST",
            "/api/learning/enrollments",
            traces=[("REQ-INT-004", "TC-INT-008")],
            raw_body='{"learner_id": "LN-03", "activity_id": "ACT-102"}',
            tests="""
const body = pm.response.json();
pm.test("TC-INT-008 REQ-INT-004 threshold enrollment is created", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("Enrolled");
    pm.collectionVariables.set("thresholdEnrollmentId", body.id);
});
""",
        ),
        item(
            "TC-INT-008 Start the threshold enrollment",
            "POST",
            "/api/learning/enrollments/{{thresholdEnrollmentId}}/start",
            traces=[("REQ-INT-004", "TC-INT-008")],
            tests="""
pm.test("TC-INT-008 REQ-INT-004 threshold enrollment is in progress", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json().state).to.eql("In Progress");
    pm.expect(pm.response.json().id).to.eql(pm.collectionVariables.get("thresholdEnrollmentId"));
});
""",
        ),
        item(
            "TC-INT-008 Pass at 80.00",
            "POST",
            "/api/learning/enrollments/{{thresholdEnrollmentId}}/assessment",
            traces=[("REQ-INT-004", "TC-INT-008")],
            raw_body='{"score": 80.00}',
            tests="""
const body = pm.response.json();
pm.test("TC-INT-008 REQ-INT-004 score 80.00 passes", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("Passed");
    pm.expect(body.score).to.be.closeTo(80, 0.001);
    pm.expect(body.certificate_id).to.eql(null);
});
""",
        ),
        item(
            "TC-INT-003 Reject an unpublished activity",
            "POST",
            "/api/learning/enrollments",
            traces=[("REQ-INT-001", "TC-INT-003")],
            raw_body='{"learner_id": "LN-02", "activity_id": "ACT-103"}',
            tests="""
pm.test("TC-INT-003 REQ-INT-001 a draft activity cannot be enrolled", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("not available");
});
""",
        ),
        item(
            "TC-INT-005 Enroll before an early assessment",
            "POST",
            "/api/learning/enrollments",
            traces=[("REQ-INT-002", "TC-INT-005")],
            raw_body='{"learner_id": "LN-02", "activity_id": "ACT-102"}',
            tests="""
const body = pm.response.json();
pm.test("TC-INT-005 REQ-INT-002 early enrollment is only enrolled", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("Enrolled");
    pm.collectionVariables.set("earlyEnrollmentId", body.id);
});
""",
        ),
        item(
            "TC-INT-005 Reject an assessment before start",
            "POST",
            "/api/learning/enrollments/{{earlyEnrollmentId}}/assessment",
            traces=[("REQ-INT-002", "TC-INT-005")],
            raw_body='{"score": 50}',
            tests="""
pm.test("TC-INT-005 REQ-INT-002 assessment before start is rejected", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("Illegal transition");
});
""",
        ),
        item(
            "TC-INT-015 Reject completion of a failed enrollment",
            "POST",
            "/api/learning/enrollments/ENR-03/complete",
            traces=[("REQ-INT-006", "TC-INT-015")],
            tests="""
pm.test("TC-INT-015 REQ-INT-006 a failed enrollment cannot complete", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("Failed -> Completed");
});
""",
        ),
        item(
            "TC-INT-020 Reject an unknown enrollment",
            "POST",
            "/api/learning/enrollments/ENR-99/start",
            traces=[("REQ-INT-009", "TC-INT-020")],
            tests="""
pm.test("TC-INT-020 REQ-INT-009 an unknown enrollment is not found", function () {
    pm.response.to.have.status(404);
    pm.expect(pm.response.json().detail).to.include("ENR-99");
});
""",
        ),
    ]
    boundary_skip = """
const score = pm.iterationData.get("score");
if (score === undefined || score === null || score === "") {
    pm.execution.skipRequest();
}
""".strip("\n")
    boundary = [
        item(
            "TC-INT-007 Enroll a boundary learner",
            "POST",
            "/api/learning/enrollments",
            traces=[("REQ-INT-003", "TC-INT-007")],
            raw_body='{"learner_id": "LN-05", "activity_id": "ACT-102"}',
            tests="""
const body = pm.response.json();
pm.test("Boundary enrollment is created", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("Enrolled");
    pm.collectionVariables.set("boundaryEnrollmentId", body.id);
});
""",
        ),
        item(
            "TC-INT-007 Start the boundary enrollment",
            "POST",
            "/api/learning/enrollments/{{boundaryEnrollmentId}}/start",
            traces=[("REQ-INT-003", "TC-INT-007")],
            tests="""
pm.test("Boundary enrollment is in progress", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json().state).to.eql("In Progress");
});
""",
        ),
        item(
            "TC-INT-007 Assess the boundary score",
            "POST",
            "/api/learning/enrollments/{{boundaryEnrollmentId}}/assessment",
            traces=[
                ("REQ-INT-003", "TC-INT-007"),
                ("REQ-INT-004", "TC-INT-008"),
                ("REQ-INT-004", "TC-INT-009"),
                ("REQ-INT-004", "TC-INT-010"),
            ],
            raw_body='{"score": {{score}}}',
            tests="""
const body = pm.response.json();
const testCase = pm.iterationData.get("test_case");
const requirement = pm.iterationData.get("requirement");
pm.test(testCase + " " + requirement + " boundary score", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql(pm.iterationData.get("expected_state"));
    pm.expect(body.score).to.be.closeTo(Number(pm.iterationData.get("expected_score")), 0.001);
    pm.expect(body.attempts).to.eql(1);
    pm.expect(body.certificate_id).to.eql(null);
});
""",
        ),
    ]
    return [
        folder("Setup", [health("Learning health"), reset("Learning reset"), disable("pass_mark", "REQ-INT-004"), disable("certificate_date", "REQ-INT-007")]),
        folder("Workflow", workflow, WORKFLOW_SKIP),
        folder("Pass mark boundaries", boundary, boundary_skip),
    ]


def quality_items() -> list[dict]:
    workflow = [
        item(
            "TC-VER-001 Read interactions",
            "GET",
            "/api/quality/interactions",
            traces=[("REQ-VER-001", "TC-VER-001")],
            tests="""
const rows = pm.response.json();
pm.test("TC-VER-001 REQ-VER-001 interactions expose the recorded fields", function () {
    pm.response.to.have.status(200);
    pm.expect(rows.length).to.be.at.least(5);
    pm.expect(rows[0]).to.include.keys("id", "channel", "agent_id", "agent_name", "summary");
});
""",
        ),
        item(
            "TC-VER-001 Create an evaluation",
            "POST",
            "/api/quality/evaluations",
            traces=[("REQ-VER-001", "TC-VER-001")],
            raw_body='{"interaction_id": "INT-01"}',
            tests="""
const body = pm.response.json();
pm.test("TC-VER-001 REQ-VER-001 a new evaluation is pending", function () {
    pm.response.to.have.status(200);
    pm.expect(body).to.include.keys("id", "interaction_id", "agent_id", "state", "score", "classification");
    pm.expect(body.state).to.eql("Pending");
    pm.expect(body.interaction_id).to.eql("INT-01");
    pm.expect(body.score).to.eql(null);
    pm.expect(body.classification).to.eql(null);
});
""",
        ),
        item(
            "TC-VER-002 Reject an unknown interaction",
            "POST",
            "/api/quality/evaluations",
            traces=[("REQ-VER-001", "TC-VER-002")],
            raw_body='{"interaction_id": "INT-99"}',
            tests="""
pm.test("TC-VER-002 REQ-VER-001 an unknown interaction is not found", function () {
    pm.response.to.have.status(404);
    pm.expect(pm.response.json().detail).to.include("INT-99");
});
""",
        ),
        item(
            "TC-VER-003 Create an evaluation for a partial submit",
            "POST",
            "/api/quality/evaluations",
            traces=[("REQ-VER-002", "TC-VER-003")],
            raw_body='{"interaction_id": "INT-02"}',
            tests="""
pm.test("TC-VER-003 REQ-VER-002 partial evaluation is pending", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json().state).to.eql("Pending");
    pm.collectionVariables.set("evalPartialId", pm.response.json().id);
});
""",
        ),
        item(
            "TC-VER-003 Reject a submit that omits a section",
            "POST",
            "/api/quality/evaluations/{{evalPartialId}}/submit",
            traces=[("REQ-VER-002", "TC-VER-003")],
            raw_body='{"sections": [{"id": "A", "earned": 1, "possible": 2}]}',
            tests="""
pm.test("TC-VER-003 REQ-VER-002 sections A, B, and C are required", function () {
    pm.response.to.have.status(422);
    pm.expect(pm.response.json().detail).to.include("Sections A, B, and C");
});
""",
        ),
        item(
            "TC-VER-004 Create an all-yes evaluation",
            "POST",
            "/api/quality/evaluations",
            traces=[("REQ-VER-003", "TC-VER-004")],
            raw_body='{"interaction_id": "INT-03"}',
            tests="""
pm.test("TC-VER-004 REQ-VER-003 all-yes evaluation is pending", function () {
    pm.response.to.have.status(200);
    pm.collectionVariables.set("evalAllYesId", pm.response.json().id);
});
""",
        ),
        item(
            "TC-VER-004 Score all yes as 100",
            "POST",
            "/api/quality/evaluations/{{evalAllYesId}}/submit",
            traces=[("REQ-VER-003", "TC-VER-004")],
            raw_body='{"sections": [{"id": "A", "earned": 2, "possible": 2}, {"id": "B", "earned": 1, "possible": 1}, {"id": "C", "earned": 1, "possible": 1}]}',
            tests="""
const body = pm.response.json();
pm.test("TC-VER-004 REQ-VER-003 all yes scores 100 and meets standard", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("Under Review");
    pm.expect(body.score).to.be.closeTo(100, 0.001);
    pm.expect(body.classification).to.eql("Meets standard");
});
""",
        ),
        item(
            "TC-VER-004 Create an all-no evaluation",
            "POST",
            "/api/quality/evaluations",
            traces=[("REQ-VER-003", "TC-VER-004")],
            raw_body='{"interaction_id": "INT-04"}',
            tests="""
pm.test("TC-VER-004 REQ-VER-003 all-no evaluation is pending", function () {
    pm.response.to.have.status(200);
    pm.collectionVariables.set("evalAllNoId", pm.response.json().id);
});
""",
        ),
        item(
            "TC-VER-004 Score all no as 0",
            "POST",
            "/api/quality/evaluations/{{evalAllNoId}}/submit",
            traces=[("REQ-VER-003", "TC-VER-004")],
            raw_body='{"sections": [{"id": "A", "earned": 0, "possible": 2}, {"id": "B", "earned": 0, "possible": 1}, {"id": "C", "earned": 0, "possible": 1}]}',
            tests="""
const body = pm.response.json();
pm.test("TC-VER-004 REQ-VER-003 all no scores 0 and is below standard", function () {
    pm.response.to.have.status(200);
    pm.expect(body.score).to.be.closeTo(0, 0.001);
    pm.expect(body.classification).to.eql("Below standard");
});
""",
        ),
        item(
            "TC-VER-005 Score weighted sections as 70",
            "POST",
            "/api/quality/evaluations/EV-01/submit",
            traces=[("REQ-VER-003", "TC-VER-005"), ("REQ-VER-002", "TC-VER-005")],
            raw_body='{"sections": [{"id": "A", "earned": 1, "possible": 2}, {"id": "B", "earned": 1, "possible": 1}, {"id": "C", "earned": 1, "possible": 1}]}',
            tests="""
const body = pm.response.json();
pm.test("TC-VER-005 REQ-VER-003 weighted score is 70 and below standard", function () {
    pm.response.to.have.status(200);
    pm.expect(body.id).to.eql("EV-01");
    pm.expect(body.state).to.eql("Under Review");
    pm.expect(body.score).to.be.closeTo(70, 0.001);
    pm.expect(body.classification).to.eql("Below standard");
    pm.expect(body.sections).to.have.lengthOf(3);
});
""",
        ),
        item(
            "TC-VER-009 Acknowledge a scored evaluation",
            "POST",
            "/api/quality/evaluations/EV-02/acknowledge",
            traces=[("REQ-VER-006", "TC-VER-009")],
            tests="""
const body = pm.response.json();
pm.test("TC-VER-009 REQ-VER-006 acknowledgement keeps the score", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("Acknowledged");
    pm.expect(body.score).to.be.closeTo(70, 0.001);
    pm.expect(body.acknowledged_at).to.be.a("string").and.not.empty;
});
""",
        ),
        item(
            "TC-VER-010 Create a pending evaluation",
            "POST",
            "/api/quality/evaluations",
            traces=[("REQ-VER-006", "TC-VER-010")],
            raw_body='{"interaction_id": "INT-05"}',
            tests="""
pm.test("TC-VER-010 REQ-VER-006 pending evaluation is stored", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json().state).to.eql("Pending");
    pm.collectionVariables.set("evalPendingId", pm.response.json().id);
});
""",
        ),
        item(
            "TC-VER-010 Reject acknowledgement while pending",
            "POST",
            "/api/quality/evaluations/{{evalPendingId}}/acknowledge",
            traces=[("REQ-VER-006", "TC-VER-010")],
            tests="""
pm.test("TC-VER-010 REQ-VER-006 a pending evaluation cannot be acknowledged", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("Pending -> Acknowledged");
});
""",
        ),
        item(
            "TC-VER-011 Create an evaluation to dispute",
            "POST",
            "/api/quality/evaluations",
            traces=[("REQ-VER-007", "TC-VER-011")],
            raw_body='{"interaction_id": "INT-01"}',
            tests="""
pm.test("TC-VER-011 REQ-VER-007 dispute evaluation is pending", function () {
    pm.response.to.have.status(200);
    pm.collectionVariables.set("evalDisputeId", pm.response.json().id);
});
""",
        ),
        item(
            "TC-VER-011 Submit the dispute evaluation",
            "POST",
            "/api/quality/evaluations/{{evalDisputeId}}/submit",
            traces=[("REQ-VER-007", "TC-VER-011")],
            raw_body='{"sections": [{"id": "A", "earned": 2, "possible": 2}, {"id": "B", "earned": 1, "possible": 1}, {"id": "C", "earned": 1, "possible": 1}]}',
            tests="""
pm.test("TC-VER-011 REQ-VER-007 dispute evaluation is under review", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json().state).to.eql("Under Review");
    pm.expect(pm.response.json().score).to.be.closeTo(100, 0.001);
});
""",
        ),
        item(
            "TC-VER-011 Dispute with a comment",
            "POST",
            "/api/quality/evaluations/{{evalDisputeId}}/dispute",
            traces=[("REQ-VER-007", "TC-VER-011")],
            raw_body='{"comment": "The greeting question does not match the call."}',
            tests="""
const body = pm.response.json();
pm.test("TC-VER-011 REQ-VER-007 dispute keeps the score and stores the comment", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("Disputed");
    pm.expect(body.score).to.be.closeTo(100, 0.001);
    pm.expect(body.dispute_comment).to.include("does not match the call");
});
""",
        ),
        item(
            "TC-VER-012 Create an evaluation for an empty dispute",
            "POST",
            "/api/quality/evaluations",
            traces=[("REQ-VER-007", "TC-VER-012")],
            raw_body='{"interaction_id": "INT-02"}',
            tests="""
pm.test("TC-VER-012 REQ-VER-007 empty-dispute evaluation is pending", function () {
    pm.response.to.have.status(200);
    pm.collectionVariables.set("evalEmptyDisputeId", pm.response.json().id);
});
""",
        ),
        item(
            "TC-VER-012 Submit before the empty dispute",
            "POST",
            "/api/quality/evaluations/{{evalEmptyDisputeId}}/submit",
            traces=[("REQ-VER-007", "TC-VER-012")],
            raw_body='{"sections": [{"id": "A", "earned": 2, "possible": 2}, {"id": "B", "earned": 1, "possible": 1}, {"id": "C", "earned": 1, "possible": 1}]}',
            tests="""
pm.test("TC-VER-012 REQ-VER-007 empty-dispute evaluation is under review", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json().state).to.eql("Under Review");
});
""",
        ),
        item(
            "TC-VER-012 Reject a dispute without a comment",
            "POST",
            "/api/quality/evaluations/{{evalEmptyDisputeId}}/dispute",
            traces=[("REQ-VER-007", "TC-VER-012")],
            raw_body='{"comment": ""}',
            tests="""
pm.test("TC-VER-012 REQ-VER-007 a dispute requires a comment", function () {
    pm.response.to.have.status(422);
    pm.expect(pm.response.json().detail).to.include("dispute requires a comment");
});
""",
        ),
        item(
            "TC-VER-013 Resolve the dispute",
            "POST",
            "/api/quality/evaluations/{{evalDisputeId}}/resolve",
            traces=[("REQ-VER-007", "TC-VER-013")],
            tests="""
const body = pm.response.json();
pm.test("TC-VER-013 REQ-VER-007 resolve returns the evaluation to under review", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("Under Review");
    pm.expect(body.score).to.be.closeTo(100, 0.001);
});
""",
        ),
        item(
            "TC-VER-014 Coach the resolved evaluation",
            "POST",
            "/api/quality/evaluations/{{evalDisputeId}}/coach",
            traces=[("REQ-VER-005", "TC-VER-014"), ("REQ-VER-008", "TC-VER-015")],
            raw_body='{"note": "Review the greeting."}',
            tests="""
const body = pm.response.json();
pm.test("TC-VER-015 REQ-VER-008 coaching keeps the score", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("Coached");
    pm.expect(body.score).to.be.closeTo(100, 0.001);
    pm.expect(body.coaching_note).to.eql("Review the greeting.");
});
""",
        ),
        item(
            "TC-VER-014 Complete the coached evaluation",
            "POST",
            "/api/quality/evaluations/{{evalDisputeId}}/complete",
            traces=[("REQ-VER-005", "TC-VER-014"), ("REQ-VER-008", "TC-VER-015")],
            tests="""
const body = pm.response.json();
pm.test("TC-VER-014 REQ-VER-005 a coached evaluation can complete", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("Completed");
    pm.expect(body.score).to.be.closeTo(100, 0.001);
    pm.expect(body.coaching_note).to.eql("Review the greeting.");
});
""",
        ),
    ]
    boundary_skip = """
const earned = pm.iterationData.get("earned_a");
if (earned === undefined || earned === null || earned === "") {
    pm.execution.skipRequest();
}
""".strip("\n")
    boundary = [
        item(
            "TC-VER-007 Create a threshold evaluation",
            "POST",
            "/api/quality/evaluations",
            traces=[("REQ-VER-004", "TC-VER-007")],
            raw_body='{"interaction_id": "INT-05"}',
            tests="""
pm.test("Threshold evaluation is pending", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json().state).to.eql("Pending");
    pm.collectionVariables.set("boundaryEvaluationId", pm.response.json().id);
});
""",
        ),
        item(
            "TC-VER-007 Submit the threshold sections",
            "POST",
            "/api/quality/evaluations/{{boundaryEvaluationId}}/submit",
            traces=[("REQ-VER-004", "TC-VER-007"), ("REQ-VER-004", "TC-VER-008")],
            raw_body='{"sections": [{"id": "A", "earned": {{earned_a}}, "possible": 2}, {"id": "B", "earned": {{earned_b}}, "possible": 1}, {"id": "C", "earned": {{earned_c}}, "possible": 1}]}',
            tests="""
const body = pm.response.json();
const testCase = pm.iterationData.get("test_case");
const requirement = pm.iterationData.get("requirement");
pm.test(testCase + " " + requirement + " quality threshold", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("Under Review");
    pm.expect(body.score).to.be.closeTo(Number(pm.iterationData.get("expected_score")), 0.001);
    pm.expect(body.classification).to.eql(pm.iterationData.get("expected_classification"));
});
""",
        ),
    ]
    return [
        folder(
            "Setup",
            [health("Quality health"), reset("Quality reset"), disable("quality_score", "REQ-VER-003")],
        ),
        folder("Workflow", workflow, WORKFLOW_SKIP),
        folder("Quality score boundaries", boundary, boundary_skip),
    ]


def work_items() -> list[dict]:
    workflow = [
        item(
            "TC-TRI-001 Reject a request missing a title",
            "POST",
            "/api/work/orders",
            traces=[("REQ-TRI-001", "TC-TRI-001")],
            raw_body='{"title": " ", "requester_id": "RQ-01", "building": "HQ", "request_class": "Electrical", "description": "Lamp is out."}',
            tests="""
pm.test("TC-TRI-001 REQ-TRI-001 a blank title is rejected", function () {
    pm.response.to.have.status(422);
    pm.expect(pm.response.json().detail).to.include("Required fields missing");
});
""",
        ),
        item(
            "TC-TRI-002 Create a service request",
            "POST",
            "/api/work/orders",
            traces=[("REQ-TRI-001", "TC-TRI-002")],
            raw_body='{"title": "Replace simulated lamp", "requester_id": "RQ-01", "building": "HQ", "request_class": "Electrical", "description": "Lamp is out."}',
            tests="""
const body = pm.response.json();
pm.test("TC-TRI-002 REQ-TRI-001 a complete request is saved as Draft", function () {
    pm.response.to.have.status(200);
    pm.expect(body).to.include.keys("id", "title", "requester_id", "building", "request_class", "description", "state", "technician_id");
    pm.expect(body.state).to.eql("Draft");
    pm.expect(body.technician_id).to.eql(null);
    pm.expect(body.title).to.eql("Replace simulated lamp");
    pm.collectionVariables.set("newOrderId", body.id);
});
""",
        ),
        item(
            "TC-TRI-002 Submit the request",
            "POST",
            "/api/work/orders/{{newOrderId}}/transition",
            traces=[("REQ-TRI-001", "TC-TRI-002")],
            raw_body='{"to": "WAPPR", "actor_id": "AP-01"}',
            tests="""
const body = pm.response.json();
pm.test("TC-TRI-002 REQ-TRI-001 the request moves to WAPPR", function () {
    pm.response.to.have.status(200);
    pm.expect(body.id).to.eql(pm.collectionVariables.get("newOrderId"));
    pm.expect(body.state).to.eql("WAPPR");
});
""",
        ),
        item(
            "TC-TRI-003 Reject self-approval",
            "POST",
            "/api/work/orders/WO-02/transition",
            traces=[("REQ-TRI-002", "TC-TRI-003")],
            raw_body='{"to": "APPR", "actor_id": "RQ-02"}',
            tests="""
pm.test("TC-TRI-003 REQ-TRI-002 the requester cannot approve their own request", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("cannot approve their own request");
});
""",
        ),
        item(
            "TC-TRI-004 Approve as a different person",
            "POST",
            "/api/work/orders/WO-02/transition",
            traces=[("REQ-TRI-002", "TC-TRI-004")],
            raw_body='{"to": "APPR", "actor_id": "AP-01"}',
            tests="""
const body = pm.response.json();
pm.test("TC-TRI-004 REQ-TRI-002 a different person can approve", function () {
    pm.response.to.have.status(200);
    pm.expect(body.id).to.eql("WO-02");
    pm.expect(body.state).to.eql("APPR");
    pm.expect(body.approved_by).to.eql("AP-01");
});
""",
        ),
        item(
            "TC-TRI-005 Reject a repeated approval",
            "POST",
            "/api/work/orders/WO-02/transition",
            traces=[("REQ-TRI-003", "TC-TRI-005")],
            raw_body='{"to": "APPR", "actor_id": "AP-01"}',
            tests="""
pm.test("TC-TRI-005 REQ-TRI-003 approving again does not create another order", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("APPR -> APPR");
});
""",
        ),
        item(
            "TC-TRI-006 Read orders after approval",
            "GET",
            "/api/work/orders",
            traces=[("REQ-TRI-003", "TC-TRI-005"), ("REQ-TRI-003", "TC-TRI-006")],
            tests="""
pm.test("TC-TRI-005 REQ-TRI-003 TC-TRI-006 one approved order and the draft stays unassigned", function () {
    pm.response.to.have.status(200);
    const rows = pm.response.json();
    const approved = rows.filter((row) => row.id === "WO-02");
    pm.expect(approved).to.have.lengthOf(1);
    pm.expect(approved[0].state).to.eql("APPR");
    const draft = rows.find((row) => row.id === "WO-01");
    pm.expect(draft.state).to.eql("Draft");
    pm.expect(draft.technician_id).to.eql(null);
    const created = rows.find((row) => row.id === pm.collectionVariables.get("newOrderId"));
    pm.expect(created.state).to.eql("WAPPR");
});
""",
        ),
        item(
            "TC-TRI-010 Reject start without a technician",
            "POST",
            "/api/work/orders/WO-02/transition",
            traces=[("REQ-TRI-005", "TC-TRI-010")],
            raw_body='{"to": "INPRG", "actor_id": "AP-01"}',
            tests="""
pm.test("TC-TRI-010 REQ-TRI-005 start without a technician is rejected", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("without an assigned technician");
});
""",
        ),
        item(
            "TC-TRI-008 Reject an inactive technician",
            "POST",
            "/api/work/orders/WO-03/assign",
            traces=[("REQ-TRI-004", "TC-TRI-008")],
            raw_body='{"technician_id": "TEC-02"}',
            tests="""
pm.test("TC-TRI-008 REQ-TRI-004 an inactive technician is rejected", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("inactive technician");
});
""",
        ),
        item(
            "TC-TRI-008 Read WO-03 after the inactive assignment",
            "GET",
            "/api/work/orders",
            traces=[("REQ-TRI-004", "TC-TRI-008")],
            tests="""
pm.test("TC-TRI-008 REQ-TRI-004 WO-03 stays unassigned", function () {
    pm.response.to.have.status(200);
    const order = pm.response.json().find((row) => row.id === "WO-03");
    pm.expect(order.state).to.eql("APPR");
    pm.expect(order.technician_id).to.eql(null);
});
""",
        ),
        item(
            "TC-TRI-007 Assign an active technician",
            "POST",
            "/api/work/orders/WO-03/assign",
            traces=[("REQ-TRI-004", "TC-TRI-007")],
            raw_body='{"technician_id": "TEC-01"}',
            tests="""
const body = pm.response.json();
pm.test("TC-TRI-007 REQ-TRI-004 an active technician is assigned without starting", function () {
    pm.response.to.have.status(200);
    pm.expect(body.id).to.eql("WO-03");
    pm.expect(body.state).to.eql("APPR");
    pm.expect(body.technician_id).to.eql("TEC-01");
});
""",
        ),
        item(
            "TC-TRI-009 Start assigned work",
            "POST",
            "/api/work/orders/WO-03/transition",
            traces=[("REQ-TRI-005", "TC-TRI-009")],
            raw_body='{"to": "INPRG", "actor_id": "AP-01"}',
            tests="""
const body = pm.response.json();
pm.test("TC-TRI-009 REQ-TRI-005 assigned work moves to INPRG", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("INPRG");
    pm.expect(body.technician_id).to.eql("TEC-01");
});
""",
        ),
        item(
            "TC-TRI-017 Reject completion from WMATL",
            "POST",
            "/api/work/orders/WO-06/transition",
            traces=[("REQ-TRI-008", "TC-TRI-017")],
            raw_body='{"to": "COMP", "actor_id": "AP-01"}',
            tests="""
pm.test("TC-TRI-017 REQ-TRI-008 WMATL cannot complete", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("WMATL -> COMP");
});
""",
        ),
        item(
            "TC-TRI-014 Reject a zero material quantity",
            "POST",
            "/api/work/orders/WO-06/materials",
            traces=[("REQ-TRI-007", "TC-TRI-014")],
            raw_body='{"item_id": "FILTER", "quantity": 0}',
            tests="""
pm.test("TC-TRI-014 REQ-TRI-007 a zero quantity is rejected", function () {
    pm.response.to.have.status(422);
    pm.expect(pm.response.json().detail).to.include("Quantity must be greater than 0");
});
""",
        ),
        item(
            "TC-TRI-013 Record a material quantity",
            "POST",
            "/api/work/orders/WO-06/materials",
            traces=[("REQ-TRI-007", "TC-TRI-013")],
            raw_body='{"item_id": "FILTER", "quantity": 1}',
            tests="""
const body = pm.response.json();
pm.test("TC-TRI-013 REQ-TRI-007 material is stored and the state stays WMATL", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("WMATL");
    pm.expect(body.material_entries).to.have.lengthOf(1);
    pm.expect(body.material_entries[0].item_id).to.eql("FILTER");
    pm.expect(body.material_entries[0].quantity).to.be.closeTo(1, 0.001);
});
""",
        ),
        item(
            "TC-TRI-015 Resume after waiting for material",
            "POST",
            "/api/work/orders/WO-06/transition",
            traces=[("REQ-TRI-007", "TC-TRI-015")],
            raw_body='{"to": "INPRG", "actor_id": "AP-01"}',
            tests="""
const body = pm.response.json();
pm.test("TC-TRI-015 REQ-TRI-007 resume keeps the material line", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("INPRG");
    pm.expect(body.material_entries).to.have.lengthOf(1);
    pm.expect(body.material_entries[0].item_id).to.eql("FILTER");
});
""",
        ),
        item(
            "TC-TRI-020 Reject closure from INPRG",
            "POST",
            "/api/work/orders/WO-05/transition",
            traces=[("REQ-TRI-009", "TC-TRI-020")],
            raw_body='{"to": "CLOSE", "actor_id": "AP-01"}',
            tests="""
pm.test("TC-TRI-020 REQ-TRI-009 INPRG cannot close", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("INPRG -> CLOSE");
});
""",
        ),
        item(
            "TC-TRI-017 Reject completion from APPR",
            "POST",
            "/api/work/orders/WO-10/transition",
            traces=[("REQ-TRI-008", "TC-TRI-017")],
            raw_body='{"to": "COMP", "actor_id": "AP-01"}',
            tests="""
pm.test("TC-TRI-017 REQ-TRI-008 APPR cannot complete", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("APPR -> COMP");
});
""",
        ),
        item(
            "TC-TRI-016 Complete in-progress work",
            "POST",
            "/api/work/orders/WO-05/transition",
            traces=[("REQ-TRI-008", "TC-TRI-016")],
            raw_body='{"to": "COMP", "actor_id": "AP-01"}',
            tests="""
const body = pm.response.json();
pm.test("TC-TRI-016 REQ-TRI-008 INPRG can complete", function () {
    pm.response.to.have.status(200);
    pm.expect(body.id).to.eql("WO-05");
    pm.expect(body.state).to.eql("COMP");
    pm.expect(body.completed_at).to.be.a("string").and.not.empty;
});
""",
        ),
        item(
            "TC-TRI-019 Close completed work",
            "POST",
            "/api/work/orders/WO-05/transition",
            traces=[("REQ-TRI-009", "TC-TRI-019")],
            raw_body='{"to": "CLOSE", "actor_id": "AP-01"}',
            tests="""
const body = pm.response.json();
pm.test("TC-TRI-019 REQ-TRI-009 COMP can close", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("CLOSE");
    pm.expect(body.closed_at).to.be.a("string").and.not.empty;
    pm.expect(body.completed_at).to.be.a("string").and.not.empty;
});
""",
        ),
        item(
            "TC-TRI-023 Reject rework without a reason",
            "POST",
            "/api/work/orders/WO-07/transition",
            traces=[("REQ-TRI-010", "TC-TRI-023")],
            raw_body='{"to": "INPRG", "actor_id": "AP-01", "reason": ""}',
            tests="""
pm.test("TC-TRI-023 REQ-TRI-010 rework requires a reason", function () {
    pm.response.to.have.status(422);
    pm.expect(pm.response.json().detail).to.include("Rework requires a reason");
});
""",
        ),
        item(
            "TC-TRI-022 Rework completed work",
            "POST",
            "/api/work/orders/WO-07/transition",
            traces=[("REQ-TRI-010", "TC-TRI-022")],
            raw_body='{"to": "INPRG", "actor_id": "AP-01", "reason": "Rail still moves"}',
            tests="""
const body = pm.response.json();
pm.test("TC-TRI-022 REQ-TRI-010 rework returns to INPRG and keeps actuals", function () {
    pm.response.to.have.status(200);
    pm.expect(body.state).to.eql("INPRG");
    pm.expect(body.rejection_reason).to.eql("Rail still moves");
    pm.expect(body.completed_at).to.eql(null);
    pm.expect(body.time_entries).to.have.lengthOf(1);
    pm.expect(body.time_entries[0].hours).to.be.closeTo(0.5, 0.001);
});
""",
        ),
        item(
            "TC-TRI-012 Reject time on a closed order",
            "POST",
            "/api/work/orders/WO-08/time",
            traces=[("REQ-TRI-006", "TC-TRI-012")],
            raw_body='{"technician_id": "TEC-01", "hours": 1}',
            tests="""
pm.test("TC-TRI-012 REQ-TRI-006 time on a closed order is rejected", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("Illegal actuals while CLOSE");
});
""",
        ),
        item(
            "TC-TRI-021 Reject reopen of a closed order",
            "POST",
            "/api/work/orders/WO-08/transition",
            traces=[("REQ-TRI-009", "TC-TRI-021")],
            raw_body='{"to": "INPRG", "actor_id": "AP-01"}',
            tests="""
pm.test("TC-TRI-021 REQ-TRI-009 a closed order stays closed", function () {
    pm.response.to.have.status(409);
    pm.expect(pm.response.json().detail).to.include("CLOSE -> INPRG");
});
""",
        ),
    ]
    boundary_skip = """
const hours = pm.iterationData.get("hours");
if (hours === undefined || hours === null || hours === "") {
    pm.execution.skipRequest();
}
""".strip("\n")
    boundary = [
        item(
            "TC-TRI-011 Record boundary hours",
            "POST",
            "/api/work/orders/WO-04/time",
            traces=[("REQ-TRI-006", "TC-TRI-011"), ("REQ-TRI-006", "TC-TRI-012")],
            raw_body='{"technician_id": "TEC-01", "hours": {{hours}}}',
            tests="""
const expected = Number(pm.iterationData.get("expected_status"));
const hours = Number(pm.iterationData.get("hours"));
const testCase = pm.iterationData.get("test_case");
const requirement = pm.iterationData.get("requirement");
pm.test(testCase + " " + requirement + " work hours boundary", function () {
    pm.response.to.have.status(expected);
    if (expected === 200) {
        const body = pm.response.json();
        pm.expect(body.id).to.eql("WO-04");
        pm.expect(body.state).to.eql("APPR");
        const entry = body.time_entries[body.time_entries.length - 1];
        pm.expect(entry.technician_id).to.eql("TEC-01");
        pm.expect(entry.hours).to.be.closeTo(hours, 0.001);
    }
    if (expected === 422 && hours > 0) {
        pm.expect(pm.response.json().detail).to.include("Hours must be");
    }
});
""",
        )
    ]
    return [
        folder(
            "Setup",
            [
                health("Work order health"),
                reset("Work order reset"),
                disable("inactive_assignment", "REQ-TRI-004"),
                disable("invalid_completion", "REQ-TRI-008"),
                disable("reopen_closed", "REQ-TRI-009"),
            ],
        ),
        folder("Workflow", workflow, WORKFLOW_SKIP),
        folder("Work hour boundaries", boundary, boundary_skip),
    ]


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    collections = {
        "learning.postman_collection.json": (
            "Package Sim Learning",
            "Learning API regression. " + SIMULATED,
            learning_items,
        ),
        "quality.postman_collection.json": (
            "Package Sim Quality",
            "Quality API regression. " + SIMULATED,
            quality_items,
        ),
        "workorders.postman_collection.json": (
            "Package Sim Work Orders",
            "Work-order API regression. " + SIMULATED,
            work_items,
        ),
    }
    out_dir = POSTMAN / "collections"
    out_dir.mkdir(parents=True, exist_ok=True)
    for filename, (name, description, builder) in collections.items():
        CURRENT["collection"] = name
        write_json(out_dir / filename, collection(name, description, builder()))

    env_dir = POSTMAN / "environments"
    env_dir.mkdir(parents=True, exist_ok=True)
    write_json(
        env_dir / "local.postman_environment.json",
        {
            "name": "Package Sim Local",
            "values": [
                {"key": "baseUrl", "value": "http://127.0.0.1:18765", "enabled": True},
                {"key": "forceDefects", "value": "false", "enabled": True},
            ],
            "_postman_variable_scope": "environment",
        },
    )

    data_dir = POSTMAN / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "pass_mark_boundaries.csv").write_text(
        "\n".join(
            [
                "score,expected_state,expected_score,test_case,requirement",
                "79.99,Failed,79.99,TC-INT-010,REQ-INT-004",
                "80.00,Passed,80.00,TC-INT-008,REQ-INT-004",
                "80.01,Passed,80.01,TC-INT-009,REQ-INT-004",
                "79.994,Failed,79.99,TC-INT-007,REQ-INT-003",
                "79.995,Passed,80.00,TC-INT-007,REQ-INT-003",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (data_dir / "quality_boundaries.csv").write_text(
        "\n".join(
            [
                "earned_a,earned_b,earned_c,expected_score,expected_classification,test_case,requirement",
                "1.9995,1,0,79.99,Below standard,TC-VER-007,REQ-VER-004",
                "2,1,0,80.00,Meets standard,TC-VER-007,REQ-VER-004",
                "2,1,0.0005,80.01,Meets standard,TC-VER-008,REQ-VER-004",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (data_dir / "work_hours_boundaries.csv").write_text(
        "\n".join(
            [
                "hours,expected_status,test_case,requirement",
                "0,422,TC-TRI-012,REQ-TRI-006",
                "0.01,200,TC-TRI-011,REQ-TRI-006",
                "24,200,TC-TRI-011,REQ-TRI-006",
                "24.01,422,TC-TRI-012,REQ-TRI-006",
                "",
            ]
        ),
        encoding="utf-8",
    )

    trace_path = ROOT / "docs" / "api_traceability.md"
    rows = [
        "| Requirement | Test Case | Postman Request | Newman Execution |",
        "| --- | --- | --- | --- |",
    ]
    for requirement, case, request_name, collection_name in TRACE:
        rows.append(
            f"| {requirement} | {case} | {collection_name} / {request_name} | Not run |"
        )
    trace_path.write_text(
        "\n".join(
            [
                "# API traceability",
                "",
                "**Milestone:** M5",
                "**Identifier:** SIMULATED",
                "**Status:** Postman requests mapped to M3 cases. Newman execution is filled after the defect-off run.",
                "",
                "Chain: Requirement → Test case → Postman request → Newman execution.",
                "",
                "CI is not wired. A passing Newman execution means the local defect-off run in `reports/api.json`.",
                "",
                *rows,
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"requests={len(TRACE)}")


if __name__ == "__main__":
    main()
