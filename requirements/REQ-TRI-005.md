# REQ-TRI-005 Work in progress

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an IBM TRIRIGA or Maximo system and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-TRI-005 |
| Title | Start assigned work and record in-progress status |
| Workflow | TRIRIGA / Maximo-style work |
| Topic | Work in progress |

## Description

The assigned technician starts the task. The lab records `INPRG` and a start time. Unassigned work cannot start.

## Business Rule

Maximo's public status page says `INPRG` means the physical work is in progress, and lists `INPRG` as an allowed change from `APPR`. The TRIRIGA fulfillment description says the technician accepts the task and performs it. Performing the work is distinct from creating or assigning it.

The public Maximo table also allows other entries to `INPRG`. The lab's simulated path starts work only from assigned `APPR`, or resumes from `WMATL` (REQ-TRI-007).

## Source Link

- IBM Maximo, "Work order statuses": https://www.ibm.com/docs/en/maximo-manage/cd?topic=orders-work-order-statuses
- IBM TRIRIGA, *Maintenance and Service Management*, service fulfillment and the Work Task app: https://www.ibm.com/docs/en/SSFCZ3_11.6/pdf/pdf_tri_maint_service_mng.pdf

The Maximo page defines `INPRG` and allows `APPR` to change to `INPRG`. The TRIRIGA guide describes accepting the task and performing it, including in-progress tasks in the Work Task app.

## Simulated Assumptions

- ASM-TRI-07. Start is allowed from `APPR` only when a resource is set. The actor is that resource or a supervisor.
- Start stores `started_at` once. A second start signal does not move `started_at`.
- Direct moves from `WAPPR` or from an unassigned task into `INPRG` are rejected in this lab, including where the broader Maximo table lists more successors. The workflow document records that narrowing.

## Acceptance Criteria

1. The assigned resource starting an `APPR` task sets status `INPRG` and stores `started_at`.
2. A supervisor may start the task for the assigned resource, with the same result.
3. Starting an `APPR` task with no resource is rejected, and the status stays `APPR`.
4. Starting a task that is already `INPRG` leaves `started_at` unchanged.
5. A person who is neither the assigned resource nor a supervisor cannot start the task, and the status stays `APPR`.
