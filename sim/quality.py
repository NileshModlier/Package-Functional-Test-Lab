"""Simulated quality workflow. Not a Verint product."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from .defects import is_on
from .models import SimError, find, next_id, store

WEIGHTS = {"A": Decimal("60"), "B": Decimal("20"), "C": Decimal("20")}
THRESHOLD = Decimal("80.00")


def list_interactions() -> list[dict]:
    return store.data["interactions"]


def list_evaluations() -> list[dict]:
    return store.data["evaluations"]


def create_evaluation(interaction_id: str) -> dict:
    interaction = find("interactions", interaction_id)
    evaluation = {
        "id": next_id("evaluations", "EV"),
        "interaction_id": interaction["id"],
        "agent_id": interaction["agent_id"],
        "agent_name": interaction["agent_name"],
        "state": "Pending",
        "score": None,
        "classification": None,
        "sections": None,
        "acknowledged_at": None,
        "dispute_comment": None,
        "coaching_note": None,
    }
    store.data["evaluations"].append(evaluation)
    return evaluation


def submit(evaluation_id: str, sections: list[dict]) -> dict:
    evaluation = find("evaluations", evaluation_id)
    if evaluation["state"] != "Pending":
        raise SimError(409, f"Illegal transition {evaluation['state']} -> Under Review")
    total = _score(sections)
    evaluation["sections"] = sections
    evaluation["score"] = float(total)
    evaluation["classification"] = (
        "Meets standard" if total >= THRESHOLD else "Below standard"
    )
    evaluation["state"] = "Under Review"
    return evaluation


def acknowledge(evaluation_id: str) -> dict:
    evaluation = find("evaluations", evaluation_id)
    if evaluation["state"] not in {"Under Review", "Coached"}:
        raise SimError(409, f"Illegal transition {evaluation['state']} -> Acknowledged")
    evaluation["state"] = "Acknowledged"
    if not evaluation["acknowledged_at"]:
        evaluation["acknowledged_at"] = _now()
    return evaluation


def dispute(evaluation_id: str, comment: str) -> dict:
    evaluation = find("evaluations", evaluation_id)
    if evaluation["state"] != "Under Review":
        raise SimError(409, f"Illegal transition {evaluation['state']} -> Disputed")
    text = (comment or "").strip()
    if not text:
        raise SimError(422, "A dispute requires a comment")
    evaluation["state"] = "Disputed"
    evaluation["dispute_comment"] = text
    return evaluation


def resolve(evaluation_id: str) -> dict:
    evaluation = find("evaluations", evaluation_id)
    if evaluation["state"] != "Disputed":
        raise SimError(409, f"Illegal transition {evaluation['state']} -> Under Review")
    evaluation["state"] = "Under Review"
    return evaluation


def coach(evaluation_id: str, note: str) -> dict:
    evaluation = find("evaluations", evaluation_id)
    if evaluation["state"] not in {"Under Review", "Acknowledged"}:
        raise SimError(409, f"Illegal transition {evaluation['state']} -> Coached")
    text = (note or "").strip()
    if not text:
        raise SimError(422, "Coaching requires a note")
    evaluation["state"] = "Coached"
    evaluation["coaching_note"] = text
    return evaluation


def complete(evaluation_id: str) -> dict:
    evaluation = find("evaluations", evaluation_id)
    if evaluation["state"] not in {"Acknowledged", "Coached"}:
        raise SimError(409, f"Illegal transition {evaluation['state']} -> Completed")
    evaluation["state"] = "Completed"
    return evaluation


def _score(sections: list[dict]) -> Decimal:
    by_id = {}
    for section in sections:
        section_id = section["id"]
        if section_id not in WEIGHTS or section_id in by_id:
            raise SimError(422, "Sections A, B, and C are required exactly once")
        earned = Decimal(str(section["earned"]))
        possible = Decimal(str(section["possible"]))
        if possible <= 0 or earned < 0 or earned > possible:
            raise SimError(422, f"Section {section_id} points are out of range")
        by_id[section_id] = (earned / possible) * Decimal("100")
    if set(by_id) != set(WEIGHTS):
        raise SimError(422, "Sections A, B, and C are required exactly once")
    if is_on("quality_score"):
        total = sum(by_id.values(), Decimal("0")) / Decimal(len(by_id))
    else:
        total = sum(
            (by_id[key] * WEIGHTS[key] / Decimal("100") for key in WEIGHTS),
            Decimal("0"),
        )
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
