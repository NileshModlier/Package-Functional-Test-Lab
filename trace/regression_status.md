# Regression status

**Milestone:** M6
**Identifier:** SIMULATED
**Generated from:** `reports/ui.xml` and `reports/api.xml`

| Requirement | Test Case | Automation | Last Result |
| --- | --- | --- | --- |
| REQ-INT-001 | TC-INT-001 | AUTO-INT-001 (test_enroll_available_activity); Newman TC-INT-001 Enroll an available activity | Pass |
| REQ-INT-001 | TC-INT-002 | AUTO-INT-002 (test_duplicate_enrollment_is_rejected); Newman TC-INT-002 Reject a duplicate enrollment | Pass |
| REQ-INT-001 | TC-INT-003 | Newman TC-INT-003 Reject an unpublished activity | Pass |
| REQ-INT-002 | TC-INT-004 | AUTO-INT-004 (test_start_marks_content_modules_complete); Newman TC-INT-004 Start the enrollment | Pass |
| REQ-INT-002 | TC-INT-005 | Newman TC-INT-005 Enroll before an early assessment; Newman TC-INT-005 Reject an assessment before start | Pass |
| REQ-INT-003 | TC-INT-006 | — | Not run |
| REQ-INT-003 | TC-INT-007 | Newman TC-INT-007 Assess the boundary score; Newman TC-INT-007 Enroll a boundary learner; Newman TC-INT-007 Start the boundary enrollment | Pass |
| REQ-INT-004 | TC-INT-008 | AUTO-INT-008 (test_score_80_passes_when_pass_mark_defect_is_off); Newman TC-INT-008 Enroll for the 80.00 threshold; Newman TC-INT-008 Pass at 80.00; Newman TC-INT-008 Start the threshold enrollment | Pass |
| REQ-INT-004 | TC-INT-009 | AUTO-INT-009 (test_score_80_01_passes); Newman TC-INT-009 Pass at 80.01 | Pass |
| REQ-INT-004 | TC-INT-010 | AUTO-INT-010 (test_score_79_99_fails_without_a_certificate); Newman TC-INT-010 Fail at 79.99 | Pass |
| REQ-INT-005 | TC-INT-010 | AUTO-INT-010 (test_score_79_99_fails_without_a_certificate); Newman TC-INT-010 Fail at 79.99 | Pass |
| REQ-INT-004 | TC-INT-011 | — | Not run |
| REQ-INT-005 | TC-INT-012 | — | Not run |
| REQ-INT-005 | TC-INT-013 | — | Not run |
| REQ-INT-006 | TC-INT-014 | AUTO-INT-014 (test_passed_enrollment_completes_once); Newman TC-INT-014 Complete the passed enrollment; Newman TC-INT-014 Reject a second completion | Pass |
| REQ-INT-006 | TC-INT-015 | Newman TC-INT-015 Reject completion of a failed enrollment | Pass |
| REQ-INT-007 | TC-INT-016 | AUTO-INT-016 (test_certificate_issued_date_matches_completion); Newman TC-INT-016 Read the certificate dates | Pass |
| REQ-INT-007 | TC-INT-017 | — | Not run |
| REQ-INT-008 | TC-INT-018 | — | Not run |
| REQ-INT-009 | TC-INT-019 | Newman TC-INT-019 Read learners; Newman TC-INT-019 Read the passed enrollment | Pass |
| REQ-INT-009 | TC-INT-020 | Newman TC-INT-020 Reject an unknown enrollment | Pass |
| REQ-INT-005 | TC-INT-021 | — | Not run |
| REQ-INT-006 | TC-INT-021 | — | Not run |
| REQ-INT-007 | TC-INT-021 | — | Not run |
| REQ-TRI-001 | TC-TRI-001 | Newman TC-TRI-001 Reject a request missing a title | Pass |
| REQ-TRI-001 | TC-TRI-002 | Newman TC-TRI-002 Create a service request; Newman TC-TRI-002 Submit the request | Pass |
| REQ-TRI-002 | TC-TRI-003 | AUTO-TRI-003 (test_requester_cannot_approve_their_own_request); Newman TC-TRI-003 Reject self-approval | Pass |
| REQ-TRI-002 | TC-TRI-004 | AUTO-TRI-004 (test_different_person_can_approve); Newman TC-TRI-004 Approve as a different person | Pass |
| REQ-TRI-003 | TC-TRI-005 | Newman TC-TRI-005 Reject a repeated approval | Pass |
| REQ-TRI-003 | TC-TRI-006 | Newman TC-TRI-006 Read orders after approval | Pass |
| REQ-TRI-004 | TC-TRI-007 | Newman TC-TRI-007 Assign an active technician | Pass |
| REQ-TRI-004 | TC-TRI-008 | AUTO-TRI-008 (test_inactive_technician_is_rejected); Newman TC-TRI-008 Read WO-03 after the inactive assignment; Newman TC-TRI-008 Reject an inactive technician | Pass |
| REQ-TRI-005 | TC-TRI-009 | Newman TC-TRI-009 Start assigned work | Pass |
| REQ-TRI-005 | TC-TRI-010 | Newman TC-TRI-010 Reject start without a technician | Pass |
| REQ-TRI-006 | TC-TRI-011 | Newman TC-TRI-011 Record boundary hours | Pass |
| REQ-TRI-006 | TC-TRI-012 | Newman TC-TRI-012 Reject time on a closed order | Pass |
| REQ-TRI-007 | TC-TRI-013 | Newman TC-TRI-013 Record a material quantity | Pass |
| REQ-TRI-007 | TC-TRI-014 | Newman TC-TRI-014 Reject a zero material quantity | Pass |
| REQ-TRI-007 | TC-TRI-015 | Newman TC-TRI-015 Resume after waiting for material | Pass |
| REQ-TRI-008 | TC-TRI-016 | AUTO-TRI-016 (test_in_progress_work_can_be_completed); Newman TC-TRI-016 Complete in-progress work | Pass |
| REQ-TRI-008 | TC-TRI-017 | AUTO-TRI-017 (test_approved_order_cannot_complete); Newman TC-TRI-017 Reject completion from APPR; Newman TC-TRI-017 Reject completion from WMATL | Pass |
| REQ-TRI-008 | TC-TRI-018 | — | Not run |
| REQ-TRI-009 | TC-TRI-019 | AUTO-TRI-019 (test_completed_order_can_close); Newman TC-TRI-019 Close completed work | Pass |
| REQ-TRI-009 | TC-TRI-020 | AUTO-TRI-020 (test_in_progress_order_cannot_close); Newman TC-TRI-020 Reject closure from INPRG | Pass |
| REQ-TRI-009 | TC-TRI-021 | AUTO-TRI-021 (test_closed_order_stays_closed); Newman TC-TRI-021 Reject reopen of a closed order | Pass |
| REQ-TRI-010 | TC-TRI-022 | AUTO-TRI-022 (test_rework_with_a_reason_returns_to_in_progress); Newman TC-TRI-022 Rework completed work | Pass |
| REQ-TRI-010 | TC-TRI-023 | AUTO-TRI-023 (test_rework_without_a_reason_is_rejected); Newman TC-TRI-023 Reject rework without a reason | Pass |
| REQ-VER-001 | TC-VER-001 | Newman TC-VER-001 Create an evaluation; Newman TC-VER-001 Read interactions | Pass |
| REQ-VER-001 | TC-VER-002 | Newman TC-VER-002 Reject an unknown interaction | Pass |
| REQ-VER-002 | TC-VER-003 | Newman TC-VER-003 Create an evaluation for a partial submit; Newman TC-VER-003 Reject a submit that omits a section | Pass |
| REQ-VER-003 | TC-VER-004 | AUTO-VER-004 (test_all_yes_scores_100); Newman TC-VER-004 Create an all-no evaluation; Newman TC-VER-004 Create an all-yes evaluation; Newman TC-VER-004 Score all no as 0; Newman TC-VER-004 Score all yes as 100 | Pass |
| REQ-VER-002 | TC-VER-005 | AUTO-VER-005 (test_weighted_sections_score_70); Newman TC-VER-005 Score weighted sections as 70 | Pass |
| REQ-VER-003 | TC-VER-005 | AUTO-VER-005 (test_weighted_sections_score_70); Newman TC-VER-005 Score weighted sections as 70 | Pass |
| REQ-VER-003 | TC-VER-006 | — | Not run |
| REQ-VER-004 | TC-VER-007 | AUTO-VER-007 (test_threshold_79_99_is_below_and_80_meets); Newman TC-VER-007 Create a threshold evaluation; Newman TC-VER-007 Submit the threshold sections | Pass |
| REQ-VER-004 | TC-VER-008 | AUTO-VER-008 (test_threshold_80_01_meets_standard) | Pass |
| REQ-VER-006 | TC-VER-009 | AUTO-VER-009 (test_acknowledge_keeps_the_score); Newman TC-VER-009 Acknowledge a scored evaluation | Pass |
| REQ-VER-006 | TC-VER-010 | AUTO-VER-010 (test_pending_evaluation_has_no_acknowledge_action); Newman TC-VER-010 Create a pending evaluation; Newman TC-VER-010 Reject acknowledgement while pending | Pass |
| REQ-VER-007 | TC-VER-011 | AUTO-VER-011 (test_dispute_stores_the_comment_and_keeps_the_score); Newman TC-VER-011 Create an evaluation to dispute; Newman TC-VER-011 Dispute with a comment; Newman TC-VER-011 Submit the dispute evaluation | Pass |
| REQ-VER-007 | TC-VER-012 | Newman TC-VER-012 Create an evaluation for an empty dispute; Newman TC-VER-012 Reject a dispute without a comment; Newman TC-VER-012 Submit before the empty dispute | Pass |
| REQ-VER-007 | TC-VER-013 | Newman TC-VER-013 Resolve the dispute | Pass |
| REQ-VER-005 | TC-VER-014 | Newman TC-VER-014 Coach the resolved evaluation; Newman TC-VER-014 Complete the coached evaluation | Pass |
| REQ-VER-008 | TC-VER-015 | AUTO-VER-015 (test_coaching_does_not_change_the_score) | Pass |
| REQ-VER-006 | TC-VER-016 | — | Not run |
| REQ-VER-007 | TC-VER-016 | — | Not run |
| REQ-VER-008 | TC-VER-016 | — | Not run |
