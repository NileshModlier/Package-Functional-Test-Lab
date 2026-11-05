# Traceability matrix

**Milestone:** M3 design, M4 automation IDs
**Identifier:** SIMULATED
**Status:** 26 cases have a Playwright automation ID. CI result cells are still empty.

The system under test is Package Sim. Automation IDs point at `tests/ui/`. CI is not wired.

Chain: Requirement → Test case → Automation → CI result.

`later-api` and `later-api-with-defect-switch` stay in the intent column. An automation ID is a separate node. See `defect_detection_matrix.md` for the six planted switches.

| Requirement | Risk | Test case | Technique | Priority | Automation intent | Automation ID | CI result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-INT-001 | Medium | [TC-INT-001](../cases/TC-INT-001.yaml) | Equivalence Partitioning | Medium | later-api | AUTO-INT-001 |  |
| REQ-INT-001 | Medium | [TC-INT-002](../cases/TC-INT-002.yaml) | Negative Testing | Medium | later-api | AUTO-INT-002 |  |
| REQ-INT-001 | Medium | [TC-INT-003](../cases/TC-INT-003.yaml) | Negative Testing | Medium | later-api |  |  |
| REQ-INT-002 | Medium | [TC-INT-004](../cases/TC-INT-004.yaml) | State Transition Testing | Medium | later-api | AUTO-INT-004 |  |
| REQ-INT-002 | Medium | [TC-INT-005](../cases/TC-INT-005.yaml) | Negative Testing | Medium | later-api |  |  |
| REQ-INT-003 | Medium | [TC-INT-006](../cases/TC-INT-006.yaml) | Equivalence Partitioning | Medium | later-api-with-defect-switch |  |  |
| REQ-INT-003 | Medium | [TC-INT-007](../cases/TC-INT-007.yaml) | Boundary Value Analysis | Medium | later-api-with-defect-switch |  |  |
| REQ-INT-004 | High | [TC-INT-008](../cases/TC-INT-008.yaml) | Boundary Value Analysis | High | later-api-with-defect-switch | AUTO-INT-008 |  |
| REQ-INT-004 | High | [TC-INT-009](../cases/TC-INT-009.yaml) | Boundary Value Analysis | High | later-api | AUTO-INT-009 |  |
| REQ-INT-004 | High | [TC-INT-010](../cases/TC-INT-010.yaml) | Boundary Value Analysis | High | later-api | AUTO-INT-010 |  |
| REQ-INT-004 | High | [TC-INT-011](../cases/TC-INT-011.yaml) | Decision Table Testing | High | later-api-with-defect-switch |  |  |
| REQ-INT-005 | High | [TC-INT-010](../cases/TC-INT-010.yaml) | Boundary Value Analysis | High | later-api | AUTO-INT-010 |  |
| REQ-INT-005 | High | [TC-INT-012](../cases/TC-INT-012.yaml) | State Transition Testing | High | later-api |  |  |
| REQ-INT-005 | High | [TC-INT-013](../cases/TC-INT-013.yaml) | Negative Testing | High | later-api |  |  |
| REQ-INT-005 | High | [TC-INT-021](../cases/TC-INT-021.yaml) | Exploratory Testing | High | manual-exploratory |  |  |
| REQ-INT-006 | High | [TC-INT-014](../cases/TC-INT-014.yaml) | State Transition Testing | High | later-api-with-defect-switch | AUTO-INT-014 |  |
| REQ-INT-006 | High | [TC-INT-015](../cases/TC-INT-015.yaml) | Negative Testing | High | later-api |  |  |
| REQ-INT-006 | High | [TC-INT-021](../cases/TC-INT-021.yaml) | Exploratory Testing | High | manual-exploratory |  |  |
| REQ-INT-007 | High | [TC-INT-016](../cases/TC-INT-016.yaml) | Decision Table Testing | High | later-api-with-defect-switch | AUTO-INT-016 |  |
| REQ-INT-007 | High | [TC-INT-017](../cases/TC-INT-017.yaml) | Negative Testing | High | later-api-with-defect-switch |  |  |
| REQ-INT-007 | High | [TC-INT-021](../cases/TC-INT-021.yaml) | Exploratory Testing | High | manual-exploratory |  |  |
| REQ-INT-008 | Medium | [TC-INT-018](../cases/TC-INT-018.yaml) | Equivalence Partitioning | Medium | later-api |  |  |
| REQ-INT-009 | Medium | [TC-INT-019](../cases/TC-INT-019.yaml) | Equivalence Partitioning | Medium | later-api |  |  |
| REQ-INT-009 | Medium | [TC-INT-020](../cases/TC-INT-020.yaml) | Negative Testing | Medium | later-api |  |  |
| REQ-VER-001 | Medium | [TC-VER-001](../cases/TC-VER-001.yaml) | Equivalence Partitioning | Medium | later-api |  |  |
| REQ-VER-001 | Medium | [TC-VER-002](../cases/TC-VER-002.yaml) | Negative Testing | Medium | later-api |  |  |
| REQ-VER-002 | Medium | [TC-VER-003](../cases/TC-VER-003.yaml) | Negative Testing | Medium | later-api |  |  |
| REQ-VER-002 | Medium | [TC-VER-005](../cases/TC-VER-005.yaml) | Decision Table Testing | High | later-api-with-defect-switch | AUTO-VER-005 |  |
| REQ-VER-003 | High | [TC-VER-004](../cases/TC-VER-004.yaml) | Equivalence Partitioning | High | later-api-with-defect-switch | AUTO-VER-004 |  |
| REQ-VER-003 | High | [TC-VER-005](../cases/TC-VER-005.yaml) | Decision Table Testing | High | later-api-with-defect-switch | AUTO-VER-005 |  |
| REQ-VER-003 | High | [TC-VER-006](../cases/TC-VER-006.yaml) | Decision Table Testing | High | later-api-with-defect-switch |  |  |
| REQ-VER-004 | High | [TC-VER-007](../cases/TC-VER-007.yaml) | Boundary Value Analysis | High | later-api-with-defect-switch | AUTO-VER-007 |  |
| REQ-VER-004 | High | [TC-VER-008](../cases/TC-VER-008.yaml) | Boundary Value Analysis | High | later-api-with-defect-switch | AUTO-VER-008 |  |
| REQ-VER-005 | Medium | [TC-VER-014](../cases/TC-VER-014.yaml) | State Transition Testing | Medium | later-api |  |  |
| REQ-VER-006 | High | [TC-VER-009](../cases/TC-VER-009.yaml) | State Transition Testing | High | later-api | AUTO-VER-009 |  |
| REQ-VER-006 | High | [TC-VER-010](../cases/TC-VER-010.yaml) | Negative Testing | High | later-api | AUTO-VER-010 |  |
| REQ-VER-006 | High | [TC-VER-016](../cases/TC-VER-016.yaml) | Exploratory Testing | High | manual-exploratory |  |  |
| REQ-VER-007 | High | [TC-VER-011](../cases/TC-VER-011.yaml) | State Transition Testing | High | later-api | AUTO-VER-011 |  |
| REQ-VER-007 | High | [TC-VER-012](../cases/TC-VER-012.yaml) | Negative Testing | High | later-api |  |  |
| REQ-VER-007 | High | [TC-VER-013](../cases/TC-VER-013.yaml) | State Transition Testing | High | later-api |  |  |
| REQ-VER-007 | High | [TC-VER-016](../cases/TC-VER-016.yaml) | Exploratory Testing | High | manual-exploratory |  |  |
| REQ-VER-008 | Medium | [TC-VER-015](../cases/TC-VER-015.yaml) | Decision Table Testing | Medium | later-api | AUTO-VER-015 |  |
| REQ-VER-008 | Medium | [TC-VER-016](../cases/TC-VER-016.yaml) | Exploratory Testing | High | manual-exploratory |  |  |
| REQ-TRI-001 | Medium | [TC-TRI-001](../cases/TC-TRI-001.yaml) | Negative Testing | Medium | later-api |  |  |
| REQ-TRI-001 | Medium | [TC-TRI-002](../cases/TC-TRI-002.yaml) | State Transition Testing | Medium | later-api |  |  |
| REQ-TRI-002 | High | [TC-TRI-003](../cases/TC-TRI-003.yaml) | Negative Testing | High | later-api | AUTO-TRI-003 |  |
| REQ-TRI-002 | High | [TC-TRI-004](../cases/TC-TRI-004.yaml) | State Transition Testing | High | later-api | AUTO-TRI-004 |  |
| REQ-TRI-003 | High | [TC-TRI-005](../cases/TC-TRI-005.yaml) | Decision Table Testing | High | later-api |  |  |
| REQ-TRI-003 | High | [TC-TRI-006](../cases/TC-TRI-006.yaml) | Negative Testing | High | later-api |  |  |
| REQ-TRI-004 | Medium | [TC-TRI-007](../cases/TC-TRI-007.yaml) | State Transition Testing | Medium | later-api-with-defect-switch |  |  |
| REQ-TRI-004 | Medium | [TC-TRI-008](../cases/TC-TRI-008.yaml) | Decision Table Testing | Medium | later-api-with-defect-switch | AUTO-TRI-008 |  |
| REQ-TRI-005 | Medium | [TC-TRI-009](../cases/TC-TRI-009.yaml) | State Transition Testing | Medium | later-api |  |  |
| REQ-TRI-005 | Medium | [TC-TRI-010](../cases/TC-TRI-010.yaml) | Negative Testing | Medium | later-api |  |  |
| REQ-TRI-006 | Medium | [TC-TRI-011](../cases/TC-TRI-011.yaml) | Boundary Value Analysis | Medium | later-api |  |  |
| REQ-TRI-006 | Medium | [TC-TRI-012](../cases/TC-TRI-012.yaml) | Negative Testing | Medium | later-api |  |  |
| REQ-TRI-007 | Medium | [TC-TRI-013](../cases/TC-TRI-013.yaml) | Equivalence Partitioning | Medium | later-api |  |  |
| REQ-TRI-007 | Medium | [TC-TRI-014](../cases/TC-TRI-014.yaml) | Negative Testing | Medium | later-api |  |  |
| REQ-TRI-007 | Medium | [TC-TRI-015](../cases/TC-TRI-015.yaml) | State Transition Testing | Medium | later-api |  |  |
| REQ-TRI-008 | High | [TC-TRI-016](../cases/TC-TRI-016.yaml) | State Transition Testing | High | later-api-with-defect-switch | AUTO-TRI-016 |  |
| REQ-TRI-008 | High | [TC-TRI-017](../cases/TC-TRI-017.yaml) | Negative Testing | High | later-api-with-defect-switch | AUTO-TRI-017 |  |
| REQ-TRI-008 | High | [TC-TRI-018](../cases/TC-TRI-018.yaml) | Decision Table Testing | High | later-api-with-defect-switch |  |  |
| REQ-TRI-009 | High | [TC-TRI-019](../cases/TC-TRI-019.yaml) | State Transition Testing | High | later-api-with-defect-switch | AUTO-TRI-019 |  |
| REQ-TRI-009 | High | [TC-TRI-020](../cases/TC-TRI-020.yaml) | Negative Testing | High | later-api | AUTO-TRI-020 |  |
| REQ-TRI-009 | High | [TC-TRI-021](../cases/TC-TRI-021.yaml) | Decision Table Testing | High | later-api-with-defect-switch | AUTO-TRI-021 |  |
| REQ-TRI-010 | High | [TC-TRI-022](../cases/TC-TRI-022.yaml) | State Transition Testing | High | later-api | AUTO-TRI-022 |  |
| REQ-TRI-010 | High | [TC-TRI-023](../cases/TC-TRI-023.yaml) | Negative Testing | High | later-api | AUTO-TRI-023 |  |

## Coverage

- Requirements: 27
- Test cases: 60
- Requirements with at least one case: 27

| Technique | Cases |
| --- | --- |
| Equivalence Partitioning | 7 |
| Boundary Value Analysis | 7 |
| Decision Table Testing | 9 |
| State Transition Testing | 15 |
| Negative Testing | 20 |
| Exploratory Testing | 2 |

## High-risk depth

Each high-risk requirement has more than one case.

| Requirement | Cases |
| --- | --- |
| REQ-INT-004 | 4 |
| REQ-INT-005 | 4 |
| REQ-INT-006 | 3 |
| REQ-INT-007 | 3 |
| REQ-TRI-002 | 2 |
| REQ-TRI-003 | 2 |
| REQ-TRI-008 | 3 |
| REQ-TRI-009 | 3 |
| REQ-TRI-010 | 2 |
| REQ-VER-003 | 3 |
| REQ-VER-004 | 2 |
| REQ-VER-006 | 3 |
| REQ-VER-007 | 4 |

## Execution rule

Start each case with POST /test/reset unless the steps say a row already reset the seed.
A case that names a defect switch is observing either the M1 rule or the planted defect. Run it in the switch position the steps name.
known_sut_differences inside a case file is a simulator limit. It is not an expected pass for behavior the simulator does not implement.
