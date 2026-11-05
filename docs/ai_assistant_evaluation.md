# AI assistant evaluation

**Milestone:** M7
**Identifier:** SIMULATED
**Run:** nine requirements, local, 2026-11-05

Requirements: REQ-INT-003, REQ-INT-006, REQ-INT-007, REQ-INT-008, REQ-TRI-002, REQ-TRI-005, REQ-TRI-006, REQ-VER-001, REQ-VER-006.

REQ-INT-006 and REQ-INT-007 already cite every acceptance criterion, so they produced no draft. The other seven produced the files below. One duplicate and one invalid contrast draft were counted and not written.

| Measure | Count |
| --- | --- |
| Proposal Count | 14 |
| Accepted Count | 8 |
| Rejected Count | 4 |
| Duplicate Count | 1 |
| Invalid Count | 1 |
| Acceptance Rate | 0.57 |

Acceptance rate is accepted divided by proposals generated (8 / 14). Among the 12 drafts a person reviewed, 8 were accepted (0.67).

## Accepted cases

| Case | Proposal | Requirement | Criterion |
| --- | --- | --- | --- |
| TC-INT-022 | REQ-INT-003-01 | REQ-INT-003 | AC-2 unanswered questions score 0 |
| TC-INT-023 | REQ-INT-003-02 | REQ-INT-003 | AC-4 attendance or launch with no answers |
| TC-TRI-024 | REQ-TRI-002-02 | REQ-TRI-002 | AC-4 rejection without a reason stays WAPPR |
| TC-TRI-025 | REQ-TRI-005-01 | REQ-TRI-005 | AC-2 supervisor may start |
| TC-TRI-026 | REQ-TRI-006-01 | REQ-TRI-006 | AC-4 coworker time line is read-only |
| TC-VER-017 | REQ-VER-001-01 | REQ-VER-001 | AC-4 second in-progress evaluation |
| TC-VER-018 | REQ-VER-006-01 | REQ-VER-006 | AC-2 second acknowledgement keeps the original time |
| TC-VER-019 | REQ-VER-006-02 | REQ-VER-006 | AC-5 acknowledgement by someone else |

Each file has `source: ai-draft`, `reviewed_by: Lab reviewer`, `status: Accepted`, and `automation_intent: not-executable`.

## Rejected drafts

| Proposal | Reason |
| --- | --- |
| REQ-TRI-002-01 | Existing cases already record that CAN is not a simulator state. |
| REQ-INT-008-01 | TC-INT-018 already records that read-only scope is not implemented. |
| REQ-INT-008-02 | TC-INT-018 already records that PATCH of a note is not implemented. |
| REQ-TRI-005-02 | TC-TRI-009 already records that started_at is not stored. |

## Example accepted proposal

TC-INT-022, from REQ-INT-003-01. Technique: exploratory. The step and expected result are the AC-2 sentence: unanswered questions contribute 0 points and still count in the possible points. No earlier case cites REQ-INT-003 AC-2. Reviewer: Lab reviewer.

## Example rejected proposal

REQ-TRI-002-01 proposed that rejecting a WAPPR request with a reason sets status CAN. The sentence is in REQ-TRI-002, so terminology validation allowed it. Review rejected it because TC-TRI-004 already says rejecting a request to CAN is not a simulator state. The rejection reason is stored on `proposals/rejected/REQ-TRI-002-01.yaml`.

## Contrast checks

The duplicate was a restatement of the first REQ-INT-003 case title. The invalid draft introduced `biometric_signature`, which is not in that requirement or its cases. Neither file was written.
