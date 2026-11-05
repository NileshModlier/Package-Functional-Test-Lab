# REQ-VER-007 Review and dispute

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not a Verint tenant and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-VER-007 |
| Title | Accept, dispute, and resolve an evaluation sent for review |
| Workflow | Verint-style quality |
| Topic | Interaction evaluation |

## Description

An evaluator can submit a completed form for the employee to review. The employee accepts it or disputes answers. A reviewer resolves a dispute. The score stays the score that was calculated at submit unless a later, separate rescore is out of scope for this requirement.

## Business Rule

Public help says Submit and Send for Review sets the evaluation to Waiting for Review and places it for the employee. Fill-out help lists the later statuses: Accepted when the employee accepts the review, Disputed when one or more answers are disputed, and Resolved when the disputed answers have been reviewed and resolved. A public dispute article describes people re-checking the interaction and agreeing the recorded result. This requirement covers the status path, not a calibration product.

## Source Link

- Verint help, "Perform an evaluation/assessment": https://wfo.mon2.verintcloudservices.com/onlinehelp/en_us/QM/QM/Perform_an_evaluation_assessment.htm
- Verint help, "Form fill-out area": https://wfo.mon2.verintcloudservices.com/onlinehelp/en_us/QM/Fillout.htm
- Verint, "5 Steps to Resolve Agent Evaluation Disputes": https://www.verint.com/blog/5-steps-to-resolve-agent-evaluation-disputes/

The perform-evaluation page says send-for-review changes the status to Waiting for Review. Fill-out help defines Accepted, Disputed, and Resolved. The dispute article describes review and agreement around the evaluation. Calibration tasks named in that article are outside this lab.

## Simulated Assumptions

- ASM-VER-05. A dispute names at least one question and includes a comment. The evaluated employee cannot move Disputed to Resolved.
- Accept and dispute are available only from `Waiting for review`.
- Resolving the dispute does not, in this requirement, change the total calculated at submit. A rescore would be a new specification.
- The actor who resolves is a reviewer and is not the evaluated employee.

## Acceptance Criteria

1. Submit and send for review, on a complete form, stores the score from REQ-VER-003 and sets status `Waiting for review`.
2. The evaluated employee can set `Waiting for review` to `Accepted`. The total is unchanged.
3. The evaluated employee can set `Waiting for review` to `Disputed` only when at least one question and a comment are supplied.
4. A reviewer other than the evaluated employee can set `Disputed` to `Resolved`. The evaluated employee cannot.
5. Accept, dispute, and resolve are rejected from `Evaluation in progress`, and the status stays `Evaluation in progress`.
