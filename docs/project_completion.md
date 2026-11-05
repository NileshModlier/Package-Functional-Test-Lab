# Project completion

**Project:** Package Functional Test Lab
**Identifier:** SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.
**Status:** M1 through M7 are complete in this repository. No further platform feature is in scope.

The workflows are study models from public documentation. The assumption register is the oracle. Vendor names identify the public sources. They are not a claim of employment, certification, partnership, or access to a vendor product.

## What each milestone delivered

| Milestone | Delivered |
| --- | --- |
| M1 | 27 requirements, three workflow notes, a test plan, a defect template, and the traceability strategy |
| M2 | Package Sim: learning, quality, and work orders, with six planted defect switches |
| M3 | 60 designed cases and the traceability matrix |
| M4 | 26 Playwright checks on Chromium, mapped to critical and high cases |
| M5 | Three Postman collections, Newman JUnit and JSON, and the API trace |
| M6 | GitHub Actions regression, summary table, and `trace/regression_status.md` |
| M7 | A review-gated drafter, eight accepted design cases, four stored rejections, and a CI review gate |

Local evidence for M6 is `reports/summary.md`: UI 26 tests and 0 failures, API 82 tests and 0 failures, with defects off. The GitHub workflow file is in the repository. It has not been executed on GitHub from this machine. M7 checked `python tools/check_reviewed.py` locally. That command printed `review gate passed`.

## Portfolio summary

This lab shows a functional-testing chain that stays inside one simulated product:

- Requirements with acceptance criteria and an assumption id when a public source is silent.
- A small FastAPI and Jinja application that implements those assumptions and can turn six known defects on.
- A YAML case catalog traced to requirement ids.
- Browser regression and API regression that pass with the defects off and fail the designated assertions with the defects on.
- A pipeline definition that publishes JUnit, Playwright traces, and Newman JSON, and that records the latest result beside each case.
- An assistant that may only propose a missing criterion, and only after a person accepts it does the idea become a non-executable case.

The eight M7 cases are design records. They are not new product behavior and they are not automated tests.

## Future roadmap

The platform stops here. Later work, if any, stays inside the same lab:

- Review the remaining uncited acceptance criteria with the same propose-and-review commands. Do not auto-accept them.
- Keep `tools/check_reviewed.py` in front of the suites so an unreviewed `ai-draft` case fails the build.
- If an external model is ever added, it must emit the same proposal shape and pass the same terminology and duplicate checks. A person still accepts or rejects every file before it can enter `cases/`.
- Leave the simulator rules, the Playwright tests, and the Postman collections as they are unless a reviewed case is later promoted to an automated check under a new, explicit request.

## Completion assessment

The M7 stop condition is met. The assistant reads requirements and cases, writes proposals only, rejects new terminology and duplicate titles, and requires a reviewer before a case exists. The CI gate enforces that rule for `source: ai-draft` cases. Measurements are in `proposals/metrics.yaml` and `docs/ai_assistant_evaluation.md`. No new simulator, automation, or reporting feature was added.
