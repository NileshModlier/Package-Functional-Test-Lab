"""Simulated learning workflow. Not an Intellum product."""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

from .defects import is_on
from .models import SimError, find, next_id, store

ACTIVE = {"Enrolled", "In Progress", "Passed", "Failed"}
PASS_MARK = Decimal("80.00")


def _q2(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _iso(value: Decimal) -> float:
    return float(value)


def list_activities() -> list[dict]:
    return store.data["activities"]


def list_learners() -> list[dict]:
    return store.data["learners"]


def list_enrollments() -> list[dict]:
    return store.data["enrollments"]


def list_certificates() -> list[dict]:
    return store.data["certificates"]


def enroll(learner_id: str, activity_id: str) -> dict:
    find("learners", learner_id)
    activity = find("activities", activity_id)
    if activity["status"] != "Available":
        raise SimError(409, "Activity is not available for enrollment")
    for row in store.data["enrollments"]:
        if (
            row["learner_id"] == learner_id
            and row["activity_id"] == activity_id
            and row["state"] in ACTIVE
        ):
            raise SimError(409, "An active enrollment already exists for this learner and activity")
    enrollment = {
        "id": next_id("enrollments", "ENR"),
        "learner_id": learner_id,
        "activity_id": activity_id,
        "state": "Enrolled",
        "score": None,
        "attempts": 0,
        "attempt_history": [],
        "completion_date": None,
        "certificate_id": None,
        "modules": [
            {
                "id": module["id"],
                "title": module["title"],
                "kind": module["kind"],
                "status": "Not started",
            }
            for module in activity["modules"]
        ],
    }
    store.data["enrollments"].append(enrollment)
    return enrollment


def start(enrollment_id: str) -> dict:
    enrollment = find("enrollments", enrollment_id)
    _require(enrollment, "Enrolled", "In Progress")
    enrollment["state"] = "In Progress"
    for module in enrollment["modules"]:
        if module["kind"] == "content":
            module["status"] = "Complete"
    return enrollment


def assess(enrollment_id: str, score) -> dict:
    enrollment = find("enrollments", enrollment_id)
    if enrollment["state"] != "In Progress":
        raise SimError(
            409,
            f"Illegal transition {enrollment['state']} -> assessment",
        )
    if enrollment["attempts"] >= 3:
        raise SimError(409, "Attempts exhausted")
    rounded = _q2(score)
    if rounded < Decimal("0.00") or rounded > Decimal("100.00"):
        raise SimError(422, "Score must be between 0.00 and 100.00")
    passed = _is_pass(rounded)
    enrollment["attempts"] += 1
    enrollment["score"] = _iso(rounded)
    enrollment["state"] = "Passed" if passed else "Failed"
    enrollment["attempt_history"].append(
        {"attempt": enrollment["attempts"], "score": _iso(rounded), "outcome": enrollment["state"]}
    )
    for module in enrollment["modules"]:
        if module["kind"] == "assessment":
            module["status"] = enrollment["state"]
    return enrollment


def reset_attempt(enrollment_id: str) -> dict:
    enrollment = find("enrollments", enrollment_id)
    if enrollment["state"] != "Failed":
        raise SimError(409, f"Illegal transition {enrollment['state']} -> Enrolled")
    if enrollment["attempts"] >= 3:
        raise SimError(409, "Attempts exhausted")
    enrollment["state"] = "Enrolled"
    enrollment["score"] = None
    for module in enrollment["modules"]:
        if module["kind"] == "assessment":
            module["status"] = "Not started"
    return enrollment


def complete(enrollment_id: str) -> dict:
    enrollment = find("enrollments", enrollment_id)
    if enrollment["state"] != "Passed":
        raise SimError(409, f"Illegal transition {enrollment['state']} -> Completed")
    activity = find("activities", enrollment["activity_id"])
    completed_on = date.today()
    enrollment["state"] = "Completed"
    enrollment["completion_date"] = completed_on.isoformat()
    if activity.get("certificate"):
        issued = completed_on - timedelta(days=1) if is_on("certificate_date") else completed_on
        sequence = _next_certificate_sequence(activity["id"], completed_on.year)
        code = f"SIM-CERT-{activity['code']}-{completed_on.year}-{sequence:02d}"
        expires = _add_months(completed_on, int(activity.get("expiration_months") or 0))
        certificate = {
            "id": code,
            "enrollment_id": enrollment["id"],
            "learner_id": enrollment["learner_id"],
            "activity_id": activity["id"],
            "issued_on": issued.isoformat(),
            "completion_date": completed_on.isoformat(),
            "expires_on": expires.isoformat() if expires else None,
            "score": enrollment["score"],
        }
        store.data["certificates"].append(certificate)
        enrollment["certificate_id"] = code
    return enrollment


def _is_pass(score: Decimal) -> bool:
    if is_on("pass_mark"):
        return score > PASS_MARK
    return score >= PASS_MARK


def _require(enrollment: dict, source: str, target: str) -> None:
    if enrollment["state"] != source:
        raise SimError(409, f"Illegal transition {enrollment['state']} -> {target}")


def _next_certificate_sequence(activity_id: str, year: int) -> int:
    activity = find("activities", activity_id)
    prefix = f"SIM-CERT-{activity['code']}-{year}-"
    count = sum(1 for row in store.data["certificates"] if str(row["id"]).startswith(prefix))
    return count + 1


def _add_months(value: date, months: int) -> date | None:
    if months <= 0:
        return None
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, _month_length(year, month))
    return date(year, month, day)


def _month_length(year: int, month: int) -> int:
    if month == 12:
        nxt = date(year + 1, 1, 1)
    else:
        nxt = date(year, month + 1, 1)
    return (nxt - timedelta(days=1)).day
