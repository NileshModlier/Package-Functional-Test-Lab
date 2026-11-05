"""UI fixtures. Chromium only. Every test reloads the simulator seed."""

from __future__ import annotations

import os
import sys
import time
import subprocess
import urllib.request
from pathlib import Path

import httpx
import pytest
from playwright.sync_api import Page, expect

ROOT = Path(__file__).resolve().parents[2]
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from pages.learning_page import LearningPage
from pages.quality_page import EvaluationPage
from pages.workorder_page import WorkOrderPage

PORT = 18765
BASE = f"http://127.0.0.1:{PORT}"


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: short path through a primary page")
    config.addinivalue_line("markers", "regression: high-priority UI regression")
    config.addinivalue_line("markers", "critical: outcome that grants or withholds a result")


@pytest.fixture(scope="session")
def browser_name():
    return "chromium"


def _wait_until_healthy() -> bool:
    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{BASE}/health", timeout=1) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.25)
    return False


@pytest.fixture(scope="session")
def sim_server():
    # CI starts Package Sim before pytest and sets SIM_EXTERNAL=1.
    # Leaving that process running lets Newman use the same server.
    if os.environ.get("SIM_EXTERNAL") == "1":
        if not _wait_until_healthy():
            raise RuntimeError("Package Sim did not become ready")
        yield BASE
        return

    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "sim.app:app", "--host", "127.0.0.1", "--port", str(PORT)],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if not _wait_until_healthy():
        process.terminate()
        raise RuntimeError("Package Sim did not become ready")
    yield BASE
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


@pytest.fixture(scope="session")
def base_url(sim_server):
    return sim_server


@pytest.fixture(autouse=True)
def reset_sim(sim_server):
    """Reload seed.json before every UI test."""
    response = httpx.post(f"{sim_server}/test/reset", timeout=10)
    assert response.status_code == 200
    yield


class DefectControls:
    def __init__(self, page: Page):
        self.page = page

    def set_enabled(self, defect_id: str, enabled: bool) -> None:
        """Leave the seeded switch unchanged when SIM_FORCE_DEFECTS=on."""
        if os.environ.get("SIM_FORCE_DEFECTS") == "on":
            return
        self.page.goto("/defects")
        card = self.page.get_by_test_id(f"defect-{defect_id}")
        state = card.get_by_test_id("defect-state")
        action = "Turn off" if not enabled else "Turn on"
        toggle = card.get_by_test_id("defect-toggle")
        if toggle.inner_text() == action:
            toggle.click()
        expect(state).to_have_text("ON" if enabled else "OFF")

    def disable(self, defect_id: str) -> None:
        self.set_enabled(defect_id, False)


@pytest.fixture
def defects(page: Page, reset_sim):
    return DefectControls(page)


@pytest.fixture
def learning(page: Page, reset_sim):
    view = LearningPage(page)
    view.open()
    return view


@pytest.fixture
def evaluation(page: Page, reset_sim):
    view = EvaluationPage(page)
    view.open()
    return view


@pytest.fixture
def workorders(page: Page, reset_sim):
    view = WorkOrderPage(page)
    view.open()
    return view
