# Summary for hiring managers

**Package Functional Test Lab, v1.0**
**Identifier:** SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.

Personal portfolio. Study models of learning, quality, and facilities workflows, built only from public documentation. No claim of employment, certification, partnership, or access to Intellum, Verint, IBM TRIRIGA, or IBM Maximo. The platform scope stops after milestone M7.

## Quality engineering

The lab treats a testable requirement as the unit of work. Twenty-seven requirements carry business rules, public sources, assumption IDs, and acceptance criteria. A test plan assigns High or Medium risk and lines its sections up with ISO/IEC/IEEE 29119 ideas while stating that the lab is not certified to that standard. Sixty cases were designed in M3 and were not rewritten. Eight further cases entered only after a named reviewer accepted them. The catalog total is 68.

The running oracle is smaller than the study diagrams, and that gap is written down. Quality uses one state field. A work order is one record for both the request and the task. `CAN`, `WSCH`, `WPCOND`, and `HISTEDIT` are not simulator states. Cases that would have expected those behaviors were rejected in review or already recorded the difference.

## Risk mitigation

Risk selected what to automate first: pass and fail at 80.00, completion, certificate dates, weighted quality scores, acknowledgement, dispute, approval, completion, closure, and rework. Six planted defects default to ON in the seed and map to those outcomes:

| Switch | Rule at risk | Off | On |
| --- | --- | --- | --- |
| `pass_mark` | Inclusive 80.00 | 80.00 passes | 80.00 fails |
| `certificate_date` | Issued date equals completion date | Same day | Issued one day early |
| `quality_score` | Weights 60 / 20 / 20 | 70.00, Below standard | 83.33, Meets standard |
| `inactive_assignment` | Inactive technician rejected | HTTP 409 | Assignment accepted |
| `invalid_completion` | Complete only from in progress | HTTP 409 from approved | Approved to complete accepted |
| `reopen_closed` | Closed work stays closed | HTTP 409 | Reopen accepted |

`POST /test/reset` reloads the seed, including the switches. A manual pipeline input, `force_defects` true, is designed to fail the job so the detection still works. Scores use half-up rounding to two decimals. 79.995 becomes 80.00. 79.994 becomes 79.99.

## Automation strategy

One FastAPI and Jinja2 application serves the browser and the API. Playwright covers 26 Chromium paths with page objects and `data-testid` locators. Newman covers three Postman collections with setup, a single workflow iteration, and boundary rows. Local defect-off evidence: UI JUnit 26 tests, 0 failures, 0 errors, 0 skipped. API JUnit 82 tests, 0 failures. API JSON 138 assertions, 0 failed (learning 53, quality 37, work 48). JUnit collapses iterations to one suite per request name, so 82 and 138 are the expected pair.

GitHub Actions defines push, pull request, manual dispatch, and a 20:30 UTC schedule. Python 3.11, Node 20, health check, both suites, a summary step, and artifact upload are in `.github/workflows/regression.yml`. The file was verified locally. It has not been executed on GitHub from this machine. A full UI re-run was not part of M7. The 26/0 figure remains the stored defect-off report.

Non-UI pytest evidence from a later combined run: 24 passed (6 assistant, 3 CI summary, 5 Postman contract, 10 API).

## Testing coverage

Every requirement has at least one case. Regression status, generated in M6, shows Pass where a Playwright test or a Newman request executed, and Not run where the case is still manual or unwired. The eight M7 cases are absent from that status file because M7 did not regenerate it. Their intent is `not-executable`. Traceability is requirement to case to automation ID to last result, with a separate matrix for the six defect detectors.

Seed scale used by every reset: 5 learners, 5 evaluations, 10 work orders. Learning allows at most 3 attempts. Work hours are valid above 0 through 24.00 inclusive.

## Defect detection

Detection is an assertion of the written rule, not a screenshot of a toggle. The suite turns the relevant switch off and expects the M1 outcome. The force flag skips that turn-off. The same assertion fails. UI and API matrices name the test and the observed wrong value for each switch. A shell variable `SIM_FORCE_DEFECTS` left set from a demo will leak into the next browser run. The operating rule is to clear it before publishing a green JUnit file.

The M1 defect template remains the form for an unexpected defect (`DEF-nnn`). The six switches are planted instrumentation with their own detection matrix.

## Traceability and the review gate

`tools/ci_summary.py --check` fails when a requirement has no case, an automated test names a missing case, or a planted defect has no wired assertion. `tools/check_reviewed.py` runs after Python setup in the workflow. It applies to `source: ai-draft` cases only, so the original 60 files are outside the gate. It requires a reviewer, a real requirement file, and a valid case ID. A local run printed `review gate passed`.

The drafter is deterministic. It loads a prompt and copies uncited acceptance criteria from the requirement text. It does not call an external model. Human review is mandatory. On the evaluation set, two requirements produced no draft because every criterion was already cited. Results: 14 generated, 8 accepted, 4 rejected, 1 duplicate, 1 invalid, acceptance rate 0.57, reviewed-draft rate 0.67, reviewer Lab reviewer. The accepted example is TC-INT-022, unanswered questions score 0. The rejected example expected status `CAN` and was refused because the catalog already says `CAN` is not a simulator state.

An external model, if ever introduced, would have to emit the same proposal shape and would still wait for a person to accept. That is future work inside this lab. It is not part of v1.0, and it is not a new product.

## Hiring conversation

The portfolio shows a specification, a system under test with controllable failures, two automation stacks, a pipeline definition, report counts that can be cross-checked, and a human gate on generated tests. State the execution limits in the same breath: the workflow has not been executed on GitHub from this machine, and M7 did not include a second full UI pass.
