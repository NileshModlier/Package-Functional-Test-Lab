# REQ-VER-004 Score threshold

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not a Verint tenant and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-VER-004 |
| Title | Classify the stored total against the quality threshold |
| Workflow | Verint-style quality |
| Topic | Score threshold |

## Description

After a total exists, the lab classifies the evaluation as meeting the sample standard or falling below it. The classification is stored beside the raw total.

## Business Rule

Public form and scoring material treats the score as the organization's measure of quality and leaves the numeric bar to the form's configuration. Coaching material ties follow-up to quality scores. This lab therefore needs an explicit comparison between the calculated total and a configured threshold. The public pages cited here do not publish a universal passing number. The number in this requirement is a lab assumption.

## Source Link

- Verint help, "Scoring methods": https://wfo.mon2.verintcloudservices.com/onlinehelp/en_us/QM/QM/Scoring_methods.htm
- Verint Quality datasheet: https://www.verint.com/wp-content/uploads/quality-management-datasheet.pdf
- Verint, "Employee Coaching for Workforce Optimization": https://www.verint.com/coaching-and-learning/

The scoring and datasheet sources describe configurable scoring rather than one global cut score. The coaching page says coaching is tied to quality evaluation scores, which is why a below-standard result is a meaningful class in this lab.

## Simulated Assumptions

- ASM-VER-03. The sample threshold is 80.00 inclusive. A total greater than or equal to 80.00 is `Meets standard`. A total below 80.00 is `Below standard`.
- The classification does not change the raw total stored by REQ-VER-003.
- Changing the configured threshold later does not rewrite classifications already stored.

## Acceptance Criteria

1. A stored total of 80.00 is classified `Meets standard`.
2. A stored total of 79.99 is classified `Below standard`.
3. A stored total of 100.00 is classified `Meets standard`, and the stored total remains 100.00.
4. The evaluation keeps both the raw total and the classification.
5. An evaluation still `Evaluation in progress`, with no total, has no classification.
