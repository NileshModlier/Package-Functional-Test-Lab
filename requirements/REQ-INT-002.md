# REQ-INT-002 Learning modules

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an Intellum configuration and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-INT-002 |
| Title | Record progress through ordered learning modules |
| Workflow | Intellum-style learning |
| Topic | Learning modules |

## Description

A sample learning path is a sequence of modules under one enrollment. The lab records which required modules are complete and which module the learner may start next.

## Business Rule

Public documentation treats catalog activities, and paths made of activities, as the things a learner is enrolled in. Completion of a certification activity is a separate fact from merely being enrolled. The data-connector description lists enrolled and completed as distinct learning facts.

The lab therefore stores module progress on the enrollment and does not treat "enrolled" as "the path is finished."

## Source Link

- Intellum, "How to Administer a Certification Program at Scale": https://www.intellum.com/resources/blog/how-to-administer-a-certification-program-at-scale-in-intellum
- Intellum data connector: https://www.intellum.com/integrations/data-connector

The certification article describes certification activities and paths as the unit learners enroll in, take, and complete. The data-connector page lists enrolled and completed as separate learning facts.

## Simulated Assumptions

- ASM-INT-05. The sample path is ordered. A content module is complete when it is marked viewed. The assessment module is not complete merely because it was opened. It is complete only when the attempt outcome is `Passed` (see REQ-INT-004).
- A learner may hold module progress only on an enrollment in `Enrolled` or `In progress`.
- Skipping a required module on an ordered path is rejected.

## Acceptance Criteria

1. Starting the first module of an ordered path moves the enrollment from `Enrolled` to `In progress` and records that module as started.
2. A content module marked viewed is recorded complete, and the next module becomes startable.
3. Starting module N+1 while required module N is incomplete is rejected, and progress is unchanged.
4. Opening the assessment module without a passing score leaves that module incomplete.
5. Progress counts completed required modules and total required modules on the enrollment.
