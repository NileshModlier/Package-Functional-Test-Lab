"""Runtime switches for planted defects.

Each switch defaults to ON from seed.json so the lab exhibits the defect
until a tester turns it off. POST /test/reset restores those defaults.
"""

from __future__ import annotations

from .models import SimError, store

CATALOG = [
    {
        "id": "pass_mark",
        "title": "Pass mark bug",
        "workflow": "Learning",
        "requirement": "REQ-INT-004",
        "summary": (
            "When ON, an assessment passes only when the rounded score is "
            "greater than 80. A score of 80.00 fails. When OFF, the score "
            "passes when it is greater than or equal to 80.00."
        ),
    },
    {
        "id": "certificate_date",
        "title": "Certificate date offset",
        "workflow": "Learning",
        "requirement": "REQ-INT-007",
        "summary": (
            "When ON, the certificate issued_on date is one day earlier than "
            "the enrollment completion_date. When OFF, the two dates match."
        ),
    },
    {
        "id": "quality_score",
        "title": "Quality score calculation error",
        "workflow": "Quality",
        "requirement": "REQ-VER-003",
        "summary": (
            "When ON, the total is the unweighted mean of the three section "
            "percents. Section weights 60, 20, and 20 are ignored. When OFF, "
            "each section percent is multiplied by its weight and divided by 100."
        ),
    },
    {
        "id": "reopen_closed",
        "title": "Work order reopen bug",
        "workflow": "Work orders",
        "requirement": "REQ-TRI-009",
        "summary": (
            "When ON, a CLOSE work order can move to INPRG. When OFF, that "
            "transition returns HTTP 409. Other illegal exits from CLOSE stay rejected."
        ),
    },
    {
        "id": "invalid_completion",
        "title": "Invalid completion state bug",
        "workflow": "Work orders",
        "requirement": "REQ-TRI-008",
        "summary": (
            "When ON, a work order can move from APPR directly to COMP. "
            "When OFF, COMP is accepted only from INPRG. INPRG to CLOSE stays "
            "rejected in both switch positions."
        ),
    },
    {
        "id": "inactive_assignment",
        "title": "Assignment bug",
        "workflow": "Work orders",
        "requirement": "REQ-TRI-004",
        "summary": (
            "When ON, an inactive technician can be assigned. When OFF, that "
            "assignment returns HTTP 409. Assignment onto a closed order stays rejected."
        ),
    },
]


def is_on(defect_id: str) -> bool:
    flags = store.data["defects"]
    if defect_id not in flags:
        raise SimError(404, f"Unknown defect {defect_id}")
    return bool(flags[defect_id])


def list_defects() -> list[dict]:
    flags = store.data["defects"]
    rows = []
    for item in CATALOG:
        rows.append({**item, "enabled": bool(flags[item["id"]])})
    return rows


def set_enabled(defect_id: str, enabled: bool) -> dict:
    if defect_id not in store.data["defects"]:
        raise SimError(404, f"Unknown defect {defect_id}")
    store.data["defects"][defect_id] = bool(enabled)
    return next(row for row in list_defects() if row["id"] == defect_id)
