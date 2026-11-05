# CI

**Milestone:** M6
**Identifier:** SIMULATED

GitHub Actions runs the Playwright and Newman regression against Package Sim. This is not a vendor pipeline. The review gate checks accepted AI drafts before the suites run. It does not draft proposals and it does not change the simulator.

## Pipeline architecture

Workflow: `.github/workflows/regression.yml`

| Trigger | When |
| --- | --- |
| push | Every push |
| pull_request | Every pull request |
| schedule | 20:30 UTC nightly (`30 20 * * *`) |
| workflow_dispatch | Manual run |

The manual run has one input, `force_defects`. `false` is the normal regression. `true` leaves the six planted switches ON. The same assertions then fail, and the job fails on purpose.

```text
Checkout
  → Python 3.11
  → python tools/check_reviewed.py
  → Node 20
  → pip install -r sim/requirements.txt and npm install -g newman
  → playwright install --with-deps chromium
  → uvicorn sim.app:app on 127.0.0.1:18765
  → GET /health
  → pytest tests/ui
  → newman run, three collections
  → python tools/ci_summary.py
  → upload artifacts
```

`SIM_EXTERNAL=1` tells the UI fixtures to use the server the workflow started instead of launching a second one. Newman uses that same server. `POST /test/reset` still runs before each UI test and at the start of each Newman iteration.

## Artifacts

The `regression-reports` artifact contains:

| File | Contents |
| --- | --- |
| `reports/ui.xml` | Playwright JUnit |
| `reports/api.xml` | Newman JUnit, three collections combined |
| `reports/api.json` | Newman JSON export |
| `reports/summary.md` | Result table |
| `trace/regression_status.md` | Requirement, test case, automation, last result |
| `test-results/` | Playwright traces, screenshots, and videos kept on failure |
| `reports/sim.log` | Simulator log |

Traces, screenshots, and videos are recorded only when a Playwright test fails.

## Execution flow

1. The simulator starts in its own session so it stays up after the start step ends.
2. Health is polled for up to 60 seconds.
3. Playwright runs Chromium only and writes `reports/ui.xml`.
4. Newman runs learning, quality, and work orders. Each collection loads `local.postman_environment.json` and its CSV boundary file.
5. `tools/ci_summary.py` merges the Newman JUnit and JSON, writes the summary, writes the regression status, and appends the summary to `GITHUB_STEP_SUMMARY`.
6. The summary step also checks that every requirement has a case, every automated test names a real case, and every planted defect is wired to a failing assertion.
7. Reports upload even when a test step failed. The server is stopped at the end.

With `force_defects=true`, pytest sees `SIM_FORCE_DEFECTS=on` and Newman receives `--env-var forceDefects=true`. Disable steps are skipped. The assertions of the M1 rules fail.

## Failure investigation

| What failed | Where to look |
| --- | --- |
| Health check | `reports/sim.log` |
| Playwright assertion | `reports/ui.xml`, then `test-results/` for the trace and screenshot |
| Newman assertion | `reports/api.xml` and `reports/api.json` |
| Summary table | `reports/summary.md` and the job summary on the Actions run |
| A requirement or test id with no owner | The check output from `tools/ci_summary.py --check` |
| Manual defect demo | Confirm the run input was `force_defects=true`. Those failures are the signal that the switches still break the M1 rule. |

A green summary is:

```text
| Result | Report | Tests | Failures | Errors | Skipped |
| --- | --- | --- | --- | --- | --- |
| Pass | reports/ui.xml | 26 | 0 | 0 | 0 |
| Pass | reports/api.xml | 82 | 0 | 0 | 0 |
```

The counts come from the JUnit files of the run. Re-run a single collection locally with the Newman command in `docs/postman.md` before changing a workflow assertion.
