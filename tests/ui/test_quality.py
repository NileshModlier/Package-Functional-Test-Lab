"""Quality UI regression. Mapped to M3 cases. Not Postman or CI."""

import pytest
from playwright.sync_api import expect

pytestmark = [pytest.mark.regression]


@pytest.mark.critical
def test_all_yes_scores_100(evaluation, defects):
    """
    TC-VER-004
    REQ-VER-003
    Equivalence Partitioning
    """
    defects.disable("quality_score")
    evaluation.open()
    evaluation.submit("EV-01", "2", "1", "1")
    evaluation.expect_state("EV-01", "Under Review")
    evaluation.expect_summary_contains("EV-01", "Score 100.0 ·")
    evaluation.expect_summary_contains("EV-01", "Meets standard")


@pytest.mark.critical
def test_weighted_sections_score_70(evaluation, defects):
    """
    TC-VER-005
    REQ-VER-002
    REQ-VER-003
    Decision Table Testing
    """
    defects.disable("quality_score")
    evaluation.open()
    evaluation.submit("EV-01", "1", "1", "1")
    evaluation.expect_state("EV-01", "Under Review")
    evaluation.expect_summary_contains("EV-01", "Score 70.0 ·")
    evaluation.expect_summary_contains("EV-01", "Below standard")


@pytest.mark.critical
def test_threshold_79_99_is_below_and_80_meets(evaluation, defects):
    """
    TC-VER-007
    REQ-VER-004
    Boundary Value Analysis
    """
    defects.disable("quality_score")
    evaluation.open()
    evaluation.submit("EV-01", "1.9995", "1", "0")
    evaluation.expect_summary_contains("EV-01", "Score 79.99")
    evaluation.expect_summary_contains("EV-01", "Below standard")


@pytest.mark.critical
def test_threshold_80_01_meets_standard(evaluation, defects):
    """
    TC-VER-008
    REQ-VER-004
    Boundary Value Analysis
    """
    defects.disable("quality_score")
    evaluation.open()
    evaluation.submit("EV-01", "2", "1", "0.0005")
    evaluation.expect_summary_contains("EV-01", "Score 80.01")
    evaluation.expect_summary_contains("EV-01", "Meets standard")


@pytest.mark.critical
def test_acknowledge_keeps_the_score(evaluation):
    """
    TC-VER-009
    REQ-VER-006
    State Transition Testing
    """
    evaluation.acknowledge("EV-02")
    evaluation.expect_state("EV-02", "Acknowledged")
    evaluation.expect_summary_contains("EV-02", "Score 70.0 ·")


def test_pending_evaluation_has_no_acknowledge_action(evaluation):
    """
    TC-VER-010
    REQ-VER-006
    Negative Testing
    """
    evaluation.expect_state("EV-01", "Pending")
    evaluation.expect_acknowledge_absent("EV-01")


@pytest.mark.critical
def test_dispute_stores_the_comment_and_keeps_the_score(evaluation):
    """
    TC-VER-011
    REQ-VER-007
    State Transition Testing
    """
    evaluation.dispute("EV-02", "The greeting question does not match the call.")
    evaluation.expect_state("EV-02", "Disputed")
    evaluation.expect_summary_contains("EV-02", "Score 70.0 ·")
    expect(evaluation.evaluation("EV-02").get_by_test_id("dispute-text")).to_contain_text(
        "does not match the call"
    )


def test_coaching_does_not_change_the_score(evaluation):
    """
    TC-VER-015
    REQ-VER-008
    Decision Table Testing
    """
    evaluation.coach("EV-02", "Score must stay 70.")
    evaluation.expect_state("EV-02", "Coached")
    evaluation.expect_summary_contains("EV-02", "Score 70.0 ·")
    evaluation.expect_summary_contains("EV-02", "Below standard")
