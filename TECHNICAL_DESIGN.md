# Technical design

**Project:** Package Functional Test Lab
**Identifier:** SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.
**Status:** M7 complete. Simulator, Playwright, and Postman behavior are unchanged by the assistant.

This document is the implementation view. Narrative background is in [CASE_STUDY.md](CASE_STUDY.md). Interview answers are in [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md).

## Repository structure

```text
package-test-lab/
├── requirements/                 M1. 27 files, REQ-INT, REQ-VER, REQ-TRI
├── plan/test-plan.md             M1. Scope, techniques, risk, assumption register
├── docs/                         Workflow notes, simulator map, Postman, CI, assistant
├── sim/                          M2. app.py, learning.py, quality.py, workorders.py,
│                                 defects.py, models.py, seed.json, requirements.txt
├── cases/                        M3 catalog (60) plus M7 accepted cases (8)
├── proposals/metrics.yaml        M7 counts
├── proposals/rejected/           Four stored rejections
├── trace/                        Matrix, defect detection, M6 regression status
├── tests/test_package_sim.py    10 API checks against the simulator
├── tests/test_postman_contract.py
├── tests/test_ci_summary.py
├── tests/test_ai_assistant.py
├── tests/ui/                     26 Chromium tests and three page objects
├── postman/                      Collections, local environment, CSV, builder
├── tools/ci_summary.py
├── tools/ai_assistant.py         Regex reader and writer. No PyYAML. No model client
├── tools/check_reviewed.py
├── tools/prompts/edge_cases.md
├── .github/workflows/regression.yml
└── reports/                      Local defect-off JUnit, JSON, and summary
```

`sim/requirements.txt` lists FastAPI 0.162.0, Uvicorn 0.54.0, Jinja2 3.1.6, python-multipart 0.0.32, pytest 9.1.1, pytest-playwright 0.10.0, and httpx 0.28.1. Case files are parsed with regular expressions in `tools/ai_assistant.py`, `tools/check_reviewed.py`, and `tools/ci_summary.py`.

## Simulator design

Package Sim is a local FastAPI application. Jinja2 renders `/`, `/learning`, `/quality`, `/workorders`, and `/defects`. The same domain functions serve the JSON API. `sim/models.py` holds the store in memory. There is no database.

`POST /test/reset` reads `sim/seed.json` and replaces learners, enrollments, evaluations, work orders, certificates, and defect flags. `GET /health` returns status `ok`. Generated OpenAPI is at `/docs`. JSON responses include the header `X-Simulated: true`. Every HTML page shows:

SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.

### Learning

| From | Event | To | Guard |
| --- | --- | --- | --- |
| Available activity | Enroll | Enrolled | No other active enrollment for that learner and activity. Draft activities are rejected. |
| Enrolled | Start | In Progress | Content modules are marked complete. |
| In Progress | Assessment | Passed or Failed | Attempt count increases. The fourth attempt is rejected. |
| Failed | Reset | Enrolled | Attempts used is below 3. History is kept. |
| Passed | Complete | Completed | A certificate is issued when the activity is configured for one. |

Pass rule with `pass_mark` off: rounded score `>= 80.00`. Rounding is half-up to two decimal places. 79.995 is stored as 80.00. 79.994 is stored as 79.99. With `pass_mark` on, the comparison is exclusive: exactly 80.00 fails, and only a score greater than 80.00 passes.

Maximum attempts: 3. Seed activities include `ACT-102` (Available, used for new enrollments) and `ACT-103` (Draft). Learners are `LN-01` through `LN-05`.

### Quality

One state field. M1’s separate coaching machine is folded into this list, and the map is documented in `docs/package_sim.md`.

| From | Event | To |
| --- | --- | --- |
| Pending | Submit sections A, B, and C | Under Review |
| Under Review | Acknowledge | Acknowledged |
| Under Review | Dispute with a comment | Disputed |
| Under Review | Coach with a note | Coached |
| Disputed | Resolve | Under Review |
| Acknowledged | Coach with a note | Coached |
| Acknowledged | Complete | Completed |
| Coached | Acknowledge | Acknowledged |
| Coached | Complete | Completed |

Pending cannot jump to Acknowledged, Coached, or Completed. Disputed cannot complete until it returns to Under Review.

Score with `quality_score` off: section percent times weight, divided by 100. Weights A 60, B 20, C 20. Classification is `Meets standard` at 80.00 or above, otherwise `Below standard`. The learning `pass_mark` switch does not change this threshold. With `quality_score` on, the total is the unweighted mean of the three section percents.

Worked example, A 1/2, B 1/1, C 1/1:

| Switch | Total | Classification |
| --- | --- | --- |
| Off | 70.00 | Below standard |
| On | 83.33 | Meets standard |

Five seeded evaluations cover Pending, Under Review, Acknowledged, Disputed, and Coached.

### Work orders

One record travels the whole path. Request, approval, assignment, labor, materials, completion, and closure are fields and transitions on that record.

| From | To | Guard |
| --- | --- | --- |
| Draft | WAPPR | Required request fields are present. |
| WAPPR | APPR | `actor_id` is present and is not the requester. |
| APPR | INPRG | A technician is assigned. |
| APPR | WMATL | — |
| INPRG | WMATL | — |
| INPRG | COMP | — |
| WMATL | INPRG | — |
| COMP | CLOSE | — |
| COMP | INPRG | A rework reason is present. Actuals stay. `completed_at` is cleared. Assumption ASM-TRI-08. |

`INPRG` to `CLOSE` is rejected. `CLOSE` has no legal successor unless `reopen_closed` is on. Time and materials are accepted in `APPR`, `INPRG`, `WMATL`, and `COMP`. Hours must be greater than 0 and at most 24.00. Zero quantity material is rejected. `TEC-02` is the inactive technician. Ten seeded work orders cover Draft, WAPPR, APPR, INPRG, WMATL, COMP, and CLOSE.

`CAN`, `WSCH`, `WPCOND`, and `HISTEDIT` are not states in this simulator.

### HTTP results

| Situation | Status |
| --- | --- |
| Illegal workflow transition | 409, `detail` names the source and target |
| Missing or invalid field | 422 |
| Unknown ID | 404 |
| Accepted command | 200 |

## Defect switch design

Switches live in `sim/defects.py` and default to ON. Change one with `POST /api/defects/{id}` and `{"enabled": false}`. The defects page posts to `/ui/...` for the browser. `POST /test/reset` turns them all back on. A switch affects new decisions. Stored seed scores stay as they were.

| ID | ON | OFF | Detector |
| --- | --- | --- | --- |
| `pass_mark` | Score passes only when greater than 80.00 | Passes at 80.00 and above | UI `test_score_80_passes_when_pass_mark_defect_is_off`; Newman `TC-INT-008 Pass at 80.00` |
| `certificate_date` | `issued_on` is one day before `completion_date` | The two dates are the same day | UI `test_certificate_issued_date_matches_completion`; Newman `TC-INT-016 Read the certificate dates` |
| `quality_score` | Unweighted mean | Weights 60 / 20 / 20 | UI `test_weighted_sections_score_70`; Newman `TC-VER-005 Score weighted sections as 70` |
| `inactive_assignment` | `TEC-02` can be assigned | That assignment returns 409 | UI `test_inactive_technician_is_rejected`; Newman `TC-TRI-008 Reject an inactive technician` |
| `invalid_completion` | `APPR` to `COMP` is accepted | `COMP` is accepted only from `INPRG` | UI `test_approved_order_cannot_complete`; Newman `TC-TRI-017 Reject completion from APPR` |
| `reopen_closed` | `CLOSE` to `INPRG` is accepted and `reopened` becomes true | That transition returns 409 | UI `test_closed_order_stays_closed`; Newman `TC-TRI-021 Reject reopen of a closed order` |

`invalid_completion` does not allow `INPRG` to `CLOSE`. `inactive_assignment` does not allow assignment onto a closed order.

Two clients honor a force flag, and they honor it differently.

| Client | Flag | Effect |
| --- | --- | --- |
| Playwright fixture | Process environment `SIM_FORCE_DEFECTS=on` | `DefectControls.set_enabled` returns without clicking. Reset has already restored ON. |
| Newman | `--env-var forceDefects=true` | Setup requests that disable switches are skipped. |
| GitHub Actions | `workflow_dispatch` input `force_defects` equal to `true` | Sets `SIM_FORCE_DEFECTS=on` and adds the Newman env var. The job is designed to fail. |

On `push`, `pull_request`, and `schedule`, the workflow expression sets `SIM_FORCE_DEFECTS` to an empty string because the dispatch input is absent. Empty is not `on`.

A local PowerShell session that still has `SIM_FORCE_DEFECTS` set will leak that mode into the next `pytest tests/ui` process. The simulator process itself does not read the variable. The leak is in the test runner. Clear it with `Remove-Item Env:SIM_FORCE_DEFECTS` before a defect-off run.

## Traceability matrix

The strategy document defines columns for requirement, acceptance criterion, assumption IDs, risk, test case, technique, automation ID, CI result, and defect IDs. The catalog implements case IDs as `TC-INT-001`, `TC-VER-001`, and `TC-TRI-001` through the M7 additions. Criterion citations inside a case look like `REQ-INT-003 AC-2`.

`trace/regression_status.md` is one row per requirement and case pair that M6 knew about. The Automation cell names `AUTO-…` plus the pytest function, the Newman request, or both. Last Result is Pass or Not run. The file’s header says it was generated from `reports/ui.xml` and `reports/api.xml`.

M7 cases are not in that file. `docs/ai_assistant.md` states that the next CI run is what would add them as Not run, and that M7 did not regenerate the file and did not execute the workflow on GitHub.

`tools/ci_summary.py --check` is the mechanical form of the strategy’s orphan rules: every requirement has a case, every automated test names a real case, and every planted defect is wired to an assertion.

## UI automation framework

pytest-playwright drives Chromium. `tests/ui/conftest.py` registers markers `smoke`, `regression`, and `critical`, forces `browser_name` to chromium, and autouses `reset_sim`.

Page objects wrap `data-testid` locators. Examples from the learning page: `enroll-learner`, `enroll-activity`, `enroll-submit`, `enrollment-{id}`, `start`, `score`, `score-submit`, `complete`. Tests call the page object, and the selectors stay in that class.

A defect-aware test asks the `defects` fixture to disable one switch, then performs the business action and asserts the M1 outcome. With the environment flag off, the fixture opens `/defects`, clicks Turn off when that is the current action, and expects the state text OFF.

CI invokes:

```text
python -m pytest tests/ui --junitxml=reports/ui.xml --tracing=retain-on-failure --screenshot=only-on-failure --video=retain-on-failure --output=test-results
```

Local defect-off evidence: 26 tests, 0 failures, 0 errors, 0 skipped. The full UI suite was not re-run as part of M7.

## API automation framework

Each collection has three folders.

1. **Setup.** `GET /health`, `POST /test/reset`, then disable the switches that workflow cares about. Disable requests are skipped when `forceDefects` is `true`.
2. **Workflow.** Runs on iteration 0. Later CSV iterations skip it. IDs travel in collection variables such as `enrollmentId`, `evalDisputeId`, and `newOrderId`.
3. **Boundaries.** Run on every CSV row. The folder is skipped when Newman starts without a data file.

Environment values override collection values. `baseUrl` is `http://127.0.0.1:18765`.

| CSV | Rows | Rule with the matching switch OFF |
| --- | --- | --- |
| `pass_mark_boundaries.csv` | 79.99, 80.00, 80.01, 79.994, 79.995 | 79.994 fails as 79.99. 79.995 and 80.00 pass. 80.01 passes. |
| `quality_boundaries.csv` | Section points for 79.99, 80.00, 80.01 | 80.00 meets standard. |
| `work_hours_boundaries.csv` | 0, 0.01, 24, 24.01 | 0 and 24.01 are rejected. 0.01 and 24 are stored. The order stays APPR. |

Negative examples, all asserted against `detail` and the status code: duplicate active enrollment 409, unpublished activity 409, assessment before start 409, unknown enrollment or interaction 404, missing quality section 422, empty dispute 422, blank request title 422, rework without a reason 422, hours out of range 422, zero material 422, self-approval 409, inactive technician 409, start without a technician 409, `INPRG` to `CLOSE` 409, `WMATL` to `COMP` 409, `APPR` to `COMP` 409, `CLOSE` to `INPRG` 409, time on a closed order 409.

Commands are the three `npx newman run` lines in `docs/postman.md`. The milestone combined them into `reports/api.xml` (82 tests, 0 failures) and `reports/api.json` (138 assertions, 0 failed: learning 53 on 5 iterations, quality 37 on 3 iterations, work 48 on 4 iterations). JUnit collapses iterations to one suite per request name, which is why 82 and 138 describe the same defect-off execution.

`postman/build_collections.py` regenerates the JSON, the environment, the CSV files, and the request rows in `docs/api_traceability.md`. Contract tests lock the boundary values and the “every request is listed” rule.

## Review workflow

```text
requirements/*.md
cases/*.yaml
        |
        v
tools/prompts/edge_cases.md
        |
        v
tools/ai_assistant.py propose --requirements REQ-...
        |
        ├── invalid or duplicate → counted, not written
        └── proposals/REQ-XXX-NN.yaml   status: proposed, reviewed_by: null
                    |
                    v
        python tools/ai_assistant.py review <file> --decision accept|reject --reviewer "Lab reviewer"
              ├── accept → new cases/TC-*.yaml, proposal deleted
              └── reject → proposals/rejected/, rejection_reason stored
                    |
                    v
        python tools/check_reviewed.py
```

`propose` requires 8 to 10 requirement IDs. It drafts at most two acceptance criteria that no case cites. The first requirement also receives the two contrast drafts.

| Check | Rule | Metric |
| --- | --- | --- |
| Schema | `source` is `ai-draft`, `status` is `proposed`, `reviewed_by` is null, technique is one of the five names, requirement id matches `REQ-INT`, `REQ-VER`, or `REQ-TRI`, and title, steps, expected, and why are present | `invalid` |
| Terminology | Backtick phrases, short all-caps tokens, numbers, and snake_case names must already appear in the requirement or in a case for that requirement | `invalid` |
| Duplicate | The criterion id is already cited, or the normalized title matches an existing case for that requirement | `duplicate` |

The prompt file must name `boundary`, `negative`, `state-transition`, `decision-table`, `exploratory`, and `reviewed_by`. The drafter copies one acceptance-criterion sentence into the title, the step, and the expected result. The `why` line names the criterion and says no existing case cites it.

Accept writes `automation_intent: not-executable` and `execution.automated: false`, keeps `source: ai-draft`, and sets `reviewed_by`. The tool will not overwrite an existing case file. Only a file still in `status: proposed` can be reviewed. The eight accepted proposals are gone from `proposals/` because accept deletes them. Re-running accept against `cases/TC-INT-022.yaml` is not a supported path.

`check_reviewed.py` walks `cases/TC-*.yaml` and continues past any file whose `source` is not `ai-draft`. For an ai-draft file it requires a reviewer other than null, at least one requirement ID that matches `REQ-(INT|VER|TRI)-nnn` and exists on disk, a case ID matching `TC-(INT|VER|TRI)-nnn` equal to the filename, and no duplicate ID. It then checks `proposals/*.yaml` (except `metrics.yaml`) for a status of `proposed` or `rejected`, and flags an `accepted` file left behind. Files in `proposals/rejected/` must be `rejected`, must have `rejection_reason`, and must have a reviewer. Success prints `review gate passed` and returns 0.

The gate runs in GitHub Actions after Python setup and before Node, the suites, and the summary. It does not draft proposals and it does not change the simulator.

### Evaluation outcome

Requirements in the local run on 2026-11-05: REQ-INT-003, REQ-INT-006, REQ-INT-007, REQ-INT-008, REQ-TRI-002, REQ-TRI-005, REQ-TRI-006, REQ-VER-001, REQ-VER-006.

REQ-INT-006 and REQ-INT-007 produced no draft. Every acceptance criterion on those two files was already cited.

| Measure | Value |
| --- | --- |
| proposals_generated | 14 |
| accepted | 8 |
| rejected | 4 |
| duplicates | 1 |
| invalid | 1 |
| acceptance_rate | 0.57 |

Reviewed-draft rate: 8 / 12 = 0.67. Reviewer: Lab reviewer.

Accepted example: TC-INT-022 from REQ-INT-003-01, technique exploratory, criterion AC-2.

Rejected example: REQ-TRI-002-01, technique state-transition, expected `CAN`. Rejection reason stored on the file: existing cases already record that `CAN` is not a simulator state. REQ-INT-008-01 and REQ-INT-008-02 were rejected because TC-INT-018 already records that read-only scope and PATCH of a note are not implemented. REQ-TRI-005-02 was rejected because TC-TRI-009 already records that `started_at` is not stored.

The duplicate was a restatement of the first REQ-INT-003 case title. The invalid draft introduced `biometric_signature`. Neither file was written.
