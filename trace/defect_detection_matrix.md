# Defect detection matrix

**Milestone:** M4
**Identifier:** SIMULATED
**Runner:** Playwright + pytest, Chromium

Each row asserts the M1 rule. The default suite turns that switch OFF through the defects page, then checks the correct outcome. `pytest tests/ui` passed 26 tests with the switches OFF.

The same six tests were run again with `SIM_FORCE_DEFECTS=on`. That setting skips the toggle, so the seed stays ON. All six failed on the correct-behavior assertion.

| Defect | Requirement | Automated test | Switch OFF | Switch ON |
| --- | --- | --- | --- | --- |
| pass_mark | REQ-INT-004 | [AUTO-INT-008](../tests/ui/test_learning.py) · TC-INT-008 | ENR-01 score 80.00 is Passed | State was Failed |
| certificate_date | REQ-INT-007 | [AUTO-INT-016](../tests/ui/test_learning.py) · TC-INT-016 | Issued date equals completion date 2026-11-05 | Issued date was 2026-11-04 |
| quality_score | REQ-VER-003 | [AUTO-VER-005](../tests/ui/test_quality.py) · TC-VER-005 | Sections A1/2 B1/1 C1/1 score 70.0, Below standard | Score was 83.33, Meets standard |
| inactive_assignment | REQ-TRI-004 | [AUTO-TRI-008](../tests/ui/test_workorders.py) · TC-TRI-008 | TEC-02 on WO-03 is rejected and stays unassigned | No error; WO-03 showed Technician TEC-02 |
| invalid_completion | REQ-TRI-008 | [AUTO-TRI-017](../tests/ui/test_workorders.py) · TC-TRI-017 | WO-10 APPR to COMP is rejected | No error; the illegal move was accepted |
| reopen_closed | REQ-TRI-009 | [AUTO-TRI-021](../tests/ui/test_workorders.py) · TC-TRI-021 | WO-08 CLOSE to INPRG is rejected | No error; WO-08 showed INPRG |

The other 20 UI tests do not depend on a planted switch. They passed in the default run.
