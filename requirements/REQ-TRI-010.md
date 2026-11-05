# REQ-TRI-010 Rework after rejection

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an IBM TRIRIGA or Maximo system and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-TRI-010 |
| Title | Return unsatisfactory completed work for rework |
| Workflow | TRIRIGA / Maximo-style work |
| Topic | Completion |

## Description

An approver who finds completed work unsatisfactory sends the task back to in progress. Time and materials already recorded stay on the task. The technician can submit completion again.

## Business Rule

The public TRIRIGA service process says a reviewer who is not satisfied rejects the submitted work and returns it for rework. The assignee performs the additional work and submits it again. The public Arizona customer training manual illustrates the same reject-and-resubmit loop. It is a customer manual, not an IBM specification.

The public Maximo status table does **not** list a change from `COMP` back to `INPRG`. On that table, `COMP` changes to `CLOSE`. ASM-TRI-08 keeps the TRIRIGA rework loop and records the deviation from the Maximo table. Testers use ASM-TRI-08 as the oracle for this requirement. They do not "correct" the lab back to the Maximo table unless the assumption register is revised.

## Source Link

- IBM TRIRIGA, *Maintenance and Service Management*, review of submitted work: https://www.ibm.com/docs/en/SSFCZ3_11.6/pdf/pdf_tri_maint_service_mng.pdf
- IBM Maximo, "Work order statuses" (the table this lab deviates from): https://www.ibm.com/docs/en/maximo-manage/cd?topic=orders-work-order-statuses
- Secondary public customer manual, Arizona ADOA/GAO service-tech guide: https://gao.az.gov/sites/default/files/2022-05/TRIRIGA%20Facilities%20Management%20-%20Service%20Tech%20V2_0.pdf

The TRIRIGA guide is the primary source for returning unsatisfactory work. The Maximo page is cited so the deviation is checkable. The Arizona manual is a secondary illustration only.

## Simulated Assumptions

- ASM-TRI-08. Rejection from `COMP` requires a reason, sets status `INPRG`, clears `completed_at`, and keeps every time and material line.
- The parent request stays `APPR` during rework. It closes only under REQ-TRI-009.
- No requestor completion notification is written on rejection.
- After rework, REQ-TRI-008 can set `COMP` again, and that new completion stores a new `completed_at`.

## Acceptance Criteria

1. An approver rejecting a `COMP` task with a reason sets status `INPRG`, stores the reason, and clears `completed_at`.
2. Time lines and material lines that existed at rejection are still present and unchanged.
3. Rejection without a reason is rejected, and the task stays `COMP` with `completed_at` intact.
4. The parent request is not `CLOSE`, and no requestor completion notification is written.
5. After that return to `INPRG`, a new completion submit sets `COMP` and a new `completed_at`, and the earlier time lines remain.
