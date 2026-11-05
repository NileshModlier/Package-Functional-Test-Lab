# REQ-INT-006 Completion

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an Intellum configuration and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-INT-006 |
| Title | Record completion on the enrollment when criteria are met |
| Workflow | Intellum-style learning |
| Topic | Completion |

## Description

The lab sets the enrollment to `Completed` and stores one completion time when the activity's completion criteria are met.

## Business Rule

Public documentation separates being enrolled from completing, and separates assessment passed from certification earned. The certification article says a credential is produced when completion criteria are met, and that enrollment status is the record those decisions use.

## Source Link

- Intellum, "How to Administer a Certification Program at Scale": https://www.intellum.com/resources/blog/how-to-administer-a-certification-program-at-scale-in-intellum
- Intellum data connector: https://www.intellum.com/integrations/data-connector

The data-connector page lists enrolled, completed, assessment passed, and certification earned as distinct facts. The certification article ties issuance to completion criteria and ties the outcome to enrollment status.

## Simulated Assumptions

- ASM-INT-08. For the sample certification activity, status `Passed` plus all required modules complete is the completion rule. The enrollment then becomes `Completed`.
- ASM-INT-05. A content-only activity with no assessment completes when every required module is viewed.
- Completion time is set once. A repeated completion event does not move that timestamp.
- `Failed` is not `Completed`.

## Acceptance Criteria

1. An enrollment in `Passed`, with every required module complete, becomes `Completed` and stores one completion timestamp.
2. A second completion signal does not change that timestamp and does not create a second completion record.
3. An enrollment in `Failed` remains not completed and has an empty completion timestamp.
4. An enrollment that is only `Enrolled` or `In progress` has an empty completion timestamp.
5. A content-only activity becomes `Completed` when its required modules are viewed, without an assessment score.
