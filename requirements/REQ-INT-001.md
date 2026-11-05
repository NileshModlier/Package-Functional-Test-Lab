# REQ-INT-001 Enrollment

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an Intellum configuration and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-INT-001 |
| Title | Create an enrollment for a learner and an activity |
| Workflow | Intellum-style learning |
| Topic | Enrollment |

## Description

The lab records an enrollment when a learner is placed into a catalog activity. That record is the learner's engagement with the activity and the anchor for later score, completion, and certificate facts.

## Business Rule

Public documentation describes an enrollment as the record of a user's engagement with catalog activities. Enrollments are created when a user accesses an activity through the catalog or when an administrator enrolls the user. The public certification operations article also describes enrollment by rule, using attributes such as group, role, or date, so the right people are placed into an activity or path.

The enrollment is created before any assessment outcome exists.

## Source Link

- Intellum, "How to Administer a Certification Program at Scale": https://www.intellum.com/resources/blog/how-to-administer-a-certification-program-at-scale-in-intellum
- Intellum product-guide listing that names "User Activity Enrollment Records": https://experience.intellum.com/student/catalog/list?category_ids=17231-product-guides&page=2

The certification article describes enrollment as the step that places people into a certification, including assignment from group, role, or date. The product-guide listing describes an enrollment as a record of engagement created from the catalog or by an administrator. The guide body itself sits behind Intellum's experience site, so this requirement uses the publicly visible description and does not depend on a signed-in page.

## Simulated Assumptions

- ASM-INT-01. The lab has three creation paths: catalog self-enrollment, administrator enrollment, and rule-based assignment.
- ASM-INT-02. A learner has at most one active enrollment for one activity. A second active enrollment is rejected. A completed enrollment may remain as history.
- ASM-INT-03. The activity must be published. A draft activity cannot be enrolled.
- ASM-INT-04. The new status is `Enrolled`. Score, completion time, and certificate identifier are empty.

## Acceptance Criteria

1. A published activity and an eligible learner produce one enrollment in status `Enrolled` with learner, activity, and created time.
2. Catalog, administrator, and rule-based paths each produce that same enrollment shape.
3. A second active enrollment for the same learner and activity is rejected, and the first enrollment is unchanged.
4. An unpublished activity produces no enrollment.
5. A new enrollment has no score, no completion timestamp, and no certificate identifier.
