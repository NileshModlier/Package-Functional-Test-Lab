# REQ-INT-003 Assessment

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an Intellum configuration and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-INT-003 |
| Title | Deliver an on-demand assessment and record the score |
| Workflow | Intellum-style learning |
| Topic | Assessment |

## Description

The sample certification ends in an on-demand assessment. Submitting the attempt stores the earned score on the enrollment's attempt history.

## Business Rule

The public certification article says a certification is based on an assessment the learner must pass. Standard assessments are available on demand and are scored by the platform. Scheduled assessments exist for proctored events. Pass or fail is determined by the score, not by attendance.

This requirement covers scoring the attempt. Pass and fail decisions are REQ-INT-004 and REQ-INT-005.

## Source Link

- Intellum, "How to Administer a Certification Program at Scale": https://www.intellum.com/resources/blog/how-to-administer-a-certification-program-at-scale-in-intellum
- Intellum, "Certifications: Moving Towards Mastery Using Assessments": https://www.intellum.com/resources/blog/certifications-using-assessments

The first article says standard assessments are on demand and automatically scored, and that the outcome follows the score rather than attendance. The second article describes assessments, including quizzes and exams, as the check that can lead to a certificate. Proctoring products named in those articles are out of lab scope (`plan/test-plan.md` section 5).

## Simulated Assumptions

- The sample assessment is a standard on-demand assessment. Scheduled and proctored delivery are not simulated.
- Each question has a point value. Unanswered questions score 0. Percent score is earned points divided by possible points, times 100, rounded half-up to two decimal places.
- Submitting an attempt is final for that attempt. A new attempt requires a fail-and-reset path under REQ-INT-005.
- ASM-INT-07. The attempt is stored even when the later pass/fail rule marks it failed.

## Acceptance Criteria

1. Submitting answers on an in-progress enrollment creates one attempt with a percent score, the raw points, and a submitted time.
2. Unanswered questions contribute 0 points and still count in the possible points.
3. A score is rounded half-up to two decimal places. A raw percent of 79.995 is stored as 80.00. A raw percent of 79.994 is stored as 79.99.
4. An attendance or launch record with no submitted answers does not create a score.
5. A second submit of the same attempt does not create a second score. A further attempt exists only through REQ-INT-005.
