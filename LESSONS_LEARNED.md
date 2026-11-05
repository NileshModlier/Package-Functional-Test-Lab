# Lessons learned

**Project:** Package Functional Test Lab
**Identifier:** SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.
**Span:** M1 through M7

These are the lessons the milestones actually produced. They are written so the next change to this lab repeats the check that caught them.

## A defect flag in the shell outlives the demo

`SIM_FORCE_DEFECTS` is read by the Playwright fixture, not by Package Sim. When the value is `on`, `DefectControls.set_enabled` returns immediately. The test still calls `POST /test/reset`, and reset reloads `seed.json`, where all six switches are true. The six designated tests then fail on the correct-behavior assertion.

That is the feature when the failure is intentional. It becomes a false alarm when the variable stays in the PowerShell process after the demo. The next `python -m pytest tests/ui` inherits it and looks like a regression of the pass mark, the certificate date, the quality weights, inactive assignment, invalid completion, or reopen.

The CI expression avoids leaving `on` behind on ordinary triggers. `SIM_FORCE_DEFECTS` is `on` only when `github.event.inputs.force_defects == 'true'`. Push, pull request, and the 20:30 UTC schedule have no dispatch input, so the value is empty, and empty is not `on`.

**Practice:** before a defect-off run, `Remove-Item Env:SIM_FORCE_DEFECTS`. After a forced-on demo, leave the stored `reports/ui.xml` and `reports/api.xml` as the defect-off evidence. `reports/README.md` says a manual `force_defects=true` run should not replace those files.

## JUnit tests and JSON assertions are both right

The defect-off Newman execution produced two honest counts.

| Report | Count | Why that count |
| --- | --- | --- |
| `reports/api.xml` | 82 tests, 0 failures | Newman’s JUnit reporter collapses iterations to one suite per request name |
| `reports/api.json` | 138 assertions, 0 failed | The JSON export keeps every CSV iteration |

The 138 splits by collection: learning 53 (5 iterations), quality 37 (3 iterations), work 48 (4 iterations). Learning’s five rows are 79.99, 80.00, 80.01, 79.994, and 79.995. A boundary failure that exists on only one of those rows is visible in the JSON and easy to miss if someone quotes only the JUnit total.

**Practice:** quote both numbers and name the reporter. `docs/postman.md` and `docs/api_defect_matrix.md` already do this. A summary table that shows 82 is the JUnit table in `reports/summary.md`. It is not a claim that only 82 assertions ran.

## A grounded draft can still be the wrong case

REQ-TRI-002 says an approver rejecting a `WAPPR` request with a reason sets status `CAN`. The drafter copied that sentence into `REQ-TRI-002-01`. Terminology validation passed, because `CAN` and `WAPPR` are in the requirement. Review rejected the draft. TC-TRI-004 already records that rejecting a request to `CAN` is not a simulator state. The rejection reason is on `proposals/rejected/REQ-TRI-002-01.yaml`. Reviewer: Lab reviewer.

The same pattern caught three more drafts.

| Proposal | Why review rejected it |
| --- | --- |
| REQ-INT-008-01 | TC-INT-018 already records that read-only scope is not implemented |
| REQ-INT-008-02 | TC-INT-018 already records that PATCH of a note is not implemented |
| REQ-TRI-005-02 | TC-TRI-009 already records that `started_at` is not stored |

The assistant is allowed to propose those sentences. The person is the one who knows the build has already written the difference down.

**Practice:** keep `known_sut_differences` on the M3 cases, and treat “the requirement says it” as the start of review, not the end.

## The review gate must leave the M3 catalog alone

`tools/check_reviewed.py` skips any case whose `source` field is not `ai-draft`. The 60 M3 files have no `source` field. They are Designed cases from before the assistant existed. A gate that required `reviewed_by` on every YAML file would have failed the build on the original catalog, which was the opposite of the M7 rule. The original 60 were not rewritten to add a source field.

The gate does check the eight accepted files. Each has `source: ai-draft`, `reviewed_by: "Lab reviewer"`, a real requirement ID, and a `TC-` ID that matches the filename. It also checks that nothing with status `accepted` is still sitting in `proposals/`, and that each file in `proposals/rejected/` has a reason and a reviewer. The local command printed `review gate passed`.

**Practice:** when a new control is added, name the population it applies to. Here the population is `source: ai-draft`, plus leftover proposal files. The control runs after Python setup and before the suites.

## The assistant does not call a model

`tools/ai_assistant.py` loads `tools/prompts/edge_cases.md`, then the requirement text and the cases that cite it. Surviving drafts copy one uncited acceptance-criterion sentence into the title, the step, and the expected result. The `why` line names the criterion ID. Contrast drafts on the first requirement exercise the duplicate and invalid counters: a copied title, and a draft that introduces `biometric_signature`. Those two are counted and not written.

There is no HTTP client to a model provider in that tool, and `sim/requirements.txt` has no model SDK. The evaluation numbers are the product of that deterministic pass over nine requirements: 14 generated, 8 accepted, 4 rejected, 1 duplicate, 1 invalid, acceptance rate 0.57. REQ-INT-006 and REQ-INT-007 produced no draft because every acceptance criterion was already cited.

Accepted output is a design record. `automation_intent` is `not-executable`. `execution.automated` is false. TC-INT-022 does not submit a score in the browser and does not add a Newman request.

**Practice:** if an external model is ever added, it has to emit the same proposal shape and pass the same terminology and duplicate checks. A person still accepts or rejects every file before it can enter `cases/`. That constraint is the roadmap, not a feature of this release.

## Other milestone lessons worth keeping

**Write the assumption when the source is silent.** The 80.00 inclusive threshold, half-up rounding, the 60/20/20 weights, the hour bounds, and rework from `COMP` to `INPRG` are lab choices with assumption IDs. Later tests cite the ID. They do not pretend the public page stated the number.

**Shrink the state model in writing.** Quality uses one state. A work order is one record. The workflow diagrams remain the study notes. `docs/package_sim.md` remains the integration map. Cases name the simulator state and the requirement together.

**Separate the certificate from the pass.** Passed and Completed are different enrollment states. The certificate is a record. `certificate_date` can be wrong while the learner is still correctly Completed, which is why that switch has its own detector on TC-INT-016.

**Reset is part of the test, not a courtesy.** Seed data and seed switches change whenever a previous test enrolls, scores, or assigns. `POST /test/reset` before each UI test, and at the start of each Newman iteration’s setup, is what makes 80.00 comparable across runs.

**Do not describe a local JUnit file as a GitHub check.** The workflow YAML is in the repository. The commands were exercised locally. This machine has not executed `.github/workflows/regression.yml` on GitHub. M7 also did not re-run the full 26-test UI suite. The 26/0 and 82/0 figures stay attributed to the stored defect-off reports.

**Quote the reviewed-draft rate beside the acceptance rate.** 8/14 is 0.57 and includes the duplicate and the invalid contrast drafts that no person accepted. 8/12 is 0.67 and is the rate among drafts a person actually reviewed. `proposals/metrics.yaml` stores the first rate. The evaluation note stores both.
