# Roadmap

**Project:** Package Functional Test Lab
**Identifier:** SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.
**Status:** The platform is complete after M7. No further platform feature is in scope.

This page lists work that could still happen inside the same lab. It does not propose a new product, a vendor connector, or a hosted service.

## Where the lab stands

| Milestone | State |
| --- | --- |
| M1 Requirements, workflows, test plan, defect template, traceability strategy | Approved and left in place |
| M2 Package Sim and six planted defect switches | Complete |
| M3 60 designed cases | Complete. Those files were not rewritten |
| M4 26 Chromium UI tests | Complete. Local defect-off JUnit is 26 tests, 0 failures |
| M5 Postman and Newman | Complete. JUnit 82 tests, 0 failures. JSON 138 assertions, 0 failed |
| M6 GitHub Actions workflow | File complete and verified locally. Not executed on GitHub from this machine |
| M7 Review-gated drafter, 8 accepted design cases, 4 stored rejections | Complete. Catalog total 68 |

Accepted M7 cases have `automation_intent: not-executable`. They are not simulator changes and they are not automated tests.

## Work that stays inside the lab

**Review the remaining uncited acceptance criteria with the same human gate.** `python tools/ai_assistant.py propose` still requires 8 to 10 requirement IDs and still writes proposals only. A person runs `review` with `--decision accept` or `--decision reject` and `--reviewer`. Nothing in that flow auto-accepts. REQ-INT-006 and REQ-INT-007 already showed the empty result: when every criterion is cited, the drafter writes nothing.

**Keep `tools/check_reviewed.py` in front of the suites.** The workflow step stays after Python setup. It continues to ignore M3 files that have no `source` field, and it continues to fail an `ai-draft` case that has no reviewer, no requirement, no source, or an invalid ID. The success line remains `review gate passed`.

**If an external model is ever added, constrain it to the current proposal shape.** It would have to emit `source: ai-draft`, a technique from `boundary`, `negative`, `state-transition`, `decision-table`, and `exploratory`, and the same title, steps, expected, and why fields. It would still have to pass the terminology check and the duplicate check. A person would still accept or reject every file before it could enter `cases/`. The current tool does not call an external model. Adding one is future work, not a capability of v1.0.

**Leave the running tests alone unless a reviewed case is promoted on purpose.** Simulator rules, the Playwright tests, and the Postman collections stay as they are unless a later, explicit request promotes a reviewed case into an automated check. Promotion would be a new milestone with its own evidence. It is not implied by an accepted design case.

**Regenerate regression status only by running the summary tool.** The eight M7 IDs are absent from `trace/regression_status.md`. The assistant note says the next CI run is what would add them as Not run. That regeneration has not been done, and the workflow has not been executed on GitHub from this machine. A future local run of `tools/ci_summary.py` can refresh the file when someone intends to refresh the evidence. Until then, the M6 file remains the historical result of the 26 and 82 test reports.

## Explicitly unchanged

- The six defect switches, their default ON seed, and `POST /test/reset`
- The 26 Chromium tests and the three Newman collections
- The original 60 case files
- The claim boundary: study models from public documentation, with no assertion of employment, certification, partnership, or access to Intellum, Verint, IBM TRIRIGA, or IBM Maximo

## How to tell that v1.0 is still the current release

`docs/project_completion.md` states the stop condition. `proposals/metrics.yaml` still reads 14, 8, 4, 1, 1, and 0.57. `python tools/check_reviewed.py` still prints `review gate passed` on this tree. Any future accept would add a case file and change those measurements, and the roadmap above is the process for doing that inside the lab.
