# Interview guide

**Project:** Package Functional Test Lab
**Identifier:** SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.
**Questions:** 50, numbered, with answers taken from this repository.

Use these answers in a portfolio interview. They describe a personal study lab. They do not describe employment at IBM or at a software vendor, and they do not describe access to a vendor tenant. Where a public source was silent, the lab recorded a simulated assumption. The assistant does not call an external model. The GitHub Actions workflow has not been executed on GitHub from this machine.

## Functional testing

### 1. What is Package Functional Test Lab?

It is a personal portfolio that practices a functional-testing chain on three simulated workflows: learning, quality, and facilities work. The chain is requirements, a FastAPI and Jinja2 simulator called Package Sim, a YAML case catalog, Playwright on Chromium, Postman collections run by Newman, a GitHub Actions workflow, and a review-gated drafter. Milestones M1 through M7 are complete in the repository. The workflows are study models from publicly available documentation about Intellum-style learning, Verint-style quality, and IBM TRIRIGA and IBM Maximo work orders. The lab does not claim employment, certification, partnership, or access to those products.

### 2. What does “done” mean for v1.0?

Done means each milestone’s artifact is in git and the local measurements were recorded. There are 27 requirements, 68 cases (60 from M3, unchanged, plus 8 accepted in M7), 26 Chromium tests with a defect-off JUnit of 26 tests, 0 failures, 0 errors, 0 skipped, and a Newman defect-off pair of 82 JUnit tests and 138 JSON assertions, both with 0 failures. The review gate printed `review gate passed`. Done also means the limits are stated: accepted M7 cases have `automation_intent: not-executable`, and the workflow file has not been executed on GitHub from this machine.

### 3. How did you decide what was in scope?

`plan/test-plan.md` fixes scope before execution. In scope are enrollment through certificate, evaluation through coaching, and service request through closure, all on Package Sim. Out of scope for the executed suites are live vendor tenants, proctoring, analytics, procurement, penetration, load, and accessibility. Maximo names `WSCH`, `WPCOND`, and `HISTEDIT` are named in the plan’s exclusion list and are not simulator states. A defect that asks the lab to implement an excluded feature is rejected against that section, or it becomes an explicit scope change before a test is added.

### 4. What belongs in a requirement file here?

Each of the 27 files has an ID, a description, a business rule, a public source link, simulated assumptions, and acceptance criteria. The inventory is `requirements/README.md`: REQ-INT-001–009, REQ-VER-001–008, REQ-TRI-001–010. Risk is High or Medium from the test plan. High means an incorrect result would issue or withhold a credential, a quality outcome, an acknowledgement, a work task, or a closure. Thirteen requirements are High and fourteen are Medium. M1 left every row at coverage state Specified. Later milestones attach cases. The requirement text itself was not rewritten.

### 5. What is an assumption ID, and why not just “the product says so”?

When a public document leaves a rule unspecified, the lab writes a simulated assumption and gives it an ID. `ASM-INT-06` is the sample pass threshold of 80.00 percent, inclusive, two decimal places, half-up. `ASM-TRI-08` is rework from `COMP` to `INPRG` when a reason is present, which is the lab’s join between a TRIRIGA rework story and a Maximo status table. Cases cite the assumption in `assumption_ids` or in `known_sut_differences`. The assumption is a test-lab choice. It is not a vendor requirement. Vendor names identify which public documentation was studied.

### 6. How do you talk about ISO/IEC/IEEE 29119 in this lab?

The test plan maps its sections onto 29119 ideas: scope, objectives, items, features, levels, techniques, entry and exit, risks, and work products. The plan says that alignment is conceptual and that the lab has not been certified against the standard. M1 was static testing of the documents. Dynamic execution arrived with Package Sim, Playwright, and Newman. I keep those two sentences together so a finished plan is not described as a certification or as a finished test.

### 7. Which functional outcomes did you treat as the ones that must not be wrong?

The high-risk set in the traceability strategy: learning pass, fail, completion, and certificate (REQ-INT-004 through REQ-INT-007); quality score, threshold, acknowledgement, and dispute (REQ-VER-003, REQ-VER-004, REQ-VER-006, REQ-VER-007); work approval, task creation, completion, closure, and rework (REQ-TRI-002, REQ-TRI-003, REQ-TRI-008, REQ-TRI-009, REQ-TRI-010). Those rows were the first automation candidates. Medium rows still have cases. Risk chose depth and automation order. It did not drop a requirement from the matrix.

### 8. What is the difference between a Passed enrollment and a Completed enrollment?

They are different states, on purpose. An assessment moves In Progress to Passed or Failed. Only Passed may move to Completed, and a certificate record is issued when the activity is configured for one. The certificate is a record, not a state. That split is why `pass_mark` and `certificate_date` are separate switches. A learner can be correctly passed and still carry a wrong issued date, or correctly completed while 80.00 was scored under the wrong comparison. REQ-INT-006 and REQ-INT-007 own those rules. The fourth assessment attempt is rejected, and a Failed enrollment may reset to Enrolled while attempts used stay below 3.

## Boundary testing

### 9. How does half-up rounding work on an assessment score?

The simulator rounds half-up to two decimal places before the pass comparison. A raw percent of 79.995 is stored as 80.00. A raw percent of 79.994 is stored as 79.99. With `pass_mark` off, the stored score passes when it is greater than or equal to 80.00. So 79.995 passes, 80.00 passes, 80.01 passes, and 79.994 fails as 79.99. With `pass_mark` on, the comparison becomes exclusive: exactly 80.00 fails, and only a score greater than 80.00 passes. REQ-INT-003 AC-3 states the rounding examples. REQ-INT-004 owns the threshold.

### 10. Which boundary rows did Newman actually execute?

`postman/data/pass_mark_boundaries.csv` has 79.99, 80.00, 80.01, 79.994, and 79.995. `quality_boundaries.csv` has section points aimed at 79.99, 80.00, and 80.01. `work_hours_boundaries.csv` has 0, 0.01, 24, and 24.01. Hours must be greater than 0 and at most 24.00, so 0 and 24.01 are rejected and 0.01 and 24 are stored, with the order staying APPR. Quality classification with `quality_score` off is `Meets standard` at 80.00 or above. The learning pass-mark switch does not move the quality threshold.

### 11. Why are 79.994 and 79.995 in the pass-mark file along with 79.99 and 80.01?

79.99 and 80.01 sit on either side of the threshold and never exercise rounding. 79.995 and 79.994 sit on either side of the half-up digit. The API defect matrix records the consequence: the 79.995 row rounds to 80.00 and passes when `pass_mark` is off, and that same row was Failed when the switch stayed on. A suite of only nice two-decimal inputs would have left `ASM-INT-06` unchecked. The JSON report keeps each CSV iteration, which is where a one-row rounding failure shows up.

### 12. Give the weighted quality boundary you use as a worked example.

Sections A 1/2, B 1/1, and C 1/1. Weights are A 60, B 20, C 20. Defect off: 70.00, Below standard. Defect on, unweighted mean: 83.33, Meets standard. The UI test is `test_weighted_sections_score_70` on TC-VER-005. The Newman request is `TC-VER-005 Score weighted sections as 70`. Threshold neighbors are in `test_threshold_79_99_is_below_and_80_meets` and `test_threshold_80_01_meets_standard`. When `quality_score` stayed on, the threshold request’s unweighted scores were 66.66, 66.67, and 66.68, which is the defect-on observation in `docs/api_defect_matrix.md`.

## State transition testing

### 13. Walk the learning state machine the way the simulator implements it.

Activity catalog status is separate: Available or Draft. Enrollment moves Available activity plus enroll to Enrolled, provided there is no other active enrollment for that learner and activity. Draft activities are rejected. Enrolled plus start goes to In Progress and marks content modules complete. In Progress plus a score goes to Passed or Failed and increments attempts. Failed plus reset returns to Enrolled when attempts used are below 3, and history is kept. Passed plus complete goes to Completed. Illegal completion, such as completing a Failed enrollment, returns HTTP 409.

### 14. Walk the quality state machine.

One `state` field. Pending plus submit of sections A, B, and C goes to Under Review. From Under Review the evaluation can be Acknowledged, Disputed with a comment, or Coached with a note. Disputed plus resolve returns to Under Review. Acknowledged can be Coached or Completed. Coached can be Acknowledged or Completed. Pending cannot jump to Acknowledged, Coached, or Completed. Disputed cannot complete until it returns to Under Review. M1 described a separate coaching lifecycle. The simulator folded that into this single machine, and `docs/package_sim.md` records the map. Acknowledgement does not change the score. Coaching does not change the score. Those are TC-VER-009 and TC-VER-015.

### 15. Walk the work-order machine, including the branch and the rework edge.

Draft to WAPPR when required request fields are present. WAPPR to APPR when `actor_id` is present and is not the requester. APPR to INPRG when a technician is assigned. APPR or INPRG can move to WMATL, and WMATL can return to INPRG. INPRG to COMP. COMP to CLOSE. COMP to INPRG when a rework reason is present: actuals stay, `completed_at` is cleared, assumption `ASM-TRI-08`. `INPRG` to `CLOSE` is rejected. `CLOSE` has no successor while `reopen_closed` is off. One record is both the request and the task. The M1 diagram’s separate task object is a known difference, written on the cases.

### 16. Which transitions are negative tests with HTTP 409?

Self-approval. Start without a technician. Inactive technician `TEC-02` while `inactive_assignment` is off. `INPRG` to `CLOSE`. `WMATL` to `COMP`. `APPR` to `COMP` while `invalid_completion` is off. `CLOSE` to `INPRG` while `reopen_closed` is off. Time on a closed order. Duplicate active enrollment, unpublished activity, assessment before start, and a second completion are also 409. Unknown IDs are 404. Missing sections, an empty dispute, a blank title, rework without a reason, hours out of range, and zero material are 422. The `detail` body is part of the assertion, not only the status code.

### 17. Why is `CAN` a state-transition question you refuse to automate?

REQ-TRI-002 contains the sentence that rejecting a WAPPR request with a reason sets `CAN`. The public Maximo material names `CAN`. Package Sim does not implement `CAN`, `WSCH`, `WPCOND`, or `HISTEDIT`. TC-TRI-004 already says rejecting a request to `CAN` is not a simulator state. The M7 drafter proposed `REQ-TRI-002-01` anyway, because the sentence is in the requirement and terminology validation allowed it. Review rejected it and stored the reason. A grounded transition list is still the wrong expected result when the build has recorded that the state is absent.

## Decision tables

### 18. Where is the pass-mark decision table?

Two conditions: the rounded score relative to 80.00, and whether `pass_mark` is off or on.

| Rounded score | `pass_mark` off | `pass_mark` on |
| --- | --- | --- |
| 79.99 | Failed | Failed |
| 80.00 | Passed | Failed |
| 80.01 | Passed | Passed |

79.994 follows the 79.99 column after rounding. 79.995 follows the 80.00 column. The inclusive rule exists only in the off column. The UI detector for the interesting cell is `test_score_80_passes_when_pass_mark_defect_is_off` on TC-INT-008. Newman hits the same cell in `TC-INT-008 Pass at 80.00` and in the 80.00 boundary row of TC-INT-007.

### 19. Where is the quality-score decision table?

Conditions: weighted versus unweighted formula, and the resulting total against 80.00. Weights apply only when `quality_score` is off: A 60, B 20, C 20. On uses the unweighted mean of the three section percents. Classification is Meets standard at 80.00 or above, otherwise Below standard. The A 1/2, B 1/1, C 1/1 input is the cell that flips: 70.00 Below standard versus 83.33 Meets standard. Neighbor totals 79.99, 80.00, and 80.01 are their own rows in the quality CSV. 80.00 meets standard when the weighted rule is in force.

### 20. Where is the approval and completion decision table?

Approval: an `actor_id` must be present, and that actor must not be the requester. Missing those conditions, WAPPR stays unapproved and the response is 409. Completion with `invalid_completion` off: the only predecessor of COMP is INPRG. APPR to COMP is 409, and WMATL to COMP is 409. With `invalid_completion` on, APPR to COMP is accepted. The switch does not legalize INPRG to CLOSE. Closure with `reopen_closed` off: CLOSE has no successor. With it on, CLOSE to INPRG is accepted and `reopened` becomes true. Rework is a separate column: COMP to INPRG requires a reason. Without a reason the response is 422 and the state stays COMP.

### 21. How did you keep a decision table from inventing columns?

The assistant may use the technique name `decision-table`, and the prompt forbids a new threshold, status, or role. Terminology validation rejects backtick phrases, short all-caps tokens, numbers, and snake_case names that are absent from the requirement and from cases that cite it. The contrast draft that said `biometric_signature` was counted as invalid and was not written. A decision table in this lab combines conditions the text already states. It does not add a column for a control the build does not have.

## Playwright

### 22. How is the UI suite structured?

`tests/ui/` has `conftest.py`, three page objects, and three test modules. Learning has 9 tests, quality 8, work orders 9, total 26. pytest-playwright drives the browser. The `browser_name` fixture returns `chromium`. Locators are `data-testid` values such as `enroll-learner`, `enrollment-{id}`, `defect-{id}`, and `defect-toggle`. Tests call the page object. Markers `smoke`, `regression`, and `critical` are registered for selection. The CI command is `python -m pytest tests/ui` with JUnit XML, tracing, screenshots, and video retained on failure.

### 23. How does a UI test get a clean seed?

The autouse fixture `reset_sim` sends `POST /test/reset` before every test and asserts HTTP 200. Reset reloads `sim/seed.json`: 5 learners, 5 evaluations, 10 work orders, and all six defect switches ON. Tests that need the M1 rule then call `defects.disable("pass_mark")` or the matching ID. The defects page shows ON or OFF. The fixture clicks Turn off only when the button text says that action is available.

### 24. What do `SIM_EXTERNAL` and `SIM_FORCE_DEFECTS` change?

`SIM_EXTERNAL=1` means CI already started Uvicorn on `127.0.0.1:18765`. The session fixture waits for `/health` and does not launch a second server, so Newman can use the same process. Unset, pytest starts Uvicorn itself and terminates it at the end of the session. `SIM_FORCE_DEFECTS=on` makes `set_enabled` return immediately, so the seeded ON value survives. The six detector tests then fail. Any other value, including an empty string, allows the toggle. The simulator process does not read `SIM_FORCE_DEFECTS`. Forgetting to clear it in PowerShell is how a green run turns red after a demo.

### 25. What did the local Chromium run record, and what did M7 rerun?

`reports/ui.xml` records 26 tests, 0 failures, 0 errors, 0 skipped, defects off. The same six detector tests were run again with the force flag and failed on the correct-behavior assertion. The other 20 passed in the default run and do not depend on a switch. M7 did not re-run the full UI suite. A later combined pytest figure of 24 passed refers to 6 assistant tests, 3 CI summary tests, 5 Postman contract tests, and the 10 API tests in `test_package_sim.py`. Quoting 24 as a UI result would be wrong.

### 26. How do you investigate a Playwright failure in this design?

Start with `reports/ui.xml` for the test name. On a CI failure, `test-results/` holds the trace, screenshot, and video, because those are retained only on failure. `reports/sim.log` is the server log if `/health` never returned 200 within 60 seconds. If the failure is “state was Failed” on the 80.00 test, check whether `SIM_FORCE_DEFECTS` was `on` or the defects page still said ON. That is a successful detection of `pass_mark`, recorded in `trace/defect_detection_matrix.md`, and it is a product bug only when the suite believed the switch was off.

## Postman

### 27. How are the collections factored?

Three collections, each able to run alone: Package Sim Learning, Package Sim Quality, Package Sim Work Orders. Each has Setup, Workflow, and Boundaries. Setup calls `/health`, `POST /test/reset`, and turns the switches that collection cares about OFF. Workflow runs on iteration 0. Later CSV iterations skip it. Boundaries run on every row and are skipped when Newman has no data file. IDs created mid-iteration sit in collection variables: `enrollmentId`, `evalDisputeId`, `newOrderId`. `postman/build_collections.py` regenerates the JSON, the environment, the CSV files, and the rows in `docs/api_traceability.md`.

### 28. How do variables decide the base URL and the defect mode?

`postman/environments/local.postman_environment.json` sets `baseUrl` to `http://127.0.0.1:18765` and `forceDefects` to `false`. Every request URL is `{{baseUrl}}` plus a path. Environment values override collection values. CSV columns arrive through `pm.iterationData` and are substituted into bodies as `{{score}}`, `{{earned_a}}`, or `{{hours}}`. Newman `--env-var forceDefects=true` is the defect-on run: Disable requests are skipped and the seed switches stay ON. The collections call Package Sim. They do not call Intellum, Verint, IBM TRIRIGA, or IBM Maximo.

### 29. What does a contract test protect that Newman itself does not?

`tests/test_postman_contract.py` has five tests. They check that requests carry tests and use `baseUrl`, that the environment loads the local URL, that the CSV files contain the required boundary values, that `docs/api_traceability.md` lists every request and case, and that the combined Newman report has no failed assertions. A regenerated collection can drift from the trace even when a single happy-path call returns 200. The contract tests fail that drift in pytest, before anyone treats a green Newman log as complete coverage.

## Newman

### 30. Why are there 82 JUnit tests and 138 JSON assertions?

They are two views of the defect-off run. Newman’s JUnit reporter collapses iterations to one suite per request name, so `reports/api.xml` has 82 tests and 0 failures. `reports/api.json` keeps every CSV iteration. Assertions total 138 and failed 0: learning 53 across 5 iterations, quality 37 across 3 iterations, work 48 across 4 iterations. `reports/summary.md` publishes the JUnit pair, UI 26 and API 82. I quote the JSON total whenever the question is about boundary rows, because a failure on only 79.995 would be one iteration inside a request that JUnit has already folded.

### 31. What command produces the learning evidence?

From the lab root, with Package Sim listening on port 18765:

```text
npx newman run postman/collections/learning.postman_collection.json -e postman/environments/local.postman_environment.json -d postman/data/pass_mark_boundaries.csv --reporters cli,junit,json --reporter-junit-export reports/learning.xml --reporter-json-export reports/learning.json
```

Quality and work orders use the matching collection, CSV, and export names in `docs/postman.md`. The milestone copied the three results into `reports/api.xml` and `reports/api.json`. Adding `--env-var forceDefects=true` is the defect-on command. Those runs exited 1 on the planted switches. Rows that do not depend on a switch, including 79.99, 80.01, 79.994, duplicate enrollment, INPRG to CLOSE, and COMP to CLOSE, still passed in that defect-on API run.

### 32. How do you avoid double-counting a workflow when the CSV has five rows?

The Workflow folder is guarded so it runs on iteration 0 and later iterations skip it. Boundaries run on every row. Setup still resets at the start of the iteration pattern the collection defines, which is why a boundary score is not inherited from the previous learner’s pass. If someone removed the iteration guard, five rows would attempt five full enroll-start-complete journeys and the JUnit-versus-JSON gap would change meaning. The contract and the collection builder are what keep that guard in the generated JSON.

## GitHub Actions

### 33. What triggers the regression workflow, and what does each trigger mean?

`.github/workflows/regression.yml` is named Regression. `push` and `pull_request` run on every push and every pull request. `schedule` uses cron `30 20 * * *`, which is 20:30 UTC. `workflow_dispatch` is the manual run. Its only input is `force_defects`, a choice of `false` or `true`, default `false`. False is the normal regression. True leaves the six planted switches ON so the same assertions fail and the job fails on purpose. The runner is `ubuntu-latest`, Python 3.11, Node 20.

### 34. What is the step order, and why is the review gate where it is?

Checkout, Python 3.11, `python tools/check_reviewed.py`, Node 20, pip install of `sim/requirements.txt`, global Newman, Chromium with dependencies, Uvicorn on `127.0.0.1:18765` under `setsid`, health poll for up to 60 seconds, `pytest tests/ui`, three Newman collections, `tools/ci_summary.py`, upload, then stop the server. The gate is immediately after Python setup so an unreviewed `ai-draft` case fails the job before Chromium or Newman starts. The gate does not draft proposals and does not change the simulator. A local run printed `review gate passed`.

### 35. How is `force_defects` wired, in the expressions that actually appear in the file?

The job environment sets `SIM_EXTERNAL` to `1` and sets `SIM_FORCE_DEFECTS` to `on` only when `github.event.inputs.force_defects == 'true'`. Otherwise the expression yields an empty string. The Newman step adds `--env-var forceDefects=true` only when `SIM_FORCE_DEFECTS` equals `on`. The summary step passes `--force-defects` to `ci_summary.py` under the same condition. On push, pull request, and schedule there is no dispatch input, so the ordinary design is a defect-off run. I do not describe an empty string as “defects on.”

### 36. What has been verified, and what has not been run on GitHub?

The workflow file is in the repository. The local suites, the summary tool, and `check_reviewed.py` were run on this machine. `reports/summary.md` shows the green defect-off table. The workflow has not been executed on GitHub from this machine. I do not claim a green GitHub check, an Actions URL, or a nightly run that I watched in the GitHub UI. Upload of `regression-reports` is what the YAML specifies: `reports/ui.xml`, `reports/api.xml`, `reports/api.json`, `reports/summary.md`, `reports/sim.log`, `trace/regression_status.md`, and `test-results/`.

### 37. What does the summary check add beyond “pytest exited 0”?

`tools/ci_summary.py --check` fails when a requirement has no case, an automated test names a missing case, or a planted defect is not wired to an assertion. It also writes `reports/summary.md` and `trace/regression_status.md` from the JUnit it was given, and on Actions it appends the summary to `GITHUB_STEP_SUMMARY`. A green process exit with an orphan test would still fail this step. `tests/test_ci_summary.py` covers the table counts, the planted-defect links, and the published green summary. That module is 3 tests, part of the 24 non-UI combined run.

## Traceability

### 38. What is the chain, and which file is the strategy versus the status?

`docs/traceability_strategy.md` (TRACE-001) defines Requirement → Test case → Automation → CI result. A manual test stops at the case. Its automation note is the strategy’s “not applicable” manual branch, and it has no CI result. `trace/regression_status.md` is the M6 status generated from `reports/ui.xml` and `reports/api.xml`. A Pass cell names `AUTO-…` plus the pytest function, the Newman request, or both. A Not run cell is a case with no automation result in those reports. Orphan automation, a check with no requirement, is a process defect against the strategy.

### 39. How are IDs actually written in `cases/`, as opposed to the early pattern sketch?

The strategy sketch used a two-suffix form such as `TC-INT-004-01`. The files that were built use `TC-INT-001` through the later numbers, with the acceptance criterion inside the file: `REQ-INT-003 AC-2`. Automation IDs in the status file follow that case number, for example `AUTO-INT-008` for `TC-INT-008`. I answer with the ID a reviewer can open. Requirement IDs were never renumbered to make the matrix look dense.

### 40. Why are TC-INT-022 and the other seven M7 cases missing from regression status?

M6 generated `trace/regression_status.md` before those files existed. M7’s own note says the next CI run is what would add the new cases as Not run, and that this milestone did not regenerate the file and did not execute the workflow on GitHub. The eight files are still in `cases/`, each with `status: Accepted`, `source: ai-draft`, and `execution.result: not-run`. Absence from the status file is a generation gap I can point at. It is not a claim that the cases were executed.

### 41. What coverage states do you use so a status report stays honest?

Specified, Planned, Written, Automated, Executed, Blocked. M1 used Specified only. Moving a row to Executed without a result record is a traceability defect. M3 cases are Written. The subset with a Pass in regression status has been Executed for that local defect-off run. M7 cases are Written design records. They are not Automated, because `automation_intent` is `not-executable` and `execution.automated` is false. Blocked would need a defect or an environment note. I do not upgrade a Written row because a neighboring row passed.

## Defect management

### 42. What is a planted defect in this lab, and how is it different from a filed DEF-nnn?

The six switches are intentional mis-implementations so a regression can prove it still detects a broken rule. They default to ON in `seed.json`. They are not DEF records of a surprise found in production. The M1 defect template defines `DEF-nnn` for a later observed defect, with severity, priority, expected, actual, and evidence. M1 itself filed nothing, because there was no runtime yet. The detection matrices are the evidence that each switch, when left on, breaks one named assertion.

### 43. Name the six switches, the requirement, and the failure you expect when each stays on.

| Switch | Requirement | Defect-on observation |
| --- | --- | --- |
| `pass_mark` | REQ-INT-004 | Score 80.00 is Failed. Greater than 80.00 can still pass. |
| `certificate_date` | REQ-INT-007 | `issued_on` is one day before `completion_date` (2026-11-04 versus 2026-11-05 in the UI matrix). |
| `quality_score` | REQ-VER-003 | A 1/2, B 1/1, C 1/1 scores 83.33 and Meets standard. The off path for the same input is 70.00 and Below standard. |
| `inactive_assignment` | REQ-TRI-004 | `TEC-02` is assigned. The off path is HTTP 409 and WO-03 stays unassigned. |
| `invalid_completion` | REQ-TRI-008 | APPR to COMP is accepted. The off path is HTTP 409. |
| `reopen_closed` | REQ-TRI-009 | CLOSE to INPRG is accepted. The off path is HTTP 409. |

`POST /api/defects/{id}` with `{"enabled": false}` turns one switch off. `POST /test/reset` turns all six back on. A switch changes new decisions. It does not rewrite scores already stored in the seed. `invalid_completion` does not allow INPRG to CLOSE.

### 44. How do you demonstrate the failing pipeline without pretending GitHub ran it?

I show `.github/workflows/regression.yml` and say the manual input `force_defects` true is designed to fail. Locally I set `SIM_FORCE_DEFECTS=on` and run a detector such as `test_score_80_passes_when_pass_mark_defect_is_off`, or I add `--env-var forceDefects=true` to a Newman command from `docs/postman.md`. I then remove the environment variable. I say plainly that this machine has not executed the workflow on GitHub. The red result I can stand next to is the local detector, plus the YAML that would pass the same flags to both suites.

### 45. What did the quality and certificate defects teach about oracles?

The quality switch changes the formula and the classification together, so an assertion on only the word “Meets standard” could pass for the wrong arithmetic. The lab asserts the number 70.00 as well as Below standard. The certificate switch leaves the learner Completed and moves the issued date. An assertion that only checks “a certificate exists” would miss it. TC-INT-016 compares issued date with completion date. Detection is only as strict as the expected result.

## AI-assisted testing

### 46. What does the assistant actually do on a propose run?

`tools/ai_assistant.py propose --requirements` takes 8 to 10 requirement IDs. It loads `tools/prompts/edge_cases.md`, then each requirement and the cases that cite it. It drafts at most two acceptance criteria that no case cites. It copies that criterion sentence into the title, the step, and the expected result, and the `why` line names the criterion. On the first requirement it also builds two contrast drafts: a copied title, counted as a duplicate, and a draft that introduces `biometric_signature`, counted as invalid. Those two are not written. The tool does not call an external model. There is no model client in `sim/requirements.txt`. The tools parse YAML with regular expressions. PyYAML is not a dependency.

### 47. Which techniques may a draft use, and what makes it invalid or a duplicate?

The prompt requires the names `boundary`, `negative`, `state-transition`, `decision-table`, and `exploratory`, and it requires `reviewed_by`. Schema validation demands `source: ai-draft`, `status: proposed`, `reviewed_by` null, a requirement ID shaped `REQ-INT`, `REQ-VER`, or `REQ-TRI`, and title, steps, expected, and why. Terminology validation rejects new backtick phrases, short all-caps tokens, numbers, and snake_case names. A duplicate is a criterion a case already cites, or a normalized title that matches an existing case for that requirement. Invalid and duplicate increment the metrics and do not create a file.

### 48. Walk through the accepted example TC-INT-022.

The evaluation included REQ-INT-003. AC-2, unanswered questions contribute 0 points and still count in the possible points, was not cited by an existing case. The drafter wrote proposal `REQ-INT-003-01` with technique exploratory. Review accepted it as `cases/TC-INT-022.yaml`. The file has `source: ai-draft`, `reviewed_by: "Lab reviewer"`, `status: Accepted`, `automation_intent: not-executable`, and `execution.automated: false`. The step text is the AC-2 sentence. Accept deleted the proposal and refused to overwrite any existing case. The case is a design record. It is not a browser test and it is not a Newman request.

### 49. Why were four drafts rejected, and why is that a successful review?

| Proposal | Reason stored |
| --- | --- |
| REQ-TRI-002-01 | Existing cases already record that CAN is not a simulator state. |
| REQ-INT-008-01 | TC-INT-018 already records that read-only scope is not implemented. |
| REQ-INT-008-02 | TC-INT-018 already records that PATCH of a note is not implemented. |
| REQ-TRI-005-02 | TC-TRI-009 already records that `started_at` is not stored. |

Each sentence appears in a requirement, so a purely lexical gate let it through. Review is where the known simulator difference wins. REQ-INT-006 and REQ-INT-007 produced no draft at all, because every acceptance criterion on them was already cited. The metrics are proposals generated 14, accepted 8, rejected 4, duplicates 1, invalid 1, acceptance rate 0.57, which is 8/14. Among the 12 drafts a person reviewed, 8 were accepted, which is 0.67. Reviewer label: Lab reviewer.

### 50. What does the review gate check, and what would an external model still have to do?

`python tools/check_reviewed.py` ignores catalog files whose `source` is not `ai-draft`, which is how the original 60 M3 cases stay out of the gate. For an ai-draft case it requires a reviewer, a requirement ID that exists as a file, a `TC-(INT|VER|TRI)-nnn` ID matching the filename, and no duplicate. It fails if a proposal file was left at status `accepted`, and it requires every file under `proposals/rejected/` to be rejected, to carry `rejection_reason`, and to name a reviewer. Success prints `review gate passed`. The workflow runs that command after Python setup.

An external model, if one were ever added, would have to emit that same proposal shape and pass the same terminology and duplicate checks. A person would still accept or reject every file before it could enter `cases/`. The current release does not call a model. Accepted cases remain `not-executable` until a separate, explicit request promotes one into automation. The platform scope stops at M7.
