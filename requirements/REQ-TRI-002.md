# REQ-TRI-002 Approval

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an IBM TRIRIGA or Maximo system and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-TRI-002 |
| Title | Approve or reject a submitted service request |
| Workflow | TRIRIGA / Maximo-style work |
| Topic | Approval |

## Description

An approver accepts a waiting request or rejects it with a reason. Acceptance allows task creation. Rejection stops the request and creates no task.

## Business Rule

The public TRIRIGA guide says a submitted service request is routed for approval, and that an approved request is routed onward through the service plan. The public Maximo status page says `APPR` means the work is approved and can begin, and `CAN` means the work order is canceled.

Task creation itself is REQ-TRI-003. This requirement decides whether the request becomes approved.

## Source Link

- IBM TRIRIGA, *Maintenance and Service Management*: https://www.ibm.com/docs/en/SSFCZ3_11.6/pdf/pdf_tri_maint_service_mng.pdf
- IBM Maximo, "Work order statuses": https://www.ibm.com/docs/en/maximo-manage/cd?topic=orders-work-order-statuses

The TRIRIGA guide says the request is approved and then routed using the service plan. The Maximo page defines `APPR` and `CAN`.

## Simulated Assumptions

- ASM-TRI-01. Approved is stored as `APPR`. Rejected is stored as `CAN`.
- ASM-TRI-03. The requester cannot approve their own request. This separation of duties is a lab control. It is not stated as a universal IBM rule in the cited pages.
- Rejection requires a reason. Approval does not.
- Only `WAPPR` can be approved or rejected.

## Acceptance Criteria

1. An approver who is not the requester sets a `WAPPR` request to `APPR` and stores the approver and the approval time.
2. The requester attempting to approve their own `WAPPR` request is rejected, and the status stays `WAPPR`.
3. An approver rejecting a `WAPPR` request with a reason sets status `CAN` and stores the reason.
4. A rejection without a reason is rejected, and the status stays `WAPPR`.
5. Approve and reject actions on a request that is not `WAPPR` are rejected, and the status is unchanged.
