"""Learning UI regression. Mapped to M3 cases. Not Postman or CI."""

import pytest
from playwright.sync_api import expect

pytestmark = [pytest.mark.regression]


@pytest.mark.smoke
def test_enroll_available_activity(learning):
    """
    TC-INT-001
    REQ-INT-001
    Equivalence Partitioning
    """
    expect(learning.page.get_by_test_id("simulated-banner")).to_be_visible()
    learning.enroll("LN-01", "ACT-102")
    created = learning.page.locator("[data-testid^='enrollment-']").filter(has_text="ACT-102").filter(has_text="LN-01")
    expect(created.get_by_test_id("state")).to_have_text("Enrolled")
    expect(created.get_by_test_id("summary")).to_contain_text("Score —")


def test_duplicate_enrollment_is_rejected(learning):
    """
    TC-INT-002
    REQ-INT-001
    Negative Testing
    """
    learning.enroll("LN-04", "ACT-101")
    learning.expect_error("active enrollment already exists")
    learning.expect_state("ENR-04", "Enrolled")


def test_start_marks_content_modules_complete(learning):
    """
    TC-INT-004
    REQ-INT-002
    State Transition Testing
    """
    learning.start("ENR-04")
    learning.expect_state("ENR-04", "In Progress")
    learning.expect_module("ENR-04", "MOD-1", "Complete")
    learning.expect_module("ENR-04", "MOD-2", "Complete")
    learning.expect_module("ENR-04", "MOD-3", "Not started")


@pytest.mark.critical
def test_score_80_passes_when_pass_mark_defect_is_off(learning, defects):
    """
    TC-INT-008
    REQ-INT-004
    Boundary Value Analysis
    """
    defects.disable("pass_mark")
    learning.open()
    learning.submit_score("ENR-01", "80.00")
    learning.expect_state("ENR-01", "Passed")
    learning.expect_summary_contains("ENR-01", "Score 80.0 ·")


@pytest.mark.critical
def test_score_80_01_passes(learning):
    """
    TC-INT-009
    REQ-INT-004
    Boundary Value Analysis
    """
    learning.submit_score("ENR-01", "80.01")
    learning.expect_state("ENR-01", "Passed")
    learning.expect_summary_contains("ENR-01", "Score 80.01")


@pytest.mark.critical
def test_score_79_99_fails_without_a_certificate(learning):
    """
    TC-INT-010
    REQ-INT-004
    REQ-INT-005
    Boundary Value Analysis
    """
    learning.submit_score("ENR-01", "79.99")
    learning.expect_state("ENR-01", "Failed")
    learning.expect_summary_contains("ENR-01", "Score 79.99")
    expect(learning.enrollment("ENR-01").get_by_test_id("certificate")).to_have_count(0)


@pytest.mark.critical
def test_passed_enrollment_completes_once(learning, defects):
    """
    TC-INT-014
    REQ-INT-006
    State Transition Testing
    """
    defects.disable("certificate_date")
    learning.open()
    learning.complete("ENR-02")
    learning.expect_state("ENR-02", "Completed")
    learning.expect_complete_absent("ENR-02")


@pytest.mark.critical
def test_certificate_issued_date_matches_completion(learning, defects):
    """
    TC-INT-016
    REQ-INT-007
    Decision Table Testing
    """
    defects.disable("certificate_date")
    learning.open()
    learning.complete("ENR-02")
    learning.expect_certificate_dates_match("LN-02")
