# REQ-TRI-004 Task assignment

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an IBM TRIRIGA or Maximo system and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-TRI-004 |
| Title | Assign a resource by plan rule or by accepting the task |
| Workflow | TRIRIGA / Maximo-style work |
| Topic | Task assignment |

## Description

The service plan either assigns the responsible person when the task is created, or leaves the task unassigned so a dispatcher or a technician can take it. Assignment does not by itself start the work.

## Business Rule

The public TRIRIGA guide lists assignment rules. Auto-Assign to Service Provider finds the responsible organization from the service assignment setup. Do not Assign leaves the task for another method, such as a dispatch manager. The Work Task app description says a technician can accept an unassigned task into their queue. Other public rules (task template, PM schedule organization, and service-plan defaults) are not simulated.

Maximo's public work-management material treats assignment as who will do approved work. Status stays approved until work is in progress.

## Source Link

- IBM TRIRIGA, *Maintenance and Service Management*, assignment rules and the Work Task app: https://www.ibm.com/docs/en/SSFCZ3_11.6/pdf/pdf_tri_maint_service_mng.pdf
- IBM Maximo, "Work order statuses": https://www.ibm.com/docs/en/maximo-manage/cd?topic=orders-work-order-statuses

The TRIRIGA guide's assignment-rule table defines Auto-Assign and Do not Assign, and the Work Task app section says a technician accepts an unassigned task. The Maximo page keeps `APPR` distinct from `INPRG`.

## Simulated Assumptions

- ASM-TRI-05. The lab implements Auto-Assign and Do not Assign only.
- Auto-Assign sets the resource to the single person configured on `SIM-PLAN-CORRECTIVE` at task creation. If that person is not configured, task creation under REQ-TRI-003 still succeeds and the task stays unassigned. That gap is visible rather than filled by a guessed name.
- A technician may accept only an unassigned `APPR` task. Accept sets the resource and leaves status `APPR`.
- A second person cannot accept a task that already has a resource.

## Acceptance Criteria

1. Auto-Assign with a configured person creates the task (REQ-TRI-003) already carrying that resource, in status `APPR`.
2. Do not Assign creates the task with an empty resource.
3. The named technician accepting an unassigned `APPR` task stores that technician as the resource and leaves status `APPR` and start time empty.
4. A different technician accepting a task that already has a resource is rejected, and the resource is unchanged.
5. Accept is rejected when the task is not `APPR`.
