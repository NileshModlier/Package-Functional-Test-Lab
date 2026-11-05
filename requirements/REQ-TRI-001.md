# REQ-TRI-001 Service request

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an IBM TRIRIGA or Maximo system and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-TRI-001 |
| Title | Submit a corrective-maintenance service request |
| Workflow | TRIRIGA / Maximo-style work |
| Topic | Service request |

## Description

A requester saves a draft and submits a corrective service request. A complete submit routes the request for approval.

## Business Rule

IBM's public service-management guide says corrective maintenance is requested through a service request. A self-service user or a contact-center agent selects a request class, enters the details, may save a draft, and submits. After submit, the request is routed for approval. The request class is tied to one service plan, and that plan carries the later task rules.

The lab uses the Maximo status name `WAPPR` for "waiting for approval." That name is a simulated label (`ASM-TRI-01`), chosen because Maximo publishes it for work waiting on approval. It is not a claim that TRIRIGA stores the code `WAPPR`.

## Source Link

- IBM TRIRIGA, *Maintenance and Service Management*, requesting corrective maintenance: https://www.ibm.com/docs/en/SSFCZ3_11.6/pdf/pdf_tri_maint_service_mng.pdf
- IBM Maximo, "Work order statuses": https://www.ibm.com/docs/en/maximo-manage/cd?topic=orders-work-order-statuses

The TRIRIGA guide describes draft, submit, request class, and routing for approval. The Maximo page defines `WAPPR` as waiting for approval. The lab maps the TRIRIGA "routed for approval" moment onto that label under ASM-TRI-01.

## Simulated Assumptions

- ASM-TRI-01. `WAPPR` means the submitted request is waiting for approval.
- ASM-TRI-02. Submit requires request class, requester, building, and description. A draft may omit them.
- The contact-center path and the self-service path create the same request shape. The contact-center user records the requester as the person the request is for.

## Acceptance Criteria

1. Saving an incomplete request stores a draft and does not set `WAPPR`.
2. Submitting a request that has request class, requester, building, and description sets status `WAPPR` and stores a submitted time.
3. Submit with any of those four fields missing is rejected and leaves a draft, or leaves no request if none was saved.
4. A submitted request does not yet have a work task.
5. Self-service and contact-center submits that carry the same required fields produce the same status and the same required-field set.
