"""Work-order UI regression. Mapped to M3 cases. Not Postman or CI."""

import pytest

pytestmark = [pytest.mark.regression]


@pytest.mark.critical
def test_requester_cannot_approve_their_own_request(workorders):
    """
    TC-TRI-003
    REQ-TRI-002
    Negative Testing
    """
    workorders.transition("WO-02", "APPR", actor_id="RQ-02")
    workorders.expect_error("cannot approve their own request")
    workorders.expect_state("WO-02", "WAPPR")


@pytest.mark.critical
def test_different_person_can_approve(workorders):
    """
    TC-TRI-004
    REQ-TRI-002
    State Transition Testing
    """
    workorders.transition("WO-02", "APPR", actor_id="AP-01")
    workorders.expect_state("WO-02", "APPR")


def test_inactive_technician_is_rejected(workorders, defects):
    """
    TC-TRI-008
    REQ-TRI-004
    Decision Table Testing
    """
    defects.disable("inactive_assignment")
    workorders.open()
    workorders.assign("WO-03", "TEC-02")
    workorders.expect_error("inactive technician")
    workorders.expect_assignment_contains("WO-03", "unassigned")
    workorders.expect_state("WO-03", "APPR")


@pytest.mark.critical
def test_in_progress_work_can_be_completed(workorders, defects):
    """
    TC-TRI-016
    REQ-TRI-008
    State Transition Testing
    """
    defects.disable("invalid_completion")
    workorders.open()
    workorders.transition("WO-05", "COMP")
    workorders.expect_state("WO-05", "COMP")


@pytest.mark.critical
def test_approved_order_cannot_complete(workorders, defects):
    """
    TC-TRI-017
    REQ-TRI-008
    Negative Testing
    """
    defects.disable("invalid_completion")
    workorders.open()
    workorders.transition("WO-10", "COMP")
    workorders.expect_error("APPR -> COMP")
    workorders.expect_state("WO-10", "APPR")


@pytest.mark.critical
def test_completed_order_can_close(workorders):
    """
    TC-TRI-019
    REQ-TRI-009
    State Transition Testing
    """
    workorders.transition("WO-07", "CLOSE")
    workorders.expect_state("WO-07", "CLOSE")


@pytest.mark.critical
def test_in_progress_order_cannot_close(workorders):
    """
    TC-TRI-020
    REQ-TRI-009
    Negative Testing
    """
    workorders.transition("WO-05", "CLOSE")
    workorders.expect_error("INPRG -> CLOSE")
    workorders.expect_state("WO-05", "INPRG")


@pytest.mark.critical
def test_closed_order_stays_closed(workorders, defects):
    """
    TC-TRI-021
    REQ-TRI-009
    Decision Table Testing
    """
    defects.disable("reopen_closed")
    workorders.open()
    workorders.transition("WO-08", "INPRG")
    workorders.expect_error("CLOSE -> INPRG")
    workorders.expect_state("WO-08", "CLOSE")


@pytest.mark.critical
def test_rework_with_a_reason_returns_to_in_progress(workorders):
    """
    TC-TRI-022
    REQ-TRI-010
    State Transition Testing
    """
    workorders.transition("WO-07", "INPRG", reason="Rail still moves")
    workorders.expect_state("WO-07", "INPRG")


@pytest.mark.critical
def test_rework_without_a_reason_is_rejected(workorders):
    """
    TC-TRI-023
    REQ-TRI-010
    Negative Testing
    """
    workorders.transition("WO-07", "INPRG", reason="")
    workorders.expect_error("Rework requires a reason")
    workorders.expect_state("WO-07", "COMP")
