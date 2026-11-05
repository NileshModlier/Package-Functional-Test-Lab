# REQ-INT-005 Fail

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an Intellum configuration and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-INT-005 |
| Title | Mark a below-threshold attempt failed and control retakes |
| Workflow | Intellum-style learning |
| Topic | Fail |

## Description

When a submitted score is below the threshold, the enrollment outcome becomes `Failed`. A later attempt is possible only when a reset or re-enrollment is allowed.

## Business Rule

The public certification article says learners who do not pass can be reset individually or in bulk, or re-enrolled for a retake. Pass or fail remains a score decision. Enrollment status stays the outcome record.

## Source Link

- Intellum, "How to Administer a Certification Program at Scale": https://www.intellum.com/resources/blog/how-to-administer-a-certification-program-at-scale-in-intellum

The article states that a score below the threshold is a fail and that non-passing learners can be reset or re-enrolled.

## Simulated Assumptions

- ASM-INT-06. Scores below 80.00 fail. The value 80.00 does not fail.
- ASM-INT-07. The sample activity allows 3 attempts. Attempt history is kept across resets. A reset clears the current fail outcome and returns the enrollment to `Enrolled` so a new attempt can be submitted. Reset does not delete prior attempts.
- A failed attempt never creates a certificate.
- Attendance without a score is not a fail record and is not a pass. It creates no attempt (REQ-INT-003).

## Acceptance Criteria

1. A score of 79.99 sets the attempt outcome to Fail and the enrollment outcome to `Failed`.
2. A failed enrollment has no certificate identifier.
3. After attempts 1 and 2 fail, a reset returns the enrollment to `Enrolled` and retains both attempts in history.
4. A third failed attempt with no further reset rejects a fourth submit, and the enrollment remains `Failed`.
5. Re-enrollment after a failure, when allowed by the attempt limit, creates the next attempt on the same active enrollment rather than a second active enrollment (ASM-INT-02).
