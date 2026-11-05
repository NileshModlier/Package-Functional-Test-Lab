# API traceability

**Milestone:** M5
**Identifier:** SIMULATED
**Status:** Defect-off Newman run passed. CI is not wired.

Chain: Requirement → Test case → Postman request → Newman execution.

CI is not wired. A passing Newman execution means the local defect-off run in `reports/api.json`.

| Requirement | Test Case | Postman Request | Newman Execution |
| --- | --- | --- | --- |
| REQ-INT-009 | TC-INT-019 | Package Sim Learning / TC-INT-019 Read learners | Pass |
| REQ-INT-001 | TC-INT-001 | Package Sim Learning / TC-INT-001 Enroll an available activity | Pass |
| REQ-INT-001 | TC-INT-002 | Package Sim Learning / TC-INT-002 Reject a duplicate enrollment | Pass |
| REQ-INT-002 | TC-INT-004 | Package Sim Learning / TC-INT-004 Start the enrollment | Pass |
| REQ-INT-004 | TC-INT-009 | Package Sim Learning / TC-INT-009 Pass at 80.01 | Pass |
| REQ-INT-009 | TC-INT-019 | Package Sim Learning / TC-INT-019 Read the passed enrollment | Pass |
| REQ-INT-006 | TC-INT-014 | Package Sim Learning / TC-INT-014 Complete the passed enrollment | Pass |
| REQ-INT-007 | TC-INT-016 | Package Sim Learning / TC-INT-014 Complete the passed enrollment | Pass |
| REQ-INT-007 | TC-INT-016 | Package Sim Learning / TC-INT-016 Read the certificate dates | Pass |
| REQ-INT-006 | TC-INT-014 | Package Sim Learning / TC-INT-014 Reject a second completion | Pass |
| REQ-INT-004 | TC-INT-010 | Package Sim Learning / TC-INT-010 Fail at 79.99 | Pass |
| REQ-INT-005 | TC-INT-010 | Package Sim Learning / TC-INT-010 Fail at 79.99 | Pass |
| REQ-INT-004 | TC-INT-008 | Package Sim Learning / TC-INT-008 Enroll for the 80.00 threshold | Pass |
| REQ-INT-004 | TC-INT-008 | Package Sim Learning / TC-INT-008 Start the threshold enrollment | Pass |
| REQ-INT-004 | TC-INT-008 | Package Sim Learning / TC-INT-008 Pass at 80.00 | Pass |
| REQ-INT-001 | TC-INT-003 | Package Sim Learning / TC-INT-003 Reject an unpublished activity | Pass |
| REQ-INT-002 | TC-INT-005 | Package Sim Learning / TC-INT-005 Enroll before an early assessment | Pass |
| REQ-INT-002 | TC-INT-005 | Package Sim Learning / TC-INT-005 Reject an assessment before start | Pass |
| REQ-INT-006 | TC-INT-015 | Package Sim Learning / TC-INT-015 Reject completion of a failed enrollment | Pass |
| REQ-INT-009 | TC-INT-020 | Package Sim Learning / TC-INT-020 Reject an unknown enrollment | Pass |
| REQ-INT-003 | TC-INT-007 | Package Sim Learning / TC-INT-007 Enroll a boundary learner | Pass |
| REQ-INT-003 | TC-INT-007 | Package Sim Learning / TC-INT-007 Start the boundary enrollment | Pass |
| REQ-INT-003 | TC-INT-007 | Package Sim Learning / TC-INT-007 Assess the boundary score | Pass |
| REQ-INT-004 | TC-INT-008 | Package Sim Learning / TC-INT-007 Assess the boundary score | Pass |
| REQ-INT-004 | TC-INT-009 | Package Sim Learning / TC-INT-007 Assess the boundary score | Pass |
| REQ-INT-004 | TC-INT-010 | Package Sim Learning / TC-INT-007 Assess the boundary score | Pass |
| Setup | Learning health | Package Sim Learning / Health | Pass |
| Setup | Learning reset | Package Sim Learning / Reset seed | Pass |
| REQ-INT-004 | Disable pass_mark | Package Sim Learning / Disable pass_mark | Pass |
| REQ-INT-007 | Disable certificate_date | Package Sim Learning / Disable certificate_date | Pass |
| REQ-VER-001 | TC-VER-001 | Package Sim Quality / TC-VER-001 Read interactions | Pass |
| REQ-VER-001 | TC-VER-001 | Package Sim Quality / TC-VER-001 Create an evaluation | Pass |
| REQ-VER-001 | TC-VER-002 | Package Sim Quality / TC-VER-002 Reject an unknown interaction | Pass |
| REQ-VER-002 | TC-VER-003 | Package Sim Quality / TC-VER-003 Create an evaluation for a partial submit | Pass |
| REQ-VER-002 | TC-VER-003 | Package Sim Quality / TC-VER-003 Reject a submit that omits a section | Pass |
| REQ-VER-003 | TC-VER-004 | Package Sim Quality / TC-VER-004 Create an all-yes evaluation | Pass |
| REQ-VER-003 | TC-VER-004 | Package Sim Quality / TC-VER-004 Score all yes as 100 | Pass |
| REQ-VER-003 | TC-VER-004 | Package Sim Quality / TC-VER-004 Create an all-no evaluation | Pass |
| REQ-VER-003 | TC-VER-004 | Package Sim Quality / TC-VER-004 Score all no as 0 | Pass |
| REQ-VER-003 | TC-VER-005 | Package Sim Quality / TC-VER-005 Score weighted sections as 70 | Pass |
| REQ-VER-002 | TC-VER-005 | Package Sim Quality / TC-VER-005 Score weighted sections as 70 | Pass |
| REQ-VER-006 | TC-VER-009 | Package Sim Quality / TC-VER-009 Acknowledge a scored evaluation | Pass |
| REQ-VER-006 | TC-VER-010 | Package Sim Quality / TC-VER-010 Create a pending evaluation | Pass |
| REQ-VER-006 | TC-VER-010 | Package Sim Quality / TC-VER-010 Reject acknowledgement while pending | Pass |
| REQ-VER-007 | TC-VER-011 | Package Sim Quality / TC-VER-011 Create an evaluation to dispute | Pass |
| REQ-VER-007 | TC-VER-011 | Package Sim Quality / TC-VER-011 Submit the dispute evaluation | Pass |
| REQ-VER-007 | TC-VER-011 | Package Sim Quality / TC-VER-011 Dispute with a comment | Pass |
| REQ-VER-007 | TC-VER-012 | Package Sim Quality / TC-VER-012 Create an evaluation for an empty dispute | Pass |
| REQ-VER-007 | TC-VER-012 | Package Sim Quality / TC-VER-012 Submit before the empty dispute | Pass |
| REQ-VER-007 | TC-VER-012 | Package Sim Quality / TC-VER-012 Reject a dispute without a comment | Pass |
| REQ-VER-007 | TC-VER-013 | Package Sim Quality / TC-VER-013 Resolve the dispute | Pass |
| REQ-VER-005 | TC-VER-014 | Package Sim Quality / TC-VER-014 Coach the resolved evaluation | Pass |
| REQ-VER-008 | TC-VER-015 | Package Sim Quality / TC-VER-014 Coach the resolved evaluation | Pass |
| REQ-VER-005 | TC-VER-014 | Package Sim Quality / TC-VER-014 Complete the coached evaluation | Pass |
| REQ-VER-008 | TC-VER-015 | Package Sim Quality / TC-VER-014 Complete the coached evaluation | Pass |
| REQ-VER-004 | TC-VER-007 | Package Sim Quality / TC-VER-007 Create a threshold evaluation | Pass |
| REQ-VER-004 | TC-VER-007 | Package Sim Quality / TC-VER-007 Submit the threshold sections | Pass |
| REQ-VER-004 | TC-VER-008 | Package Sim Quality / TC-VER-007 Submit the threshold sections | Pass |
| Setup | Quality health | Package Sim Quality / Health | Pass |
| Setup | Quality reset | Package Sim Quality / Reset seed | Pass |
| REQ-VER-003 | Disable quality_score | Package Sim Quality / Disable quality_score | Pass |
| REQ-TRI-001 | TC-TRI-001 | Package Sim Work Orders / TC-TRI-001 Reject a request missing a title | Pass |
| REQ-TRI-001 | TC-TRI-002 | Package Sim Work Orders / TC-TRI-002 Create a service request | Pass |
| REQ-TRI-001 | TC-TRI-002 | Package Sim Work Orders / TC-TRI-002 Submit the request | Pass |
| REQ-TRI-002 | TC-TRI-003 | Package Sim Work Orders / TC-TRI-003 Reject self-approval | Pass |
| REQ-TRI-002 | TC-TRI-004 | Package Sim Work Orders / TC-TRI-004 Approve as a different person | Pass |
| REQ-TRI-003 | TC-TRI-005 | Package Sim Work Orders / TC-TRI-005 Reject a repeated approval | Pass |
| REQ-TRI-003 | TC-TRI-005 | Package Sim Work Orders / TC-TRI-006 Read orders after approval | Pass |
| REQ-TRI-003 | TC-TRI-006 | Package Sim Work Orders / TC-TRI-006 Read orders after approval | Pass |
| REQ-TRI-005 | TC-TRI-010 | Package Sim Work Orders / TC-TRI-010 Reject start without a technician | Pass |
| REQ-TRI-004 | TC-TRI-008 | Package Sim Work Orders / TC-TRI-008 Reject an inactive technician | Pass |
| REQ-TRI-004 | TC-TRI-008 | Package Sim Work Orders / TC-TRI-008 Read WO-03 after the inactive assignment | Pass |
| REQ-TRI-004 | TC-TRI-007 | Package Sim Work Orders / TC-TRI-007 Assign an active technician | Pass |
| REQ-TRI-005 | TC-TRI-009 | Package Sim Work Orders / TC-TRI-009 Start assigned work | Pass |
| REQ-TRI-008 | TC-TRI-017 | Package Sim Work Orders / TC-TRI-017 Reject completion from WMATL | Pass |
| REQ-TRI-007 | TC-TRI-014 | Package Sim Work Orders / TC-TRI-014 Reject a zero material quantity | Pass |
| REQ-TRI-007 | TC-TRI-013 | Package Sim Work Orders / TC-TRI-013 Record a material quantity | Pass |
| REQ-TRI-007 | TC-TRI-015 | Package Sim Work Orders / TC-TRI-015 Resume after waiting for material | Pass |
| REQ-TRI-009 | TC-TRI-020 | Package Sim Work Orders / TC-TRI-020 Reject closure from INPRG | Pass |
| REQ-TRI-008 | TC-TRI-017 | Package Sim Work Orders / TC-TRI-017 Reject completion from APPR | Pass |
| REQ-TRI-008 | TC-TRI-016 | Package Sim Work Orders / TC-TRI-016 Complete in-progress work | Pass |
| REQ-TRI-009 | TC-TRI-019 | Package Sim Work Orders / TC-TRI-019 Close completed work | Pass |
| REQ-TRI-010 | TC-TRI-023 | Package Sim Work Orders / TC-TRI-023 Reject rework without a reason | Pass |
| REQ-TRI-010 | TC-TRI-022 | Package Sim Work Orders / TC-TRI-022 Rework completed work | Pass |
| REQ-TRI-006 | TC-TRI-012 | Package Sim Work Orders / TC-TRI-012 Reject time on a closed order | Pass |
| REQ-TRI-009 | TC-TRI-021 | Package Sim Work Orders / TC-TRI-021 Reject reopen of a closed order | Pass |
| REQ-TRI-006 | TC-TRI-011 | Package Sim Work Orders / TC-TRI-011 Record boundary hours | Pass |
| REQ-TRI-006 | TC-TRI-012 | Package Sim Work Orders / TC-TRI-011 Record boundary hours | Pass |
| Setup | Work order health | Package Sim Work Orders / Health | Pass |
| Setup | Work order reset | Package Sim Work Orders / Reset seed | Pass |
| REQ-TRI-004 | Disable inactive_assignment | Package Sim Work Orders / Disable inactive_assignment | Pass |
| REQ-TRI-008 | Disable invalid_completion | Package Sim Work Orders / Disable invalid_completion | Pass |
| REQ-TRI-009 | Disable reopen_closed | Package Sim Work Orders / Disable reopen_closed | Pass |
