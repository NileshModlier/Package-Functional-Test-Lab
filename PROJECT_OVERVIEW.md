# Project overview

**Project:** Package Functional Test Lab
**Identifier:** SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.
**Status:** M1 through M7 are complete in this repository. The platform stops here.

This document is the orientation for someone meeting the lab for the first time. It is a study lab and a personal portfolio. It is not a product, a vendor connector, or a customer implementation.

## Problem statement

Enterprise functional testing fails quietly when the specification, the cases, the automation, and the pipeline result are four separate piles. A score of 80 can pass in a requirement and fail in a build. A status name from a public manual can be copied into a test that the running system will never reach. A generated test idea can land in the suite before anyone has decided it belongs there.

The practical problem this lab takes on is the chain itself:

- Write a rule that a tester can observe.
- Record the assumption when the public source is silent.
- Design a case that cites the rule.
- Execute the critical cases in a browser and through an API.
- Leave a known defect switch in the build so a regression can prove it still detects the break.
- Keep a machine-written draft out of the catalog until a person accepts it.

## Business context

Large package programs test workflows that already have public process documentation: enrollment through a certificate, an interaction evaluation through coaching, and a facilities request through closure. The business outcome is easy to state and expensive to get wrong. A learner is marked passed. An evaluation meets a standard. A work order closes. Each of those outcomes depends on a threshold, a legal transition, and a record that later steps can read.

Teams that test those workflows need a shared vocabulary. Requirements carry IDs. Cases cite acceptance criteria. Automation IDs point at one case. A pipeline result names the run. When a public document and the system under test disagree, the disagreement is written down in the case and the simulator map.

This repository practices that vocabulary on study models. The workflows come from publicly available documentation about Intellum-style learning, Verint-style quality management, and IBM TRIRIGA and IBM Maximo facilities work. The lab does not claim employment, certification, partnership, or access to those products.

## Why enterprise functional testing matters

Functional testing at this scale is how an organization shows that a business rule survived the trip from a document into a running path.

- A pass mark that is exclusive at the written threshold issues a failure to someone who met the rule, or a pass to someone who missed it.
- A certificate date that drifts from the completion date breaks the audit trail of the credential.
- An unweighted quality score can classify the same form as meeting the standard when the weighted rule says it does not.
- An inactive technician, a completion from the wrong status, or a reopen of closed work changes who is allowed to finish a facilities job.

Those are functional defects. They show up as the wrong state, the wrong number, or the wrong HTTP result. Boundary values, state transitions, and decision tables are the techniques that find them before a later suite only checks the happy path.

Traceability matters for the same reason. A green run that cannot name its requirement is a run nobody can audit. A requirement with no case is a rule nobody has agreed how to demonstrate.

## How this lab addresses it

The lab keeps the whole chain in one repository and labels every layer simulated.

| Need | What the lab contains |
| --- | --- |
| Testable rules | 27 requirements, REQ-INT-001–009, REQ-VER-001–008, REQ-TRI-001–010, each with acceptance criteria and assumption IDs where the public source is silent |
| A place to execute | Package Sim: FastAPI and Jinja2, in-memory seed, 5 learners, 5 evaluations, 10 work orders |
| Designed coverage | 60 YAML cases from M3, left as written, plus 8 accepted M7 design cases. Catalog total 68 |
| Repeatable UI evidence | 26 Chromium tests. `reports/ui.xml`: 26 tests, 0 failures, 0 errors, 0 skipped, defects off |
| Repeatable API evidence | Three Postman collections. JUnit `reports/api.xml`: 82 tests, 0 failures. JSON assertions: 138, 0 failed |
| A defect you can turn on | Six switches, default ON. `POST /test/reset` reloads the seed. Designated tests fail while the switches stay on |
| A pipeline definition | `.github/workflows/regression.yml`, triggers push, pull_request, workflow_dispatch, and `30 20 * * *`. Verified locally. Not executed on GitHub from this machine |
| A human gate on generated ideas | Deterministic drafter, 14 proposals, 8 accepted, 4 rejected, 1 duplicate, 1 invalid. Accepted cases stay `automation_intent: not-executable` |

The assistant loads `tools/prompts/edge_cases.md` and drafts from requirement and case text. It does not call an external model. Human review is mandatory. Reviewer label on the accepted work: Lab reviewer.

## Expected audience

The lab is written so each of these readers can find the layer they care about.

| Reader | What to open first |
| --- | --- |
| Recruiters | [SUMMARY_FOR_RECRUITERS.md](SUMMARY_FOR_RECRUITERS.md) and [RESUME_BULLETS.md](RESUME_BULLETS.md) |
| Hiring managers | [SUMMARY_FOR_HIRING_MANAGERS.md](SUMMARY_FOR_HIRING_MANAGERS.md) and [CASE_STUDY.md](CASE_STUDY.md) |
| QA leads | [CASE_STUDY.md](CASE_STUDY.md), `plan/test-plan.md`, and `trace/traceability_matrix.md` |
| SDET interviewers | [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md) and [DEMO_SCRIPT.md](DEMO_SCRIPT.md) |
| IBM package consultants | The workflow notes in `docs/` and the simulator limits in `docs/package_sim.md`. Read them as study models from public documentation. |
| Test automation teams | [TECHNICAL_DESIGN.md](TECHNICAL_DESIGN.md), `docs/ci.md`, `docs/postman.md`, and `.github/workflows/regression.yml` |

## What completion means

Completion means the chain exists and the measurements above were recorded locally. It means the review gate printed `review gate passed`. It means the eight new cases are design records with a reviewer name.

Completion does not mean a vendor tenant was tested, a GitHub-hosted workflow run was observed from this machine, or the full Playwright suite was executed again during M7. Those limits are part of the status, and they are repeated in [RELEASE_NOTES_v1.0.md](RELEASE_NOTES_v1.0.md) and [LESSONS_LEARNED.md](LESSONS_LEARNED.md).
