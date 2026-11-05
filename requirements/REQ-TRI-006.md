# REQ-TRI-006 Time entry

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an IBM TRIRIGA or Maximo system and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-TRI-006 |
| Title | Record labor time against an open task |
| Workflow | TRIRIGA / Maximo-style work |
| Topic | Time entry |

## Description

A technician records hours worked against a task that is approved, in progress, waiting on material, or physically complete and not yet closed. Closed and canceled tasks reject time.

## Business Rule

Maximo's public actuals pages say that as work progresses on an approved work order, labor hours are reported on the actuals labor lines. The status page says actuals already reported, or work already in progress, block cancellation.

The TRIRIGA Work Task app description says the technician logs time as a duration or with a timer, that a time-log entry is created when time is modified, and that a technician can see another person's time and cannot edit it. Completed tasks that are not closed can still be edited. Closed tasks are read-only.

## Source Link

- IBM Maximo, "Reporting actuals for work orders": https://www.ibm.com/docs/en/maximo-manage/cd?topic=reporting-actuals-work-orders
- IBM Maximo, "Actuals on work orders": https://www.ibm.com/docs/en/maximo-manage/cd?topic=overview-actuals-work-orders
- IBM Maximo, "Work order statuses": https://www.ibm.com/docs/en/maximo-manage/cd?topic=orders-work-order-statuses
- IBM TRIRIGA, *Maintenance and Service Management*, logging time in the Work Task app: https://www.ibm.com/docs/en/SSFCZ3_11.6/pdf/pdf_tri_maint_service_mng.pdf

The Maximo actuals pages cover labor on an approved work order. The status page covers the effect of actuals on cancel, which this lab reflects by refusing time on `CAN` and `CLOSE` and by not offering cancel of a task that already has time. The TRIRIGA guide covers the time log and the read-only closed task.

## Simulated Assumptions

- Time is accepted when the task status is `APPR`, `INPRG`, `WMATL`, or `COMP`.
- One entry's hours are greater than 0 and at most 24.00, in hundredths of an hour.
- The author of a line may correct that line while the task still accepts time. The author cannot edit another person's line.
- ASM-TRI-06. Hours are a record only. The lab has no payroll or rate engine.
- Recording time does not change task status.

## Acceptance Criteria

1. A time line with 0.01 hours and a time line with 24.00 hours are stored on an `INPRG` task, with labor identifier, date, and hours.
2. Lines with 0 hours, negative hours, or 24.01 hours are rejected, and no line is added.
3. Time lines are rejected when the task is `CLOSE` or `CAN`.
4. A technician can read a coworker's time line and cannot change it.
5. Adding time leaves the task status as it was.
