# Case study

**Project:** Package Functional Test Lab
**Identifier:** SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.
**Span:** Milestones M1 through M7
**Audience:** QA leads, hiring managers, and SDET interviewers

## Background

Package programs publish enough process documentation for a tester to reconstruct a workflow and then discover that the reconstruction is larger than any one build. Learning material describes enrollment, delivery, issuance, and tracking. Quality material describes evaluation statuses, percentage scoring, acknowledgement, and a coaching session with its own lifecycle. Facilities material describes a TRIRIGA corrective-maintenance path and a Maximo status table, and those are different products.

This lab is a personal portfolio that studies those public sources and then tests a smaller simulated application, Package Sim, against an explicit assumption register. Vendor names identify the public sources. The lab does not claim employment, certification, partnership, or access to a vendor product.

The work was sequenced so each milestone could be reviewed on its own:

| Milestone | Question it answered |
| --- | --- |
| M1 | Can the rules be written so a later test has an oracle? |
| M2 | Can a small application implement those rules and also mis-implement six of them on purpose? |
| M3 | Can every requirement own at least one designed case? |
| M4 | Can the critical UI paths run unattended on Chromium? |
| M5 | Can the API paths, including boundary rows, run unattended in Newman? |
| M6 | Can one workflow definition run both suites and publish JUnit? |
| M7 | Can a drafter propose missing criteria and still be unable to put an unreviewed case in the catalog? |

## Challenges

**Public documents leave numbers and paths unspecified.** The pass mark, the quality weights, the hour bounds, and the enrollment URL the lab calls are simulated assumptions with IDs. A test that treated a public marketing page as a complete oracle would have invented the rest.

**The study model is wider than the simulator.** M1 quality notes describe an evaluation status and a coaching status. Package Sim keeps one `state`. M1 work notes split a service request from a work task and include `CAN`. Package Sim uses one record and does not implement `CAN`, `WSCH`, `WPCOND`, or `HISTEDIT`. Cases that meet the build record that difference in `known_sut_differences`. The expected result names the simulator state.

**Happy-path automation hides threshold bugs.** A suite that only submits 100 and 0 never shows whether 80.00 is a pass. The lab planted `pass_mark` so that exactly 80.00 fails while the switch is on, and wrote the boundary rows 79.99, 80.00, 80.01, 79.994, and 79.995 so half-up rounding is part of the evidence.

**Two reporters count different things.** Newman’s JUnit export has 82 tests. The JSON export has 138 assertions. Both files are from the defect-off run, and both have 0 failures. Publishing either number alone would mislead a reader who expects them to match.

**Generated tests can look grounded and still be the wrong case.** The drafter proposed `CAN` because REQ-TRI-002 contains that sentence. Terminology validation allowed it. Review rejected it because TC-TRI-004 already says rejecting a request to `CAN` is not a simulator state. Grounding in the requirement is necessary and was not sufficient.

**A defect flag left in the shell looks like a product bug.** `SIM_FORCE_DEFECTS=on` makes the UI fixture skip the turn-off click. The next “green” run then fails the six designated tests. The seed is doing what it was built to do.

**A review gate aimed at every YAML file would have failed the M3 catalog.** Those 60 files have no `source` field. The gate had to key off `source: ai-draft`.

## Design decisions

**One system under test, two clients.** FastAPI routes and Jinja pages call the same Python functions. Playwright drives the pages. Newman drives `/api/...`. `POST /test/reset` is the shared way back to `seed.json`, including the six switches defaulting to ON.

**Defects are switches, not random faults.** Each switch maps to one requirement: `pass_mark`, `certificate_date`, `quality_score`, `reopen_closed`, `invalid_completion`, `inactive_assignment`. The default suite turns the relevant switch OFF and asserts the M1 rule. A forced-on run asserts the same expectation and fails. `workflow_dispatch` input `force_defects` true is the pipeline form of that second run.

**Risk selects the first automation, and the catalog still holds the rest.** Thirteen requirements are High and fourteen are Medium. Playwright covers the critical and high browser paths that were chosen in M4: 26 tests. Many M3 cases remain `automation_intent: later-api` or manual. Their rows in `trace/regression_status.md` say Not run when no automation is wired. That is a visible gap, recorded on purpose.

**The assistant copies a criterion. It does not explore past the text.** Allowed techniques are boundary, negative, state-transition, decision-table, and exploratory. A draft that introduces a token absent from the requirement and its cases is invalid. A draft that repeats a title or a cited criterion is a duplicate. Accept always sets `automation_intent: not-executable`. The original 60 cases were not rewritten.

**The pipeline definition is in git, and the GitHub run is not claimed.** `.github/workflows/regression.yml` is the artifact for M6. Local checks produced `reports/summary.md` and a review gate line `review gate passed`. The workflow has not been executed on GitHub from this machine.

## Traceability strategy

`docs/traceability_strategy.md` (TRACE-001) fixes the chain:

```text
Requirement → Test case → Automation → CI result
```

Implemented IDs in `cases/` are `TC-INT-001` style. Acceptance criteria are cited inside the file, for example `REQ-INT-003 AC-2`. Automation IDs in `trace/regression_status.md` follow the case number and name the pytest function or the Newman request. A manual or exploratory case has no automation cell filled with a passing result.

Coverage states from the strategy still govern how the lab speaks: Specified, Planned, Written, Automated, Executed, Blocked. M1 left every requirement at Specified. M3 moved designed cases to Written. M4 and M5 moved the automated subset to Executed for the local defect-off run. M7 cases are Written design records. They are not Executed, and they are absent from the M6 regression-status file because that file was not regenerated.

Every one of the 27 requirements has at least one case. High-risk acceptance criteria were the depth target. Medium-risk requirements have coverage at the requirement level. `tools/ci_summary.py --check` fails the summary step when a requirement has no case, an automated test names a missing case, or a planted defect has no failing assertion wired to it.

## Automation strategy

UI automation is risk-based and narrow. Page objects expose actions. Tests assert state text, scores, and error visibility through `data-testid`. The suite is Chromium only. Twenty of the 26 tests do not touch a defect switch. Six of them are the detectors in `trace/defect_detection_matrix.md`.

API automation carries the boundary tables and the negative status codes. Learning uses five CSV iterations, quality three, and work orders four. Workflow folders run once, on iteration 0, so a five-row file does not enroll five full journeys. Negative checks expect 409, 422, or 404 and the simulator `detail` body. `tests/test_postman_contract.py` guards the collection shape so a regenerated JSON file can be diffed against the trace.

The two layers meet at port 18765 and at `POST /test/reset`. CI sets `SIM_EXTERNAL=1` so Playwright does not start a second server beside Newman.

## CI strategy

The job is one regression, not a deploy. Order is deliberate: review gate, then the server, then Playwright, then Newman, then the summary, then upload even when a test step failed. The review gate is a Python script with no extra packages, placed immediately after `actions/setup-python`. It prints `review gate passed` when every `ai-draft` case has a reviewer, a real requirement file, and a valid ID, and when no accepted draft is still sitting in `proposals/`.

`force_defects` true is an intentional red build. The expression in the workflow sets `SIM_FORCE_DEFECTS` to `on` only when the dispatch input equals `true`. Push, pull request, and the 20:30 UTC schedule leave it empty, so the ordinary design is a defect-off run. Reports upload on failure so a red demo still has JUnit, a simulator log, and Playwright traces.

Because this machine has not run the workflow on GitHub, the evidence a reader can open today is the workflow YAML plus the local `reports/` files. A green badge is not part of the story.

## AI review strategy

The drafter is deterministic. `propose` reads the prompt, then the selected requirements. It writes at most two uncited acceptance criteria per requirement. On the first requirement it also builds two contrast drafts: a copied title, counted as a duplicate, and a draft that says `biometric_signature`, counted as invalid. Those two are dropped and not written.

`review` is the only path into `cases/`. The command requires a path, `--decision accept|reject`, and `--reviewer`. The evaluation used `Lab reviewer`. Accept refuses to overwrite an existing case. Reject requires the reason to be stored on the file under `proposals/rejected/`.

The evaluation set was nine requirements. Two of them, REQ-INT-006 and REQ-INT-007, already cited every acceptance criterion and produced no draft. The other seven produced the files that became eight accepts and four rejects. Metrics: proposals generated 14, accepted 8, rejected 4, duplicates 1, invalid 1, acceptance rate 0.57. Among the 12 drafts a person reviewed, 8 were accepted, which is 0.67.

Human review is mandatory because a grounded sentence can describe behavior the simulator has already declined. The `CAN` rejection is the example used in interviews. Read-only scope and PATCH of a note were rejected because TC-INT-018 already records that they are not implemented. `started_at` was rejected because TC-TRI-009 already records that the field is not stored.

## Results

| Evidence | Figure | Condition |
| --- | --- | --- |
| Requirements | 27 | M1 inventory |
| Designed cases | 60, then 68 | M3 unchanged; M7 added 8 |
| Playwright JUnit | 26 tests, 0 failures, 0 errors, 0 skipped | Defects off, local, `reports/ui.xml` |
| Newman JUnit | 82 tests, 0 failures | Defects off, `reports/api.xml` |
| Newman JSON assertions | 138, 0 failed (53 + 37 + 48) | Same run, iterations preserved |
| Defect detectors | 6 switches | OFF passes the designated check; ON fails it |
| Review gate | Printed `review gate passed` | Local `python tools/check_reviewed.py` |
| Proposal acceptance | 0.57 generated, 0.67 of reviewed drafts | `proposals/metrics.yaml` |
| Non-UI pytest | 10 API tests; later combined run 24 passed | 6 assistant + 3 CI summary + 5 contract + 10 API |
| GitHub-hosted workflow run | None from this machine | File exists and was checked locally |

M7 did not re-run the full UI suite. The 26/0 figure stays the M4/M6 local report.

Worked quality example used throughout the lab, sections A 1/2, B 1/1, C 1/1: defect off scores 70.00 and Below standard; defect on scores 83.33 and Meets standard. Worked learning example: 80.00 is Passed when `pass_mark` is off and Failed when it is on.

## Lessons learned

The short form is in [LESSONS_LEARNED.md](LESSONS_LEARNED.md). The ones that changed the design are these.

- Clear `SIM_FORCE_DEFECTS` after a defect-on demo. The fixture treats that variable as an instruction to skip the toggle, and reset restores switches to ON.
- Publish both Newman counts and say why they differ. JUnit collapses iterations to one suite per request name.
- Let the reviewer reject a grounded draft. `CAN` is in the requirement and out of the simulator, and the catalog already says so.
- Scope the review gate to `source: ai-draft`. Applying it to every file in `cases/` would have failed the M3 catalog.
- Keep the assistant on requirement text and a human accept step. It does not call an external model, and an accepted case is still not an automated test.

## What a reader can defend in an interview

The lab shows a functional-testing chain with named rules, a system that can break those rules on purpose, evidence files with counts, and a gate that keeps unreviewed drafts out of the catalog. The lab also shows its limits in the same documents: simulated workflows, a workflow file that has not been executed on GitHub from this machine, and eight design cases that are not executable.
