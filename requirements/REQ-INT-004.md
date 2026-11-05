# REQ-INT-004 Pass

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an Intellum configuration and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-INT-004 |
| Title | Mark an assessment attempt passed when the score meets the threshold |
| Workflow | Intellum-style learning |
| Topic | Pass |

## Description

When a submitted assessment score meets the activity threshold, the enrollment outcome becomes `Passed`.

## Business Rule

The public certification article says pass or fail is determined by the score threshold, and that enrollment status is the definitive record of the learner outcome. Attendance is not the pass rule.

## Source Link

- Intellum, "How to Administer a Certification Program at Scale": https://www.intellum.com/resources/blog/how-to-administer-a-certification-program-at-scale-in-intellum

The article states that pass or fail follows the score threshold and that enrollment status is the record used for credentialing and reporting.

## Simulated Assumptions

- ASM-INT-06. The sample threshold is 80.00 percent, inclusive. The comparison uses the two-decimal score from REQ-INT-003.
- A passing attempt sets the enrollment outcome to `Passed` and stores the score on the enrollment.
- Passing makes the learner eligible for completion under REQ-INT-006. This requirement does not itself issue a certificate.

## Acceptance Criteria

1. A score of 80.00 sets the attempt outcome to Pass and the enrollment outcome to `Passed`.
2. A score of 80.01 sets the same Pass outcomes.
3. A score of 79.99 does not set `Passed`.
4. The passing score stored on the enrollment equals the attempt score.
5. A pass does not, by itself, write a certificate identifier. Certificate creation is REQ-INT-007.
