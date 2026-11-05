# REQ-VER-003 Score calculation

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not a Verint tenant and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-VER-003 |
| Title | Calculate and store the evaluation total on submit |
| Workflow | Verint-style quality |
| Topic | Score calculation |

## Description

Submitting a complete evaluation calculates a total from 0 through 100 and stores it on the evaluation. The evaluation is then attached to the interaction.

## Business Rule

Public help says that after submit, the scores on the form are calculated and the evaluation is attached to the interaction. Percentage scoring derives a component score from a relative score times a base percentage. Scoring-rule help says an automatic decrease still respects the configured baseline and does not drive the component through an unbounded negative adjustment.

The lab implements the percentage rollup for one sample form. It does not implement the full form-designer rule catalog.

## Source Link

- Verint help, "Perform an evaluation/assessment": https://wfo.mon2.verintcloudservices.com/onlinehelp/en_us/QM/QM/Perform_an_evaluation_assessment.htm
- Verint help, "Scoring methods": https://wfo.mon2.verintcloudservices.com/onlinehelp/en_us/QM/QM/Scoring_methods.htm
- Verint help, "Scoring rules": https://wfo.mon2.verintcloudservices.com/onlinehelp/en_us/QM/QM/Scoring_rules.htm

The perform-evaluation page says submit calculates the form scores and attaches the evaluation to the interaction. The scoring-methods page describes percentage scoring as relative score times base percentage. The scoring-rules page says a rule-based decrease still considers the baseline and is bounded by the section or form.

## Simulated Assumptions

- ASM-VER-02. Yes earns the question's points. No earns 0. A section's percent is points earned in that section divided by points possible in that section, times 100. The section contribution is that percent times the section base percentage, divided by 100. The total is the sum of the section contributions.
- The total is rounded half-up to two decimal places and is clamped to the inclusive range 0.00 through 100.00.
- Submit without "send for review" sets status `Evaluation submitted`. Submit and send for review is REQ-VER-007 and still uses this score.
- No scoring rule in the sample form lowers a section below 0.

## Acceptance Criteria

1. Submitting a complete `SIM-QM-001` stores one total between 0.00 and 100.00 inclusive and attaches the evaluation identifier to the interaction.
2. All Yes answers produce a total of 100.00. All No answers produce a total of 0.00.
3. A section with base percentage 60 and half of its points earned contributes 30.00 to the total. The other sections do not change that section's contribution.
4. The stored total is rounded half-up to two decimal places.
5. Submit without review sets status `Evaluation submitted` and does not set `Waiting for review`.
