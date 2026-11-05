"""Simulator verification. These are not the M3 test-case catalog."""

from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from sim.app import DISCLAIMER, app

client = TestClient(app)

SECTIONS_PARTIAL = [
    {"id": "A", "earned": 1, "possible": 2},
    {"id": "B", "earned": 1, "possible": 1},
    {"id": "C", "earned": 1, "possible": 1},
]


@pytest.fixture(autouse=True)
def _reset():
    response = client.post("/test/reset")
    assert response.status_code == 200
    yield


def _defect(defect_id: str, enabled: bool) -> None:
    response = client.post(f"/api/defects/{defect_id}", json={"enabled": enabled})
    assert response.status_code == 200
    assert response.json()["enabled"] is enabled


def _order(order_id: str) -> dict:
    orders = client.get("/api/work/orders").json()
    return next(row for row in orders if row["id"] == order_id)


def _enroll_and_start() -> str:
    created = client.post(
        "/api/learning/enrollments",
        json={"learner_id": "LN-01", "activity_id": "ACT-102"},
    )
    assert created.status_code == 200
    enrollment_id = created.json()["id"]
    started = client.post(f"/api/learning/enrollments/{enrollment_id}/start")
    assert started.status_code == 200
    assert started.json()["state"] == "In Progress"
    return enrollment_id


def test_health_and_pages_are_labeled_simulated():
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {
        "status": "ok",
        "simulated": True,
        "service": "package-sim",
    }
    assert health.headers["X-Simulated"] == "true"
    for path in ("/", "/learning", "/quality", "/workorders", "/defects"):
        page = client.get(path)
        assert page.status_code == 200
        assert DISCLAIMER in page.text


def test_seed_counts_and_restoration():
    assert len(client.get("/api/learning/learners").json()) == 5
    assert len(client.get("/api/quality/evaluations").json()) == 5
    assert len(client.get("/api/work/orders").json()) == 10
    assert _order("WO-01")["state"] == "Draft"

    moved = client.post("/api/work/orders/WO-01/transition", json={"to": "WAPPR"})
    assert moved.status_code == 200
    _defect("pass_mark", False)

    restored = client.post("/test/reset")
    assert restored.json()["status"] == "reset"
    assert _order("WO-01")["state"] == "Draft"
    flags = {row["id"]: row["enabled"] for row in client.get("/api/defects").json()}
    assert flags["pass_mark"] is True
    assert len(client.get("/api/learning/learners").json()) == 5
    assert len(client.get("/api/quality/evaluations").json()) == 5
    assert len(client.get("/api/work/orders").json()) == 10


def test_learning_pass_boundary_and_illegal_completion():
    _defect("pass_mark", False)
    _defect("certificate_date", False)
    enrollment_id = _enroll_and_start()
    scored = client.post(
        f"/api/learning/enrollments/{enrollment_id}/assessment",
        json={"score": 79.995},
    )
    assert scored.status_code == 200
    assert scored.json()["score"] == 80.0
    assert scored.json()["state"] == "Passed"
    blocked = client.post(f"/api/learning/enrollments/ENR-04/complete")
    assert blocked.status_code == 409
    assert "Illegal transition Enrolled -> Completed" in blocked.json()["detail"]

    finished = client.post(f"/api/learning/enrollments/{enrollment_id}/complete")
    assert finished.status_code == 200
    assert finished.json()["state"] == "Completed"
    certificate = next(
        row
        for row in client.get("/api/learning/certificates").json()
        if row["enrollment_id"] == enrollment_id
    )
    assert certificate["issued_on"] == certificate["completion_date"]


def test_pass_mark_defect_fails_exact_threshold():
    enrollment_id = _enroll_and_start()
    scored = client.post(
        f"/api/learning/enrollments/{enrollment_id}/assessment",
        json={"score": 80},
    )
    assert scored.status_code == 200
    assert scored.json()["state"] == "Failed"
    above = client.post(
        "/api/learning/enrollments",
        json={"learner_id": "LN-02", "activity_id": "ACT-102"},
    )
    assert above.status_code == 200
    other = above.json()["id"]
    assert client.post(f"/api/learning/enrollments/{other}/start").status_code == 200
    higher = client.post(
        f"/api/learning/enrollments/{other}/assessment",
        json={"score": 80.01},
    )
    assert higher.json()["state"] == "Passed"


def test_certificate_date_defect_is_one_day_early():
    enrollment_id = _enroll_and_start()
    assert client.post(
        f"/api/learning/enrollments/{enrollment_id}/assessment",
        json={"score": 91},
    ).status_code == 200
    finished = client.post(f"/api/learning/enrollments/{enrollment_id}/complete")
    assert finished.status_code == 200
    certificate = next(
        row
        for row in client.get("/api/learning/certificates").json()
        if row["enrollment_id"] == enrollment_id
    )
    issued = date.fromisoformat(certificate["issued_on"])
    completed = date.fromisoformat(certificate["completion_date"])
    assert issued == completed - timedelta(days=1)


def test_quality_transitions_score_and_calculation_defect():
    pending = client.post(f"/api/quality/evaluations/EV-01/complete")
    assert pending.status_code == 409

    wrong = client.post(
        "/api/quality/evaluations/EV-01/submit",
        json={"sections": SECTIONS_PARTIAL},
    )
    assert wrong.status_code == 200
    assert wrong.json()["state"] == "Under Review"
    assert wrong.json()["score"] == pytest.approx(83.33, abs=0.001)
    assert wrong.json()["classification"] == "Meets standard"

    client.post("/test/reset")
    _defect("quality_score", False)
    right = client.post(
        "/api/quality/evaluations/EV-01/submit",
        json={"sections": SECTIONS_PARTIAL},
    )
    assert right.status_code == 200
    assert right.json()["score"] == 70.0
    assert right.json()["classification"] == "Below standard"

    disputed = client.post("/api/quality/evaluations/EV-04/complete")
    assert disputed.status_code == 409
    resolved = client.post("/api/quality/evaluations/EV-04/resolve")
    assert resolved.status_code == 200
    assert resolved.json()["state"] == "Under Review"

    acknowledged = client.post("/api/quality/evaluations/EV-03/complete")
    assert acknowledged.status_code == 200
    assert acknowledged.json()["state"] == "Completed"

    empty = client.post(
        "/api/quality/evaluations/EV-02/dispute",
        json={"comment": "   "},
    )
    assert empty.status_code == 422


def test_work_order_legal_and_illegal_transitions():
    draft = client.post("/api/work/orders/WO-01/transition", json={"to": "WAPPR"})
    assert draft.status_code == 200
    assert draft.json()["state"] == "WAPPR"

    self_approval = client.post(
        "/api/work/orders/WO-02/transition",
        json={"to": "APPR", "actor_id": "RQ-02"},
    )
    assert self_approval.status_code == 409
    approved = client.post(
        "/api/work/orders/WO-02/transition",
        json={"to": "APPR", "actor_id": "AP-01"},
    )
    assert approved.status_code == 200
    assert approved.json()["state"] == "APPR"

    unassigned = client.post("/api/work/orders/WO-03/transition", json={"to": "INPRG"})
    assert unassigned.status_code == 409
    started = client.post("/api/work/orders/WO-04/transition", json={"to": "INPRG"})
    assert started.status_code == 200
    assert started.json()["state"] == "INPRG"

    skip_close = client.post("/api/work/orders/WO-05/transition", json={"to": "CLOSE"})
    assert skip_close.status_code == 409
    assert "INPRG -> CLOSE" in skip_close.json()["detail"]

    waiting = client.post("/api/work/orders/WO-06/transition", json={"to": "COMP"})
    assert waiting.status_code == 409
    resumed = client.post("/api/work/orders/WO-06/transition", json={"to": "INPRG"})
    assert resumed.status_code == 200

    missing_reason = client.post("/api/work/orders/WO-07/transition", json={"to": "INPRG"})
    assert missing_reason.status_code == 422
    rework = client.post(
        "/api/work/orders/WO-07/transition",
        json={"to": "INPRG", "reason": "Rail still moves"},
    )
    assert rework.status_code == 200
    assert rework.json()["state"] == "INPRG"
    assert rework.json()["completed_at"] is None

    completed = client.post("/api/work/orders/WO-09/transition", json={"to": "COMP"})
    assert completed.status_code == 200
    closed = client.post("/api/work/orders/WO-09/transition", json={"to": "CLOSE"})
    assert closed.status_code == 200
    assert closed.json()["state"] == "CLOSE"


def test_planted_work_order_defects_toggle():
    closed = client.post("/api/work/orders/WO-08/transition", json={"to": "INPRG"})
    assert closed.status_code == 200
    assert closed.json()["reopened"] is True
    _defect("reopen_closed", False)
    client.post("/test/reset")
    _defect("reopen_closed", False)
    rejected = client.post("/api/work/orders/WO-08/transition", json={"to": "INPRG"})
    assert rejected.status_code == 409

    _defect("invalid_completion", False)
    skipped = client.post("/api/work/orders/WO-10/transition", json={"to": "COMP"})
    assert skipped.status_code == 409
    _defect("invalid_completion", True)
    allowed = client.post("/api/work/orders/WO-10/transition", json={"to": "COMP"})
    assert allowed.status_code == 200
    assert allowed.json()["state"] == "COMP"
    still_blocked = client.post("/api/work/orders/WO-09/transition", json={"to": "CLOSE"})
    assert still_blocked.status_code == 409

    inactive = client.post(
        "/api/work/orders/WO-03/assign",
        json={"technician_id": "TEC-02"},
    )
    assert inactive.status_code == 200
    _defect("inactive_assignment", False)
    client.post("/test/reset")
    _defect("inactive_assignment", False)
    blocked = client.post(
        "/api/work/orders/WO-03/assign",
        json={"technician_id": "TEC-02"},
    )
    assert blocked.status_code == 409
    active = client.post(
        "/api/work/orders/WO-03/assign",
        json={"technician_id": "TEC-01"},
    )
    assert active.status_code == 200
    assert active.json()["technician_id"] == "TEC-01"


def test_time_entry_bounds_follow_state():
    accepted = client.post(
        "/api/work/orders/WO-05/time",
        json={"technician_id": "TEC-01", "hours": 24},
    )
    assert accepted.status_code == 200
    rejected = client.post(
        "/api/work/orders/WO-05/time",
        json={"technician_id": "TEC-01", "hours": 24.01},
    )
    assert rejected.status_code == 422
    closed = client.post(
        "/api/work/orders/WO-08/time",
        json={"technician_id": "TEC-01", "hours": 1},
    )
    assert closed.status_code == 409


def test_unpublished_activity_and_duplicate_enrollment_are_rejected():
    draft = client.post(
        "/api/learning/enrollments",
        json={"learner_id": "LN-01", "activity_id": "ACT-103"},
    )
    assert draft.status_code == 409
    duplicate = client.post(
        "/api/learning/enrollments",
        json={"learner_id": "LN-04", "activity_id": "ACT-101"},
    )
    assert duplicate.status_code == 409
