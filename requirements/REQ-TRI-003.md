# REQ-TRI-003 Task creation

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an IBM TRIRIGA or Maximo system and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-TRI-003 |
| Title | Create one work task when a request is approved |
| Workflow | TRIRIGA / Maximo-style work |
| Topic | Task creation |

## Description

Approval of the sample corrective request creates one work task from the service plan's task template. The task is linked to the request and starts approved, which means work is allowed once a resource is assigned.

## Business Rule

The public TRIRIGA guide says the service plan associated with the request class uses a task template to create the task when the request is processed. A request class has one service plan. Assignment of a person is a separate rule on that plan (REQ-TRI-004).

The public Maximo page says an approved work order (`APPR`) can begin. The lab creates the task already in `APPR` because the request approval is the approval gate. The task is not in progress until REQ-TRI-005.

## Source Link

- IBM TRIRIGA, *Maintenance and Service Management*, service plans and project or task creation: https://www.ibm.com/docs/en/SSFCZ3_11.6/pdf/pdf_tri_maint_service_mng.pdf
- IBM Maximo, "Work order statuses": https://www.ibm.com/docs/en/maximo-manage/cd?topic=orders-work-order-statuses

The TRIRIGA guide says task creation is based on the task template on the service plan, and that the request class points at one service plan. The Maximo page says `APPR` means the work can begin.

## Simulated Assumptions

- ASM-TRI-04. Service plan `SIM-PLAN-CORRECTIVE` creates exactly one task when the request first reaches `APPR`.
- The task stores the request identifier, the request class, the building, and status `APPR`.
- A canceled request (`CAN`) creates no task.
- Approving an already approved request does not create a second task.

## Acceptance Criteria

1. Moving a request from `WAPPR` to `APPR` creates one task linked to that request, with status `APPR` and no start time.
2. The task count for that request remains one if the approval action is repeated.
3. A request in `CAN` has zero tasks.
4. A request still in `WAPPR` or draft has zero tasks.
5. The created task's building and request class match the request.
