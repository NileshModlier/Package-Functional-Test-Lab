# REQ-VER-002 Evaluation form

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not a Verint tenant and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-VER-002 |
| Title | Require answers to mandatory form questions before submit |
| Workflow | Verint-style quality |
| Topic | Evaluation form |

## Description

The sample evaluation form is a set of sections, categories, and questions. Submit is allowed only when every mandatory question has an answer.

## Business Rule

Public material describes a form designer that builds quality forms from the organization's questions, with question types, default answers, and predefined reasons. Fill-out help says each question shows its status, including incomplete and mandatory. Submit, or submit and send for review, is how the evaluator finishes the form.

## Source Link

- Verint help, "Form fill-out area": https://wfo.mon2.verintcloudservices.com/onlinehelp/en_us/QM/Fillout.htm
- Verint help, "Perform an evaluation/assessment": https://wfo.mon2.verintcloudservices.com/onlinehelp/en_us/QM/QM/Perform_an_evaluation_assessment.htm
- Verint Quality datasheet: https://www.verint.com/wp-content/uploads/quality-management-datasheet.pdf

Fill-out help identifies mandatory and incomplete questions and lists submit actions. The perform-evaluation page says the evaluator completes the form with Submit or Submit and Send for Review. The datasheet describes configurable question types and predefined reasons.

## Simulated Assumptions

- ASM-VER-02. Sample form `SIM-QM-001` has three sections with base percentages 60, 20, and 20. Every question is Yes/No and mandatory. The evaluator selects this form. The lab does not auto-select a form from interaction metadata.
- Saving a partial form keeps status `Evaluation in progress`.
- A displayed default that the evaluator has not confirmed counts as unanswered.
- The form names each unanswered mandatory question when submit is rejected.

## Acceptance Criteria

1. Saving a Yes or No answer stores it on that question and leaves the evaluation `Evaluation in progress` when other mandatory questions are empty.
2. Submit with any mandatory question empty is rejected, names each empty mandatory question, and does not calculate a total.
3. Submit when every mandatory question is answered is accepted by this requirement and is scored by REQ-VER-003.
4. A question left at a default unanswered state counts as empty even if the form defines a display default the evaluator has not confirmed.
5. The section weights on `SIM-QM-001` are 60, 20, and 20 and sum to 100.
