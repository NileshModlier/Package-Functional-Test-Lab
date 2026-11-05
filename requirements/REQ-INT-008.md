# REQ-INT-008 Enrollment API write

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an Intellum API client. M1 specifies the contract and does not implement it.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-INT-008 |
| Title | Create and update an enrollment through the simulated write contract |
| Workflow | Intellum-style learning |
| Topic | Enrollment API |

## Description

A later simulated service must let a client with write scope create an enrollment and update allowed fields. M1 records that contract so a future test can call the lab. M1 does not expose a server.

## Business Rule

The public API page says Intellum's v3 REST API reads and writes users, courses, enrollments, assessment responses, and certifications. An administrator creates an OAuth application and chooses Read, Write, or both scopes. The public API v3 guide says the detailed path list is the OpenAPI document available to an unrestricted admin inside the product. That path list is not on the public marketing page.

This requirement therefore binds the lab's own route names, not undocumented vendor paths.

## Source Link

- Intellum, "LMS REST API": https://www.intellum.com/integrations/api
- Intellum, "Intellum API v3": https://clients.intellum.com/student/path/643313-intellum-api-v3

The API page states that the v3 API reads and writes enrollments and that applications use Read, Write, or both scopes. The API v3 guide states that endpoint detail lives in the in-product OpenAPI document. Because that document is not public, the routes below are lab identifiers.

## Simulated Assumptions

- ASM-INT-10. The lab route for creation is `POST /simulated/intellum/enrollments`. The lab route for update is `PATCH /simulated/intellum/enrollments/{id}`. Neither path is an Intellum path.
- Write scope is required. Read-only scope is rejected.
- Create body carries learner and activity identifiers. The business outcome is the same enrollment as REQ-INT-001.
- Patch may correct an administrator note field. Patch may not set score, completion, or certificate fields. Those fields change only through REQ-INT-003, REQ-INT-004, REQ-INT-005, REQ-INT-006, and REQ-INT-007.
- ASM-LAB-01. The lab never sends this request to Intellum.

## Acceptance Criteria

1. `POST /simulated/intellum/enrollments` with write scope, an eligible learner, and a published activity creates one `Enrolled` enrollment and returns its identifier.
2. The same call with read-only scope is rejected and creates nothing.
3. The same call that would violate REQ-INT-001 (duplicate active enrollment or unpublished activity) is rejected and creates nothing.
4. `PATCH` of the note field with write scope stores the note and leaves score, completion time, and certificate identifier unchanged.
5. `PATCH` that attempts to set score, completion, or certificate fields is rejected, and those fields stay unchanged.
