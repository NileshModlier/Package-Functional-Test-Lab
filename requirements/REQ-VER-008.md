# REQ-VER-008 Coaching linked to an evaluation

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not a Verint tenant and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-VER-008 |
| Title | Link a coaching session to an evaluation without changing the score |
| Workflow | Verint-style quality |
| Topic | Coaching session |

## Description

A supervisor can attach a coaching session to an evaluation so the session has the quality result in context. The attachment does not rescore the evaluation.

## Business Rule

The public quality datasheet says coaching sessions can carry the interaction and the quality context, and that quality scores, scorecards, and coaching are used together. The coaching product page says the coaching workflow is integrated with evaluation scores and KPIs. The public dispute article treats the coaching conversation as a place to agree the evaluation, while the recorded score changes only when someone updates the evaluation itself.

## Source Link

- Verint Quality datasheet: https://www.verint.com/wp-content/uploads/quality-management-datasheet.pdf
- Verint, "Employee Coaching for Workforce Optimization": https://www.verint.com/coaching-and-learning/
- Verint help, "Recommended workflow: Create a coaching session": https://wfo.mon2.verintcloudservices.com/onlinehelp/en_us/coaching/CoachingUser/coach_ug_Workflow_create_session.htm

The datasheet says interactions and KPI or quality context can be attached to a coaching session. The coaching page ties the session workflow to evaluation scores. The status workflow remains REQ-VER-005.

## Simulated Assumptions

- ASM-VER-06. The link stores the evaluation identifier on the session. Completing the session does not change the evaluation total, classification, or status.
- A `Below standard` evaluation may be linked. A `Meets standard` evaluation may also be linked. The lab does not require coaching for either class.
- The linked evaluation must already be scored. An in-progress evaluation cannot be linked.

## Acceptance Criteria

1. Creating a coaching session with an evaluation identifier stores that identifier on the session and leaves the evaluation total unchanged.
2. Moving the linked session to Completed (REQ-VER-005) leaves the evaluation total, classification, and status unchanged.
3. Linking an evaluation that is still `Evaluation in progress` is rejected, and no session is created by that attempt.
4. A session may exist without an evaluation link (REQ-VER-005). Adding a link later stores the identifier and still does not change the score.
5. The evaluation record does not gain a second total because a coaching session was opened.
