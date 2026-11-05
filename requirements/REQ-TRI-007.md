# REQ-TRI-007 Material entry

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an IBM TRIRIGA or Maximo system and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-TRI-007 |
| Title | Record materials and waiting-on-material status |
| Workflow | TRIRIGA / Maximo-style work |
| Topic | Material entry |

## Description

A technician records materials used on an open task. The technician can also mark the task as waiting on material and later resume it.

## Business Rule

Maximo's public actuals pages include materials reported against the work order. The status page defines `WMATL` as the state in which materials must arrive before the work can be performed, and it allows `APPR` and `INPRG` to move to `WMATL`, and `WMATL` to move back to `INPRG`.

The TRIRIGA Work Task app description says the technician can add parts. Procedure material lists exist in the service-management setup. The lab records the parts the technician says were used. It does not check a storeroom balance. Maximo's separate material-availability status (`NONE`, `PARTIAL`, `COMPLETE`) is public and is not simulated (`plan/test-plan.md` section 5).

## Source Link

- IBM Maximo, "Reporting actuals for work orders": https://www.ibm.com/docs/en/maximo-manage/cd?topic=reporting-actuals-work-orders
- IBM Maximo, "Work order statuses": https://www.ibm.com/docs/en/maximo-manage/cd?topic=orders-work-order-statuses
- IBM Maximo, "Material availability status on work orders": https://www.ibm.com/docs/en/maximo-manage/cd?topic=statuses-material-availability-status-work-orders
- IBM TRIRIGA, *Maintenance and Service Management*, parts on the Work Task app: https://www.ibm.com/docs/en/SSFCZ3_11.6/pdf/pdf_tri_maint_service_mng.pdf

The actuals page lists materials. The status page defines `WMATL` and the transitions this requirement uses. The availability page is cited to show the lab saw the inventory-status feature and left it out of scope. The TRIRIGA guide says technicians add parts while fulfilling the task.

## Simulated Assumptions

- A material line requires an item identifier and a quantity greater than 0.
- Material lines are accepted in `APPR`, `INPRG`, `WMATL`, and `COMP`, and rejected in `CLOSE` and `CAN`.
- ASM-TRI-06. Quantity is a record. No inventory balance changes.
- ASM-TRI-07. `APPR` or `INPRG` may move to `WMATL` with a waiting reason. `WMATL` resumes to `INPRG`. The lab does not complete straight from `WMATL`.
- Recording a material line does not by itself change status.

## Acceptance Criteria

1. A material line with a positive quantity is stored on an `INPRG` task with item, quantity, and entered time.
2. A quantity of 0 or less is rejected, and no line is added.
3. Material lines are rejected on a `CLOSE` task.
4. An `INPRG` task marked waiting, with a reason, becomes `WMATL`. Resuming that task returns it to `INPRG` and keeps the material lines.
5. Adding a material line on `APPR` leaves the status `APPR`.
