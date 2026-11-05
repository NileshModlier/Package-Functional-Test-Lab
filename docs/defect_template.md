# Defect template

**Document ID:** DEF-TPL-001
**Milestone:** M1
**Identifier:** SIMULATED

This template is the only defect artifact in M1. It does not record an observed defect. The lab has no simulator and has executed no tests, so there is nothing to file against a running system.

A defect written later must cite a requirement ID from `requirements/` or, when the issue is in the specification itself, the test-plan or workflow section it contradicts.

## Blank defect

```text
ID:
Title:
Requirement:
Severity:
Priority:
Environment:
Preconditions:
Steps:
Expected Result:
Actual Result:
Evidence:
Status:
```

## Field rules

| Field | Rule |
| --- | --- |
| ID | `DEF-nnn`, assigned in sequence when the first real defect is filed. Do not reuse an ID. |
| Title | One sentence naming the broken rule and the object. Leave out speculation about the cause. |
| Requirement | One or more requirement IDs (`REQ-INT-004`). For a specification defect, cite the document and section instead, and set Requirement to `SPEC`. |
| Severity | Effect on the workflow if the defect is real. Use the scale below. |
| Priority | Order in which the lab should address it. Priority can differ from severity. |
| Environment | Simulated environment name, build or document version, and data set. M1 document defects use `M1 documentation / no runtime`. |
| Preconditions | State that must be true before the steps. Include the requirement's assumption IDs when the expected result depends on them. |
| Steps | Numbered actions a reviewer or tester performed. Steps stay free of the expected result. |
| Expected Result | The observable outcome required by the acceptance criteria or by the cited specification section. |
| Actual Result | The observable outcome that occurred. Quote messages. Do not propose a fix in this field. |
| Evidence | File name, screenshot, response body, or document quote. If there is no attachment, write `None` and say what was observed directly. |
| Status | One value from the status list below. |

## Severity

| Value | Meaning in this lab |
| --- | --- |
| 1 — Blocker | A workflow cannot finish, or a pass, certificate, approval, closure, or acknowledgement is granted or withheld incorrectly. |
| 2 — Major | A required transition, score, assignment, or record is wrong, and a workaround is awkward or lossy. |
| 3 — Minor | A field, message, or secondary rule is wrong, and the primary outcome is still correct. |
| 4 — Trivial | Wording, formatting, or a clarification that does not change a business outcome. |

## Priority

| Value | Meaning |
| --- | --- |
| P1 | Address before any further testing of that workflow. |
| P2 | Address in the current milestone. |
| P3 | Address when the touched area is next changed. |
| P4 | Address if convenient. |

## Status

| Status | Meaning |
| --- | --- |
| New | Filed, not yet reviewed. |
| Open | Confirmed and not yet corrected. |
| In Analysis | Under investigation. The expected result is not yet agreed. |
| Fixed | Corrected, not yet retested. |
| Ready for Retest | A tester can repeat the steps. |
| Closed | Retest matched the expected result, or the reporter accepted a specification change. |
| Deferred | Real, and scheduled for a later milestone. |
| Rejected | Not a defect. The actual result matches the requirement or an accepted assumption. |

## Sample illustration

The record below shows how to fill the template. **It is not an observed defect.** No test was run.

```text
ID: SAMPLE-000
Title: Illustration only — score equal to the threshold would be easy to mis-file
Requirement: REQ-INT-004
Severity: 4 — Trivial
Priority: P4
Environment: M1 documentation / no runtime
Preconditions: ASM-INT-06 is accepted (pass threshold is 80.00 inclusive). No system is under test.
Steps:
1. Read REQ-INT-004 acceptance criterion 1.
2. Compare it with a hypothetical result in which a score of 80.00 is stored as Fail.
Expected Result: A score of 80.00 is a pass.
Actual Result: Not observed. This sample exists to show the fields.
Evidence: None. Illustration only.
Status: Rejected
```

Close `SAMPLE-000` as Rejected if it is ever copied into a tracker by mistake. Do not count it in defect metrics.

## Filing rules for later milestones

- File against the simulated lab, never against a vendor support channel, from this template.
- One defect, one primary failure. Related failures may be linked, not merged, when their requirements differ.
- A mismatch that is caused by an unaccepted assumption is a specification issue (`Requirement: SPEC`) until the assumption register is updated.
- Retest evidence stays on the same ID. Do not open a second defect for the retest.
