# REQ-VER-001 Interaction evaluation

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not a Verint tenant and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-VER-001 |
| Title | Start an evaluation of a recorded employee interaction |
| Workflow | Verint-style quality |
| Topic | Interaction evaluation |

## Description

An evaluator starts a manual evaluation of one recorded interaction from the employee's perspective. The new evaluation is in progress and is linked to that interaction and employee.

## Business Rule

Public evaluation help says that once an interaction is recorded, a reviewer can evaluate the employee's handling of it. The same help distinguishes an evaluation (employee perspective) from an assessment (customer perspective). Questions on the form show whether they are complete, incomplete, or mandatory. Those question rules are REQ-VER-002. This requirement covers creating the evaluation.

## Source Link

- Verint help, "Perform an evaluation/assessment": https://wfo.mon2.verintcloudservices.com/onlinehelp/en_us/QM/QM/Perform_an_evaluation_assessment.htm
- Verint Quality datasheet: https://www.verint.com/wp-content/uploads/quality-management-datasheet.pdf

The help page says an evaluation reviews the employee on a recorded interaction and is distinct from a customer assessment. The datasheet describes forms used to measure quality criteria. Customer assessments and analytics are outside this lab (`ASM-VER-01`).

## Simulated Assumptions

- ASM-VER-01. The lab creates a manual employee evaluation only. One evaluator evaluates one interaction for one employee.
- The interaction must already exist. Starting an evaluation does not record audio or screen.
- The initial status is `Evaluation in progress`. The score is empty until submit (REQ-VER-003).

## Acceptance Criteria

1. Starting an evaluation on an existing interaction creates one evaluation linked to the interaction, the employee, the evaluator, and the selected form, with status `Evaluation in progress`.
2. The new evaluation has no total score and is not acknowledged.
3. Starting an evaluation without an interaction is rejected and creates nothing.
4. A second in-progress evaluation of the same interaction by the same evaluator and form is rejected.
5. Creating the evaluation does not create a coaching session.
