"""Simulated facilities work-order workflow. Not an IBM TRIRIGA or Maximo product."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from .defects import is_on
from .models import SimError, find, next_id, store

# Legal path for the simulated corrective work order.
# COMP -> INPRG is the approved rework transition from the M1 assumption register.
LEGAL = {
    "Draft": {"WAPPR"},
    "WAPPR": {"APPR"},
    "APPR": {"INPRG", "WMATL"},
    "INPRG": {"WMATL", "COMP"},
    "WMATL": {"INPRG"},
    "COMP": {"CLOSE", "INPRG"},
    "CLOSE": set(),
}
ACTUAL_STATES = {"APPR", "INPRG", "WMATL", "COMP"}
ASSIGN_STATES = {"APPR", "INPRG", "WMATL"}


def list_orders() -> list[dict]:
    return store.data["work_orders"]


def list_technicians() -> list[dict]:
    return store.data["technicians"]


def create_order(payload: dict) -> dict:
    required = ("title", "requester_id", "building", "request_class", "description")
    missing = [name for name in required if not str(payload.get(name) or "").strip()]
    if missing:
        raise SimError(422, "Required fields missing: " + ", ".join(missing))
    order = {
        "id": next_id("work_orders", "WO"),
        "title": payload["title"].strip(),
        "requester_id": payload["requester_id"].strip(),
        "building": payload["building"].strip(),
        "request_class": payload["request_class"].strip(),
        "description": payload["description"].strip(),
        "state": "Draft",
        "technician_id": None,
        "completed_at": None,
        "closed_at": None,
        "reopened": False,
        "rejection_reason": None,
        "time_entries": [],
        "material_entries": [],
    }
    store.data["work_orders"].append(order)
    return order


def transition(order_id: str, target: str, actor_id: str | None = None, reason: str | None = None) -> dict:
    order = find("work_orders", order_id)
    source = order["state"]
    if target not in _known_states():
        raise SimError(422, f"Unknown state {target}")
    if not _allowed(source, target):
        raise SimError(409, f"Illegal transition {source} -> {target}")
    if source == "WAPPR" and target == "APPR":
        if not actor_id:
            raise SimError(422, "Approval requires an actor_id")
        if actor_id == order["requester_id"]:
            raise SimError(409, "The requester cannot approve their own request")
        order["approved_by"] = actor_id
    if source == "APPR" and target == "INPRG" and not order.get("technician_id"):
        raise SimError(409, "Illegal transition APPR -> INPRG without an assigned technician")
    if source == "COMP" and target == "INPRG":
        text = (reason or "").strip()
        if not text:
            raise SimError(422, "Rework requires a reason")
        order["rejection_reason"] = text
        order["completed_at"] = None
    if target == "COMP":
        order["completed_at"] = _now()
    if target == "CLOSE":
        order["closed_at"] = _now()
    if source == "CLOSE" and target == "INPRG":
        order["reopened"] = True
        order["closed_at"] = None
    order["state"] = target
    return order


def assign(order_id: str, technician_id: str) -> dict:
    order = find("work_orders", order_id)
    if order["state"] not in ASSIGN_STATES:
        raise SimError(409, f"Illegal assignment while {order['state']}")
    technician = find("technicians", technician_id)
    if not technician["active"] and not is_on("inactive_assignment"):
        raise SimError(409, "Illegal assignment of inactive technician")
    order["technician_id"] = technician_id
    return order


def add_time(order_id: str, technician_id: str, hours) -> dict:
    order = find("work_orders", order_id)
    _require_actuals(order)
    find("technicians", technician_id)
    amount = Decimal(str(hours)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if amount <= Decimal("0.00") or amount > Decimal("24.00"):
        raise SimError(422, "Hours must be greater than 0 and at most 24.00")
    order["time_entries"].append(
        {"technician_id": technician_id, "hours": float(amount), "entered_at": _now()}
    )
    return order


def add_material(order_id: str, item_id: str, quantity) -> dict:
    order = find("work_orders", order_id)
    _require_actuals(order)
    amount = Decimal(str(quantity)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if amount <= Decimal("0.00"):
        raise SimError(422, "Quantity must be greater than 0")
    if not str(item_id or "").strip():
        raise SimError(422, "An item_id is required")
    order["material_entries"].append(
        {"item_id": item_id.strip(), "quantity": float(amount), "entered_at": _now()}
    )
    return order


def _allowed(source: str, target: str) -> bool:
    if target in LEGAL.get(source, set()):
        return True
    if source == "CLOSE" and target == "INPRG" and is_on("reopen_closed"):
        return True
    if source == "APPR" and target == "COMP" and is_on("invalid_completion"):
        return True
    return False


def _known_states() -> set[str]:
    return set(LEGAL)


def _require_actuals(order: dict) -> None:
    if order["state"] not in ACTUAL_STATES:
        raise SimError(409, f"Illegal actuals while {order['state']}")


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
