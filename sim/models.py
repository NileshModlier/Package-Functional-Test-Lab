"""In-memory store for the simulated lab. Reloaded from seed.json."""

from __future__ import annotations

import json
from pathlib import Path

SEED_PATH = Path(__file__).with_name("seed.json")


class SimError(Exception):
    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class Store:
    def __init__(self) -> None:
        self.data: dict = {}
        self.reset()

    def reset(self) -> dict:
        self.data = json.loads(SEED_PATH.read_text(encoding="utf-8"))
        return self.data


store = Store()


def find(collection: str, item_id: str) -> dict:
    for item in store.data[collection]:
        if item["id"] == item_id:
            return item
    raise SimError(404, f"{item_id} was not found in {collection}")


def next_id(collection: str, prefix: str) -> str:
    highest = 0
    for item in store.data[collection]:
        tail = str(item["id"]).rsplit("-", 1)[-1]
        if tail.isdigit():
            highest = max(highest, int(tail))
    return f"{prefix}-{highest + 1:02d}"
