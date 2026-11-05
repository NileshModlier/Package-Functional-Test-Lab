# REQ-TRI-009 Closure

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an IBM TRIRIGA or Maximo system and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-TRI-009 |
| Title | Close accepted work and lock the task |
| Workflow | TRIRIGA / Maximo-style work |
| Topic | Closure |

## Description

An approver closes a physically complete task. The task becomes read-only, the parent request closes, and a requestor notification is recorded.

## Business Rule

Maximo's public status page says `CLOSE` finalizes the work order, removes inventory reservations for items that were not used, and makes the work order a history record. From `COMP`, the published successor on a standard work order is `CLOSE`.

The TRIRIGA guide says that when the reviewer accepts the performed work, the task is closed and the requestor is notified for corrective maintenance. When surveys are enabled for the request class, a survey follows completion. The Work Task app description says closed tasks are read-only.

The lab records the reservation release and the notification. It does not move stock and does not send mail.

## Source Link

- IBM Maximo, "Work order statuses": https://www.ibm.com/docs/en/maximo-manage/cd?topic=orders-work-order-statuses
- IBM TRIRIGA, *Maintenance and Service Management*, approval of completed work and requestor notification: https://www.ibm.com/docs/en/SSFCZ3_11.6/pdf/pdf_tri_maint_service_mng.pdf

The Maximo page defines the close effects and allows `COMP` to change to `CLOSE`. The TRIRIGA guide says accepted work is closed and the corrective-maintenance requestor is notified, with a survey when the request class has one configured.

## Simulated Assumptions

- The actor has the approver role. The technician is not required to be a different person, except that closure is an approver action rather than the completion action in REQ-TRI-008.
- ASM-TRI-06. Closure sets `reservations_released` true. No inventory quantity changes.
- ASM-TRI-09. Closure writes one requestor notification record and sets the parent request to `CLOSE`. If the request class is marked survey-enabled, `survey_due` is true. The lab does not send email and does not open a survey form.
- After `CLOSE`, time and material writes are rejected.

## Acceptance Criteria

1. An approver closing a `COMP` task sets the task to `CLOSE`, stores `closed_at`, and sets `reservations_released`.
2. The parent request status becomes `CLOSE`, and one notification record exists for the requester.
3. When the request class is survey-enabled, the closed request has `survey_due` true. Otherwise `survey_due` is false.
4. A time or material write after `CLOSE` is rejected.
5. Close from any task status other than `COMP` is rejected, and no notification is written.
