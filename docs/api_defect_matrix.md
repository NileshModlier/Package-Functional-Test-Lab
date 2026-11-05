# API defect matrix

**Milestone:** M5
**Identifier:** SIMULATED
**Runner:** Newman against the three Postman collections

The defect-off run keeps `forceDefects` false. Each collection turns its switches OFF after reset, then asserts the M1 rule. That run is `reports/api.json`: 138 assertions, 0 failed.

The same three commands were repeated with `--env-var forceDefects=true`. The Disable requests are skipped, so the seed switches stay ON. Each collection exited 1.

| Defect | Requirement | Postman request | Switch OFF | Switch ON |
| --- | --- | --- | --- | --- |
| pass_mark | REQ-INT-004 | Package Sim Learning / TC-INT-008 Pass at 80.00 | State Passed, score 80.00 | State was Failed |
| pass_mark | REQ-INT-004 | Package Sim Learning / TC-INT-007 Assess the boundary score, row 80.00 | Passed | State was Failed |
| pass_mark | REQ-INT-003 | Package Sim Learning / TC-INT-007 Assess the boundary score, row 79.995 | Rounds to 80.00 and passes | State was Failed |
| certificate_date | REQ-INT-007 | Package Sim Learning / TC-INT-016 Read the certificate dates | Issued date equals completion date | Expected 2026-11-05 and received 2026-11-04 |
| quality_score | REQ-VER-003 | Package Sim Quality / TC-VER-005 Score weighted sections as 70 | Score 70, Below standard | Score was 83.33 |
| quality_score | REQ-VER-004 | Package Sim Quality / TC-VER-007 Submit the threshold sections | 79.99 below, 80.00 and 80.01 meet | Unweighted scores were 66.66, 66.67, and 66.68 |
| inactive_assignment | REQ-TRI-004 | Package Sim Work Orders / TC-TRI-008 Reject an inactive technician | HTTP 409, WO-03 stays unassigned | HTTP 200, technician was TEC-02 |
| invalid_completion | REQ-TRI-008 | Package Sim Work Orders / TC-TRI-017 Reject completion from APPR | HTTP 409 | HTTP 200 |
| reopen_closed | REQ-TRI-009 | Package Sim Work Orders / TC-TRI-021 Reject reopen of a closed order | HTTP 409 | HTTP 200 |

Rows that do not depend on a switch still passed in the defect-on run. Those include 79.99, 80.01, 79.994, duplicate enrollment, INPRG to CLOSE, and COMP to CLOSE.
