# REQ-TRI-008 Completion

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an IBM TRIRIGA or Maximo system and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-TRI-008 |
| Title | Submit in-progress work as physically complete |
| Workflow | TRIRIGA / Maximo-style work |
| Topic | Completion |

## Description

The technician submits an in-progress task as physically complete. The task remains editable for actuals until an approver closes it. The requestor is not notified at this step.

## Business Rule

Maximo's public status page says `COMP` means the physical work is finished, and lists `COMP` as a change from `INPRG`. The TRIRIGA guide says that after the work is performed it is submitted for review, and that a completed task which is not yet closed can still be edited. Notification of the requestor follows approval of the work, which is REQ-TRI-009 in this lab.

The public Maximo table allows `COMP` from several earlier statuses, including a direct jump that skips in-progress work. ASM-TRI-07 narrows the lab so completion is submitted from `INPRG` only. That narrowing is simulated scope, not a claim that Maximo forbids the other jumps.

## Source Link

- IBM Maximo, "Work order statuses": https://www.ibm.com/docs/en/maximo-manage/cd?topic=orders-work-order-statuses
- IBM TRIRIGA, *Maintenance and Service Management*, completing the task and the Work Task app: https://www.ibm.com/docs/en/SSFCZ3_11.6/pdf/pdf_tri_maint_service_mng.pdf

The Maximo page defines `COMP` and allows it from `INPRG`. The TRIRIGA guide says completed work is submitted for review and can still be edited before it is closed. The Arizona customer manual is only a secondary illustration of "submit for review" and is not the oracle for this requirement: https://gao.az.gov/sites/default/files/2022-05/TRIRIGA%20Facilities%20Management%20-%20Service%20Tech%20V2_0.pdf

## Simulated Assumptions

- ASM-TRI-07. Only `INPRG` may move to `COMP` in this lab.
- Completion stores `completed_at`. It does not set `closed_at` and does not write the requestor notification.
- Time and material entry remain allowed (REQ-TRI-006, REQ-TRI-007).

## Acceptance Criteria

1. The assigned resource submitting an `INPRG` task sets status `COMP` and stores `completed_at`.
2. A time line and a material line can still be added while the task is `COMP`.
3. Submit-completion from `APPR`, `WMATL`, or `WAPPR` is rejected, and the status is unchanged.
4. Completion does not write a requestor notification and does not close the parent request.
5. A second completion signal does not change `completed_at`.
