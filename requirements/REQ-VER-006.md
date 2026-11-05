# REQ-VER-006 Agent acknowledgement

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not a Verint tenant and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-VER-006 |
| Title | Let the evaluated agent acknowledge a scored evaluation |
| Workflow | Verint-style quality |
| Topic | Agent acknowledgement |

## Description

When acknowledgement is enabled, the evaluated agent records that they have received a scored evaluation. Acknowledgement is a receipt. It is not an edit of the score.

## Business Rule

Public form-management help says a form setting can allow an agent to acknowledge a scored evaluation, indicating that the agent received it. A related setting allows acknowledgement and appeal. Appeal in this lab is the dispute path in REQ-VER-007. Fill-out help separates acknowledgement-related review from the score itself: accepted, disputed, and resolved are review statuses, and the score is already calculated before review.

## Source Link

- Verint help, "Manage evaluation forms": https://www.wfohelp.com/doc/Content/user-guides/application-management/evaluation-form-manager.htm
- Verint help, "Form fill-out area": https://wfo.mon2.verintcloudservices.com/onlinehelp/en_us/QM/Fillout.htm

The form-manager page says agents can indicate that they have received their evaluations when acknowledgement is allowed, and can ask for a rescore when appeal is allowed. Fill-out help lists the review statuses and keeps them distinct from the in-progress state.

## Simulated Assumptions

- ASM-VER-04. The sample form allows acknowledgement. The first acknowledgement stores the agent and the time. A repeat acknowledgement does not change that time.
- Acknowledgement does not change the total, the threshold classification, or the evaluation status.
- The agent can acknowledge an evaluation in `Evaluation submitted`, `Accepted`, or `Resolved`. The agent cannot acknowledge `Evaluation in progress`.
- The actor must be the evaluated employee.

## Acceptance Criteria

1. The evaluated employee acknowledging a submitted scored evaluation sets acknowledged and stores the employee and the acknowledgement time.
2. A second acknowledgement by the same employee leaves the original time in place.
3. The total score and the status after acknowledgement equal the total score and the status before acknowledgement.
4. An acknowledgement attempt on an evaluation in `Evaluation in progress` is rejected.
5. An acknowledgement attempt by anyone other than the evaluated employee is rejected.
