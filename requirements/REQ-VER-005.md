# REQ-VER-005 Coaching session

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not a Verint tenant and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-VER-005 |
| Title | Move a coaching session through the published status path |
| Workflow | Verint-style quality |
| Topic | Coaching session |

## Description

A coach creates a session for an employee or a group and advances it through the public coaching statuses until it is completed.

## Business Rule

Public coaching help describes this path. A manager creates a session, or a session is created from a KPI alert. A date is set, or scheduling leaves the session Pending. After the meeting, the coach sets Coached, adds a meeting summary, and sets Await Employee Feedback. Feedback moves the session to Await Coach Follow Up when the individual employee has responded, or when every employee in a group has responded. A manager may set a group session to Completed before all feedback is in. The coach then grades the session and sets Completed. A later reviewer approval leaves the status at Completed.

## Source Link

- Verint help, "Recommended workflow: Create a coaching session": https://wfo.mon2.verintcloudservices.com/onlinehelp/en_us/coaching/CoachingUser/coach_ug_Workflow_create_session.htm
- Verint, "Employee Coaching for Workforce Optimization": https://www.verint.com/coaching-and-learning/

The help page is the status workflow summarized above. The product page describes coaching as scheduled, delivered, and tracked with quality scores. KPI-alert creation and workforce scheduling are recognized as public inputs that still start at Pending. The lab does not model a scheduling product (`plan/test-plan.md` section 5).

## Simulated Assumptions

- ASM-VER-07. Status values are Pending, Coached, Await Employee Feedback, Await Coach Follow Up, and Completed.
- A meeting summary is required before Await Employee Feedback.
- A grade is required before the coach moves Await Coach Follow Up to Completed.
- Early completion is allowed only for a group session and only by a manager.
- Linking the session to an evaluation is REQ-VER-008. This requirement allows a session with no evaluation link.

## Acceptance Criteria

1. Creating a session stores Pending, the employee or the group, and an optional date.
2. Pending moves to Coached only when the coach records that the meeting occurred. Coached moves to Await Employee Feedback only when a meeting summary is present.
3. An individual session moves from Await Employee Feedback to Await Coach Follow Up when that employee submits feedback, and not before.
4. A group session stays in Await Employee Feedback until every member has responded, unless a manager sets it to Completed early.
5. Await Coach Follow Up moves to Completed only when a grade is present. A reviewer approval after that leaves the status Completed.
