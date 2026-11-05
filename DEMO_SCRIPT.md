# Demo script

**Project:** Package Functional Test Lab
**Length:** 5 minutes
**Identifier to say out loud:** SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.
**Shell:** Windows PowerShell, lab root `package-test-lab`
**Chain commands with `;`.** PowerShell does not use `&&` in the blocks below.

Say once, at the start: this is a personal portfolio lab. The workflows are study models from public documentation. The lab does not claim employment, certification, partnership, or access to Intellum, Verint, IBM TRIRIGA, or IBM Maximo.

Before you begin, clear a leftover defect flag so the green run stays green:

```powershell
Remove-Item Env:SIM_FORCE_DEFECTS -ErrorAction SilentlyContinue
```

| Beat | Clock | What the audience sees |
| --- | --- | --- |
| 1 Requirements | 0:00–0:35 | 27 testable rules |
| 2 Traceability matrix | 0:35–1:10 | Requirement to case to automation to result |
| 3 Playwright | 1:10–2:10 | 26 Chromium tests |
| 4 Newman | 2:10–3:20 | Three collections, then the 82 and 138 counts |
| 5 Defect injection | 3:20–3:55 | One switch left ON fails the M1 assertion |
| 6 Failing pipeline | 3:55–4:25 | `force_defects` in the workflow file |
| 7 AI proposal review | 4:25–5:00 | Accepted case, rejected `CAN` draft, review gate |

Pytest in beat 3 starts Package Sim on port 18765 and stops it when the session ends. Start the server for Newman only after that session has exited. If port 18765 is already taken, stop the other process before beat 3.

## 1. Requirements (0:00–0:35)

Open the inventory.

```powershell
Get-Content requirements\README.md -TotalCount 40
```

Say: twenty-seven requirements. Nine learning, eight quality, ten work. Each file has a public source, a simulated assumption where that source is silent, and acceptance criteria. High-risk rows are the ones that grant or withhold a pass, a certificate, a quality outcome, an acknowledgement, or a closure. The pass rule you will demo is in REQ-INT-004: with the planted switch off, 80.00 is a pass, and the score is half-up to two decimals.

## 2. Traceability matrix (0:35–1:10)

```powershell
Get-Content trace\regression_status.md -TotalCount 20
```

Say: one row ties a requirement to a case, to an automation ID, to the last local result. `TC-INT-008` is the 80.00 pass, automated by a Playwright test and by a Newman request, last result Pass on the defect-off reports. Scroll once to a `Not run` row so the gap is visible. The eight M7 design cases are not in this file. M7 did not regenerate it. Their `automation_intent` is `not-executable`.

## 3. Playwright run (1:10–2:10)

Confirm the defect flag is clear, then run the UI suite. The stored `reports/ui.xml` already records 26 tests, 0 failures, 0 errors, 0 skipped. This command refreshes that file. It takes about half a minute of test time plus startup, which fits this beat if the audience watches the node names.

```powershell
Remove-Item Env:SIM_FORCE_DEFECTS -ErrorAction SilentlyContinue ; python -m pytest tests/ui --junitxml=reports/ui.xml
```

Say: Chromium only, page objects, `data-testid` locators. Every test posts `POST /test/reset` first, so the seed is 5 learners, 5 evaluations, and 10 work orders, and the six switches are back ON until a test turns one off. Twenty tests never touch a switch. Six tests turn their switch off and assert the written rule. This milestone’s full UI suite is this command. M7 did not re-run it as part of the assistant work. The 26/0 result the portfolio quotes is the defect-off JUnit file.

If the clock is behind, point at the existing `reports/ui.xml` header (`tests="26" failures="0"`) and move on. Do not start Newman until pytest has exited and released port 18765.

## 4. Newman run (2:10–3:20)

Start Package Sim, then run the three commands from `docs/postman.md`. Use a second window for Uvicorn, or start it in the background and continue.

Window A:

```powershell
python -m uvicorn sim.app:app --host 127.0.0.1 --port 18765
```

Window B, after `GET /health` would succeed:

```powershell
npx newman run postman/collections/learning.postman_collection.json -e postman/environments/local.postman_environment.json -d postman/data/pass_mark_boundaries.csv --reporters cli,junit,json --reporter-junit-export reports/learning.xml --reporter-json-export reports/learning.json ; npx newman run postman/collections/quality.postman_collection.json -e postman/environments/local.postman_environment.json -d postman/data/quality_boundaries.csv --reporters cli,junit,json --reporter-junit-export reports/quality.xml --reporter-json-export reports/quality.json ; npx newman run postman/collections/workorders.postman_collection.json -e postman/environments/local.postman_environment.json -d postman/data/work_hours_boundaries.csv --reporters cli,junit,json --reporter-junit-export reports/workorders.xml --reporter-json-export reports/workorders.json
```

Say: Setup resets the seed and turns this collection’s switches OFF. Workflow runs on iteration 0. Boundaries run on every CSV row. Learning rows are 79.99, 80.00, 80.01, 79.994, and 79.995. 79.995 half-up rounds to 80.00 and passes when `pass_mark` is off. 79.994 rounds to 79.99 and fails.

The combined defect-off evidence already in the repo is `reports/api.xml` with 82 tests and 0 failures, and `reports/api.json` with 138 assertions and 0 failed: learning 53, quality 37, work 48. JUnit collapses iterations to one suite per request name. Both counts are from that same kind of run. If the three commands overrun the beat, stop after the learning collection and show `reports/summary.md` for the stored 82.

## 5. Defect injection (3:20–3:55)

Show the detector table, then force a single known failure. The fixture skips the turn-off click when `SIM_FORCE_DEFECTS` is `on`. Reset leaves `pass_mark` on, so exactly 80.00 is Failed. That failure is the point.

```powershell
Get-Content trace\defect_detection_matrix.md -TotalCount 20 ; $env:SIM_FORCE_DEFECTS = "on" ; python -m pytest tests/ui/test_learning.py::test_score_80_passes_when_pass_mark_defect_is_off --junitxml=reports\demo-defect-ui.xml ; Remove-Item Env:SIM_FORCE_DEFECTS
```

Say: six switches default to ON in `seed.json`: `pass_mark`, `certificate_date`, `quality_score`, `reopen_closed`, `invalid_completion`, `inactive_assignment`. `POST /test/reset` reloads that seed. `POST /api/defects/pass_mark` with `{"enabled": false}` is how a single switch is turned off during the green suite. With the flag on, this test expects Passed at 80.00 and observes Failed.

The JUnit path above is `reports/demo-defect-ui.xml` so the green `reports/ui.xml` stays the defect-off portfolio file. Clear the environment variable before you take another question. A shell that keeps `SIM_FORCE_DEFECTS=on` will fail the next green run for the same reason.

Stop the Uvicorn window if it is still holding port 18765 before this pytest, or the fixture cannot bind. The API twin of this demo is the documented Newman flag `--env-var forceDefects=true` on the learning command from beat 4. You do not need both in a five-minute slot.

## 6. Failing pipeline (3:55–4:25)

Open the workflow. Do not claim it has run on GitHub.

```powershell
Get-Content .github\workflows\regression.yml -TotalCount 40
```

Say: the file is `.github/workflows/regression.yml`. Triggers are push, pull_request, workflow_dispatch, and cron `30 20 * * *`, which is 20:30 UTC. The manual input `force_defects` defaults to false. True sets `SIM_FORCE_DEFECTS` to `on` for pytest and passes `--env-var forceDefects=true` to Newman. Disable steps are skipped. The same assertions fail, and the job is designed to fail. That red result is the signal that the switches still break the M1 rules.

The review gate, `python tools/check_reviewed.py`, runs after Python 3.11 setup and before the suites. A local run printed `review gate passed`. The workflow was verified locally. It has not been executed on GitHub from this machine. There is no green GitHub check to show.

## 7. AI proposal review (4:25–5:00)

Show one accepted design case, one stored rejection, the review command the milestone used, and the gate.

```powershell
Get-Content cases\TC-INT-022.yaml ; Get-Content proposals\rejected\REQ-TRI-002-01.yaml ; python tools/ai_assistant.py review --help ; python tools/check_reviewed.py
```

Say: the assistant loads `tools/prompts/edge_cases.md` and drafts from the requirement and the cases that cite it. It does not call an external model. It writes proposals only. A person accepts or rejects. Techniques are boundary, negative, state-transition, decision-table, and exploratory.

`TC-INT-022` is the accepted example. Requirement REQ-INT-003, criterion AC-2: unanswered questions contribute 0 points and still count in the possible points. `reviewed_by` is Lab reviewer. `automation_intent` is `not-executable`. It is not a Playwright test.

`REQ-TRI-002-01` expected status `CAN`. The sentence is in the requirement, so the terminology check allowed it. Review rejected it because existing cases record that `CAN` is not a simulator state.

The accept command, already used for the eight cases, is:

```powershell
python tools/ai_assistant.py review proposals\REQ-INT-003-01.yaml --decision accept --reviewer "Lab reviewer"
```

There is no `status: proposed` file left to accept. Accept deletes the proposal, and review refuses anything that is not still proposed. `--help` shows the real arguments: a path, `--decision accept` or `reject`, and `--reviewer`. `python tools/check_reviewed.py` is the command to run live. It prints `review gate passed`. The gate applies to `source: ai-draft` only. The original 60 M3 cases have no `source` field and are left alone.

Close on the metrics: 14 proposals generated, 8 accepted, 4 rejected, 1 duplicate, 1 invalid, acceptance rate 0.57. Of the 12 drafts a person reviewed, 8 were accepted, which is 0.67. Catalog total 68. The platform stops at M7.

## If a beat slips

| Priority | Keep | Drop first |
| --- | --- | --- |
| Must say | Disclaimer, 27 requirements, 26 and 82 and 138, six switches, `force_defects` not run on GitHub, assistant writes proposals only | A second Newman collection |
| Must run | `python tools/check_reviewed.py` and either pytest or one Newman collection | The single-test defect failure, if you already showed the matrix |

Stored files you can open without rerunning: `reports/summary.md`, `reports/ui.xml`, `reports/api.xml`, `proposals/metrics.yaml`, `docs/project_completion.md`.
