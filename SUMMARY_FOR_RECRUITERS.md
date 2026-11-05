# Summary for recruiters

**Package Functional Test Lab** is a personal portfolio project. It shows a complete functional-testing chain on simulated enterprise workflows.

**SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.**

The workflows are study models from publicly available documentation. This is not a job at IBM or at a software vendor, and it is not a claim of product access, employment, certification, or partnership.

## What the project demonstrates

**Requirements engineering.** Twenty-seven written requirements cover learning (9), quality (8), and facilities work (10). Each one has acceptance criteria. Where a public document left a rule unspecified, the lab recorded a named assumption. Thirteen requirements are high risk because they grant or withhold a pass, a certificate, a quality result, an acknowledgement, or a closure.

**Test design.** Sixty YAML test cases were designed against those requirements and left unchanged. A later review added eight more design cases. The catalog total is 68. Techniques in the lab include boundary values, state transitions, decision tables, negative tests, and exploratory notes.

**Automation frameworks.** A small local application, Package Sim, is the system under test. Twenty-six browser tests run in Chromium with Playwright. Three Postman collections run through Newman against the same application. The browser report shows 26 tests and 0 failures. The API JUnit report shows 82 tests and 0 failures. The API JSON report shows 138 assertions and 0 failed. Both API counts are from the same run. They differ because one reporter folds repeated data rows together.

**CI/CD.** A GitHub Actions workflow runs the browser suite and the API suite on push, on pull request, on a manual run, and on a nightly schedule at 20:30 UTC. A review check runs before the suites. The workflow file was checked locally. It has not been executed on GitHub from this machine.

**AI-assisted QA.** A deterministic drafting tool reads the requirements and proposes missing edge cases. It does not call an external model. A person accepted 8 drafts and rejected 4. One duplicate and one invalid draft were counted and discarded. Accepted cases are design notes only. They are not automated tests. Acceptance rate on everything generated: 0.57. Rate on the drafts a person reviewed: 0.67. Reviewer: Lab reviewer.

**Enterprise testing concepts.** The simulator includes six known defects that default to on, covering an exclusive pass mark, a shifted certificate date, an unweighted quality score, reopening closed work, completing from the wrong status, and assigning an inactive technician. Turning a defect off makes the matching test pass. Leaving it on makes that test fail. That is how the suite shows it can still detect the break.

## Scale, in one glance

| Item | Figure |
| --- | --- |
| Requirements | 27 |
| Test cases | 68 |
| Browser tests | 26, 0 failures |
| API JUnit tests | 82, 0 failures |
| API assertions | 138, 0 failed |
| Known defect switches | 6 |
| Drafts accepted after review | 8 of 14 generated |

## How to read it in five minutes

Start with `README.md`, then `reports/summary.md`, then `DEMO_SCRIPT.md`. The interview question set is `INTERVIEW_GUIDE.md`.
