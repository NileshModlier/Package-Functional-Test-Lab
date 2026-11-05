# REQ-INT-009 Enrollment API read

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an Intellum API client. M1 specifies the contract and does not implement it.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-INT-009 |
| Title | Read an enrollment and its assessment attempts through the simulated read contract |
| Workflow | Intellum-style learning |
| Topic | Enrollment API |

## Description

A later simulated service must let a client with read scope retrieve the enrollment outcome and the attempt history. M1 records that contract and does not expose a server.

## Business Rule

The public API page says the v3 API reads enrollments and assessment responses. The public data-connector description treats enrollment state, completion, assessment passed, and certification earned as data that can leave the learning system. The in-product OpenAPI list is not public, so the lab names its own routes.

## Source Link

- Intellum, "LMS REST API": https://www.intellum.com/integrations/api
- Intellum data connector: https://www.intellum.com/integrations/data-connector
- Intellum, "Intellum API v3": https://clients.intellum.com/student/path/643313-intellum-api-v3

The API page includes enrollments and assessment responses among the objects the API reads. The data-connector page shows those learning facts as reportable data. The route templates are lab names because the public pages do not publish them.

## Simulated Assumptions

- ASM-INT-10. `GET /simulated/intellum/enrollments/{id}` returns the enrollment. `GET /simulated/intellum/enrollments/{id}/assessment-responses` returns its attempts. These paths are lab names.
- Read scope is required. A write-only scope is rejected.
- The enrollment payload includes status, score, completion time, and certificate identifier, using empty values when REQ-INT-004 through REQ-INT-007 have not set them.
- Attempts are ordered by submitted time, oldest first.
- ASM-LAB-01. The lab never sends this request to Intellum.

## Acceptance Criteria

1. `GET` of an existing enrollment with read scope returns the learner, activity, status, score, completion time, and certificate identifier.
2. After a pass and completion with a certificate, that payload shows `Completed`, the passing score, the completion time, and the certificate identifier from REQ-INT-007.
3. `GET` of the attempt collection returns every stored attempt, including failed attempts kept by a reset, in submitted-time order.
4. A write-only scope is rejected and returns no enrollment body.
5. A request for an unknown enrollment identifier is rejected and returns no other learner's enrollment.
