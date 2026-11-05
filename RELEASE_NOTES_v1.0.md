# Release notes v1.0

**Project:** Package Functional Test Lab
**Identifier:** SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.
**Version:** 1.0
**Date of the local M7 evaluation:** 2026-11-05
**Status:** M1 through M7 are complete in this repository. No further platform feature is in scope.

v1.0 is the portfolio snapshot of the lab after the review-gated drafter. Workflows are study models from publicly available documentation. The lab does not claim employment, certification, partnership, or access to Intellum, Verint, IBM TRIRIGA, or IBM Maximo.

The GitHub Actions workflow exists at `.github/workflows/regression.yml` and was verified locally. It has not been executed on GitHub from this machine. v1.0 does not include a green GitHub check run.

## M1 — Specification

Delivered the oracle the later milestones execute against.

- 27 requirements: REQ-INT-001–009 (9), REQ-VER-001–008 (8), REQ-TRI-001–010 (10). Thirteen High, fourteen Medium.
- Workflow notes: `docs/intellum_workflow.md`, `docs/verint_workflow.md`, `docs/tririga_workflow.md`.
- `plan/test-plan.md`, aligned in structure with ISO/IEC/IEEE 29119 ideas, and explicit that the plan is not a certification.
- Defect template `docs/defect_template.md`.
- Traceability strategy `docs/traceability_strategy.md`.
- Assumption IDs wherever a public source leaves a rule unspecified. Sample pass threshold `ASM-INT-06`: 80.00 percent, inclusive, half-up to two decimal places. Rework `ASM-TRI-08`: `COMP` back to `INPRG` when a reason is present.

M1 did not include a simulator. Requirement files were not rewritten in later milestones.

## M2 — Package Sim

Delivered a local FastAPI and Jinja2 application with an in-memory store and no database.

- Learning states: Enrolled → In Progress → Passed or Failed; Passed → Completed. Pass threshold 80.00 when `pass_mark` is off. Maximum 3 attempts.
- Quality states: Pending → Under Review → Acknowledged, Disputed, or Coached; Disputed → Under Review; Acknowledged or Coached → Completed. Weights A 60, B 20, C 20. Threshold 80. One state field on the evaluation.
- Work states: Draft → WAPPR → APPR → INPRG → COMP → CLOSE, with a WMATL branch. One record is both the request and the task. `CAN`, `WSCH`, `WPCOND`, and `HISTEDIT` are not simulator states.
- Seed: 5 learners, 5 evaluations, 10 work orders.
- Six planted defects, default ON: `pass_mark`, `certificate_date`, `quality_score`, `reopen_closed`, `invalid_completion`, `inactive_assignment`. `POST /test/reset` reloads `seed.json` and turns the switches back on.
- `tests/test_package_sim.py`: 10 tests. They verify the simulator. They are not the case catalog.

Every page carries the simulated banner. JSON responses carry `X-Simulated: true`.

## M3 — Case catalog

Delivered 60 designed YAML cases traced to requirement IDs and acceptance criteria, plus the traceability matrix. Those 60 files were not rewritten afterward. Automation intent on that catalog is `later-api`, `later-api-with-defect-switch`, or `manual-exploratory`. Execution results inside the case files stay `not-run` until a suite records a run elsewhere.

## M4 — Playwright

Delivered 26 Chromium UI tests under `tests/ui/`, with page objects and `data-testid` locators. Nine learning tests, eight quality tests, and nine work-order tests. Each test reloads the seed.

`reports/ui.xml`: 26 tests, 0 failures, 0 errors, 0 skipped. That file is the local defect-off run. The six detector tests were also run with `SIM_FORCE_DEFECTS=on` and failed on the correct-behavior assertion. The other 20 UI tests do not depend on a planted switch. M7 did not re-run this full suite.

## M5 — Postman and Newman

Delivered three collections (learning, quality, work orders), a local environment pointed at `http://127.0.0.1:18765`, and CSV boundary files.

- Pass-mark rows: 79.99, 80.00, 80.01, 79.994, 79.995. Half-up: 79.994 stores as 79.99 and fails; 79.995 stores as 80.00 and passes when `pass_mark` is off.
- Quality rows cover 79.99, 80.00, and 80.01. 80.00 meets standard when `quality_score` is off.
- Hour rows: 0 and 24.01 rejected; 0.01 and 24 stored; the order stays APPR.

`reports/api.xml`: 82 tests, 0 failures. `reports/api.json`: 138 assertions, 0 failed (learning 53, quality 37, work 48). JUnit collapses iterations to one suite per request name, so the two counts describe one defect-off execution. `--env-var forceDefects=true` skips Disable requests and the designated assertions fail. `tests/test_postman_contract.py` has 5 tests.

## M6 — GitHub Actions

Delivered `.github/workflows/regression.yml`.

- Triggers: `push`, `pull_request`, `workflow_dispatch`, `schedule` `30 20 * * *` (20:30 UTC).
- Manual input `force_defects`, default `false`. The value `true` sets `SIM_FORCE_DEFECTS=on` and Newman `--env-var forceDefects=true`. The job is designed to fail.
- Python 3.11, Node 20, Chromium, Uvicorn on `127.0.0.1:18765`, `GET /health`, `pytest tests/ui`, three Newman collections, `tools/ci_summary.py`.
- Artifacts: JUnit, Newman JSON, summary, regression status, simulator log, and Playwright failure traces.
- Local summary table: UI 26/0 and API 82/0.
- `tests/test_ci_summary.py`: 3 tests.

The workflow has not been executed on GitHub from this machine.

## M7 — Review-gated drafter

Delivered `tools/ai_assistant.py`, `tools/prompts/edge_cases.md`, `tools/check_reviewed.py`, and the review-gate step after Python setup in the workflow.

The drafter is deterministic. It loads the prompt and drafts from requirement and case text. It does not call an external model. It writes proposals only. Human review is mandatory. Techniques: `boundary`, `negative`, `state-transition`, `decision-table`, `exploratory`.

Evaluation requirements: REQ-INT-003, REQ-INT-006, REQ-INT-007, REQ-INT-008, REQ-TRI-002, REQ-TRI-005, REQ-TRI-006, REQ-VER-001, REQ-VER-006. REQ-INT-006 and REQ-INT-007 produced no draft because every acceptance criterion was already cited.

| Measure | Value |
| --- | --- |
| Proposals generated | 14 |
| Accepted | 8 |
| Rejected | 4 |
| Duplicates | 1 |
| Invalid | 1 |
| Acceptance rate | 0.57 |
| Reviewed-draft rate | 0.67 (8/12) |
| Reviewer | Lab reviewer |

Accepted cases, catalog total 68: TC-INT-022, TC-INT-023, TC-TRI-024, TC-TRI-025, TC-TRI-026, TC-VER-017, TC-VER-018, TC-VER-019. Each has `source: ai-draft`, `reviewed_by: "Lab reviewer"`, and `automation_intent: not-executable`.

Accepted example: TC-INT-022 / REQ-INT-003 AC-2, unanswered questions contribute 0 points.

Rejected example: REQ-TRI-002-01 expected `CAN`, rejected because existing cases record that `CAN` is not a simulator state. Also rejected: read-only scope and PATCH of a note, already recorded on TC-INT-018; `started_at`, already recorded on TC-TRI-009.

The duplicate and the invalid `biometric_signature` draft were counted and not written. A local run of `python tools/check_reviewed.py` printed `review gate passed`. The gate does not apply to M3 cases. M7 did not change simulator behavior, Playwright tests, or Postman collections, and it did not regenerate `trace/regression_status.md`.

A later combined pytest run of the non-UI modules passed 24 tests: 6 assistant, 3 CI summary, 5 Postman contract, and 10 API.

## Known limits in this release

- No license file is included.
- No GitHub-hosted execution of `regression.yml` from this machine.
- Eight accepted cases are design records. They are not executable tests.
- `trace/regression_status.md` is the M6 generation and does not list the eight M7 IDs.
- The full UI suite was not re-run during M7. Use `reports/ui.xml` for the 26/0 figure.
