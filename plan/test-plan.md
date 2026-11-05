# Test plan

**Document ID:** TP-PTL-001
**Product:** Package Functional Test Lab
**Version:** M1 baseline
**Identifier:** SIMULATED
**Standard alignment:** ISO/IEC/IEEE 29119-1 (concepts), 29119-2 (test processes), 29119-3 (test documentation), 29119-4 (test techniques)

This plan follows the test-plan ideas in ISO/IEC/IEEE 29119. It is a project test plan for a simulated lab. It is not a claim that the lab has been certified against the standard, and it does not reproduce the standard's text.

M1 finishes test planning and static specification. Dynamic test execution, monitoring, and a test completion report belong to 29119-2 and are later deliverables. They are listed in section 12 and they do not exist yet.

## Standards alignment

| This plan | 29119 idea |
| --- | --- |
| Section 1 Scope | Test plan context and scope of testing |
| Section 2 Objectives | Test objectives |
| Section 3 Test items | Items to be tested |
| Sections 4 and 5 | Features to be tested and features not to be tested |
| Section 6 Test levels | Test sub-processes at unit, integration, system, and acceptance levels |
| Section 7 Test techniques | 29119-4 design techniques, plus risk-based test management from 29119-1 and 29119-2 |
| Section 8 Automation strategy | Approach for later dynamic testing. No automation is produced by this plan. |
| Sections 9 and 10 | Entry and exit criteria |
| Section 11 Risks | Risks and contingencies |
| Section 12 Deliverables | Test work products |
| Assumption register | The conditions a later test oracle must use when the public source is silent |

Traceability from requirement to test case to automation to CI result is specified in `docs/traceability_strategy.md`.

## 1 Scope

The lab will eventually test three simulated workflows:

1. An Intellum-style learning path from enrollment through certificate issuance, including a simulated enrollment API contract.
2. A Verint-style quality path from interaction evaluation through score, threshold, acknowledgement, dispute, and coaching.
3. A TRIRIGA-style corrective-maintenance path using Maximo status names, from service request through time, materials, completion, closure, and rework.

**M1 scope** is the specification itself: requirements, workflow models, this plan, the defect template, and the traceability structure. The test activity in M1 is static review of those documents.

**Execution scope** (later milestones) is the simulated lab only. Testing against a live Intellum, Verint, TRIRIGA, or Maximo environment is outside the lab.

Inclusions, exclusions, and the assumption register below are the authority for what a later test may expect. A test that expects a live vendor response is out of scope even if a public document describes that vendor.

## 2 Objectives

1. Give each in-scope business rule a stable requirement ID, a public source, an explicit assumption where the source is silent, and acceptance criteria a test can observe.
2. Make state changes and decision points visible before any test case is written.
3. Select techniques that match those rules: partitions and boundaries for scores and quantities, decision tables for combined conditions, state transitions for lifecycles, exploratory testing for the gaps between rules, and risk to decide what is tested first.
4. Define entry and exit criteria for M1 separately from entry and exit criteria for later execution, so a finished plan is not reported as a finished test.
5. Keep every work product labeled simulated, with vendor names used only as the source of the public documentation.

## 3 Test items

| Item | Identity in M1 | Later identity |
| --- | --- | --- |
| Learning workflow specification | `REQ-INT-001` through `REQ-INT-009`, `docs/intellum_workflow.md` | A simulated learning component that does not yet exist |
| Quality workflow specification | `REQ-VER-001` through `REQ-VER-008`, `docs/verint_workflow.md` | A simulated quality component that does not yet exist |
| Work workflow specification | `REQ-TRI-001` through `REQ-TRI-010`, `docs/tririga_workflow.md` | A simulated work component that does not yet exist |
| Traceability and defect rules | `docs/traceability_strategy.md`, `docs/defect_template.md` | The same documents, plus future rows and defect records |

There is no build, no interface, and no data set to execute. The M1 test item is the document set.

## 4 Features to test

Risk is the 29119 risk-based priority for later execution. High means an incorrect result would issue or withhold a credential, a quality outcome, an acknowledgement, a work task, or a closure. Medium means the rule matters and is less central than those outcomes.

| Requirement | Feature | Risk |
| --- | --- | --- |
| REQ-INT-001 | Create one active enrollment | Medium |
| REQ-INT-002 | Ordered learning-module progress | Medium |
| REQ-INT-003 | Score an on-demand assessment attempt | Medium |
| REQ-INT-004 | Pass at the inclusive threshold | High |
| REQ-INT-005 | Fail, retake, and attempt limit | High |
| REQ-INT-006 | Completion timestamp and status | High |
| REQ-INT-007 | One certificate when completion criteria are met | High |
| REQ-INT-008 | Simulated enrollment write contract | Medium |
| REQ-INT-009 | Simulated enrollment read contract | Medium |
| REQ-VER-001 | Start an employee-perspective evaluation | Medium |
| REQ-VER-002 | Mandatory questions on the evaluation form | Medium |
| REQ-VER-003 | Calculate and store the form total | High |
| REQ-VER-004 | Compare the total with the threshold | High |
| REQ-VER-005 | Coaching session status lifecycle | Medium |
| REQ-VER-006 | Agent acknowledgement | High |
| REQ-VER-007 | Accept, dispute, and resolve | High |
| REQ-VER-008 | Link coaching to an evaluation without changing the score | Medium |
| REQ-TRI-001 | Submit a service request | Medium |
| REQ-TRI-002 | Approve or reject the request | High |
| REQ-TRI-003 | Create one task from an approved request | High |
| REQ-TRI-004 | Assign or accept a task | Medium |
| REQ-TRI-005 | Start work in progress | Medium |
| REQ-TRI-006 | Time entry bounds and allowed statuses | Medium |
| REQ-TRI-007 | Material entry | Medium |
| REQ-TRI-008 | Submit completion | High |
| REQ-TRI-009 | Close and make the task read-only | High |
| REQ-TRI-010 | Return rejected work for rework | High |

## 5 Features not to test

The public sources mention these. They are excluded so later tests do not grow to cover them by implication.

- Live vendor tenants, SSO, and production data
- Intellum proctoring (Honorlock, Safe Exam Browser), adaptive testing, ecommerce, Credly, LinkedIn sharing, and certificate PDF rendering
- Intellum recertification scheduling and renewal campaigns
- Published API rate limits (200 requests per second, list-endpoint limits, HTTP 429). They are public context, not M1 functional scope
- Verint customer-perspective assessments, speech and text analytics, automated form questions, form selection from interaction metadata, calibration, and report-latency behavior
- Workforce-management scheduling of coaching, beyond the public status name Pending
- TRIRIGA preventive maintenance generation, projects other than the single corrective task, reservations, move requests, procurement, and surveys as a user interface
- Maximo statuses `WSCH`, `WPCOND`, and `HISTEDIT`, inventory balances, and direct issue purchasing
- Security penetration, load, accessibility, and localization
- The AI assistant, CI pipeline, and browser or API automation harnesses listed as later milestones

A defect that asks the lab to implement an excluded feature is rejected against this section, or turned into a scope change before any test is added.

## 6 Test levels

29119-2 separates static and dynamic testing. M1 uses static testing only.

| Level | M1 | Later milestone, not started |
| --- | --- | --- |
| Static review | Review requirements for the mandatory sections, source links, assumptions, and acceptance criteria. Review workflows for states and decisions. Review this plan for the sections in the M1 exit criteria. | Repeat when a requirement changes. |
| Component | Not run. There is no component. | One simulated workflow component at a time, through its service boundary, using state and decision tests. |
| Integration | Not run. | Learning completion to certificate. Quality score to threshold to coaching link. Approved request to task to closure of the parent request. |
| System | Not run. | An end-to-end simulated path for each workflow, using the decision points in the workflow documents. |
| Acceptance | Not run. | Comparison of observed simulated behavior with the acceptance criteria and the accepted assumption register. |

No level above static review can start under this plan until the M1 exit criteria are met and the assumption register is accepted.

## 7 Test techniques

Techniques specify how later tests will be designed. The examples are design sketches for the oracle. They are not test cases, and they have not been executed.

Risk-based testing is the management technique that orders the work. The other five are design techniques. Exploratory testing is the experience-based technique in the 29119 series. Equivalence partitioning, boundary value analysis, decision table testing, and state transition testing are specification-based techniques in 29119-4.

### Equivalence partitioning

Divide inputs into classes that the rule treats the same way. Test one representative from each class.

Learning enrollment (`REQ-INT-001`): valid classes are catalog, administrator, and rule-based creation against a published activity. Invalid classes are an unpublished activity, an unknown learner, and a second active enrollment. One valid path and each invalid class are enough to represent the rule. The three valid paths still each appear once because `ASM-INT-01` says they must produce the same enrollment shape. That is three representatives of the valid class, chosen because the assumption names them.

Time hours (`REQ-TRI-006`): valid class is (0, 24.00]. Invalid classes are 0, negative, and greater than 24.00.

### Boundary value analysis

On an ordered boundary, test the values at the edge and the values immediately outside.

| Rule | Boundary | Values to include in later cases |
| --- | --- | --- |
| Pass threshold 80.00 inclusive (`ASM-INT-06`, `REQ-INT-004`, `REQ-INT-005`) | 80.00 | 79.99 fails. 80.00 passes. 80.01 passes. |
| Quality threshold 80.00 inclusive (`ASM-VER-03`, `REQ-VER-004`) | 80.00 | Same three values, applied to the form total. |
| Attempt limit 3 (`ASM-INT-07`) | 3rd and 4th attempt | Attempt 3 may be scored. Attempt 4 without a reset is rejected. |
| Time entry (`REQ-TRI-006`) | 0 and 24.00 | 0 rejected. 0.01 accepted. 24.00 accepted. 24.01 rejected. |
| Material quantity (`REQ-TRI-007`) | 0 | 0 rejected. The smallest positive unit the lab allows is accepted. |

Scores use two decimal places. A later test must not send 80.001 and call it the boundary.

### Decision tables

Use a table when the outcome depends on a combination of conditions.

**Certificate issuance (`REQ-INT-004`, `REQ-INT-006`, `REQ-INT-007`)**

| Assessment required | Score versus threshold | Certificate configured | Enrollment outcome | Certificate |
| --- | --- | --- | --- | --- |
| Yes | At or above | Yes | Completed | One certificate |
| Yes | At or above | No | Completed | None |
| Yes | Below | Yes | Failed | None |
| Yes | Below | No | Failed | None |
| No, content only | Not applicable | Yes | Completed when required modules are done | One certificate |
| Attendance recorded, no score | Not applicable | Yes | Not passed | None |

**Request approval (`REQ-TRI-002`, `REQ-TRI-003`)**

| Actor | Decision | Reason present | Next request status | Task count |
| --- | --- | --- | --- | --- |
| Other person | Approve | Not required | APPR | 1 |
| Requester | Approve | Any | Unchanged WAPPR | 0 |
| Other person | Reject | Yes | CAN | 0 |
| Other person | Reject | No | Unchanged WAPPR | 0 |

**Coaching feedback (`REQ-VER-005`)**

| Session type | Feedback received | Actor | Next status |
| --- | --- | --- | --- |
| Individual | The employee responded | Coach path | Await Coach Follow Up |
| Group | Some employees responded | Any | Await Employee Feedback |
| Group | Every employee responded | Coach path | Await Coach Follow Up |
| Group | Some employees responded | Manager forces completion | Completed |

### State transition testing

Each workflow document has a transition table. Later tests will cover:

- Every valid transition on the simulated path (0-switch)
- Illegal transitions that the guards name: duplicate enrollment, submit with a mandatory question empty, start work with no resource, time entry after `CLOSE`, acknowledge an in-progress evaluation, close from any status other than `COMP`
- The rework cycle `INPRG → COMP → INPRG → COMP → CLOSE` because `ASM-TRI-08` is a deviation from the Maximo table and is easy to implement backwards

A transition that the workflow marks as recognized and not simulated is tested only as a rejection, with the workflow section cited as the oracle.

### Exploratory testing

Exploratory testing is chartered, time-boxed learning during later execution. It is not a substitute for the decision tables above. M1 defines charters and does not run them.

| Charter | Mission | Requirements in focus |
| --- | --- | --- |
| CH-INT-001 | After a failure and a reset, look for a certificate, a cleared history, or a second completion date. | REQ-INT-005, REQ-INT-006, REQ-INT-007 |
| CH-VER-001 | Dispute one answer, leave another unresolved, and try to acknowledge or coach in the middle of the dispute. | REQ-VER-006, REQ-VER-007, REQ-VER-008 |
| CH-TRI-001 | Record time and materials, reject completion, and confirm the actuals survive rework and die at closure. | REQ-TRI-006, REQ-TRI-007, REQ-TRI-009, REQ-TRI-010 |

Notes from a charter cite the requirement the tester was using as the oracle. A surprise becomes a defect only when it contradicts a requirement or an accepted assumption. A surprise that the specification never mentioned becomes a `SPEC` defect against this plan.

### Risk-based testing

Risk chooses depth. It does not delete Medium rows from the traceability matrix.

| Risk signal | Why it is High | Minimum later depth |
| --- | --- | --- |
| Score versus an inclusive threshold | Off-by-one grants a pass, a certificate, or a "meets standard" result | Boundary values plus the decision table |
| Certificate and completion | A missing or duplicate credential is the learning workflow's business outcome | Decision table and a state check that completion time is set once |
| Acknowledgement and dispute | The employee record of fairness is the quality workflow's control | State transitions, including the actor guard |
| Approval creates work | A rejected or self-approved request must not create a task | Decision table |
| Closure and rework | Closure is irreversible in the model, and rework contradicts the Maximo table on purpose | State cycle in the exploratory charter and a transition test |

Medium features get equivalence classes and the happy-path transition. They are automated only after the High rows have automation IDs, unless a Medium row blocks a High path.

## 8 Automation strategy

**M1 implements no automation.** `tools/` contains no tests. `reports/` contains no results. Naming Playwright, Postman, Newman, or GitHub Actions here records the intended *class* of later work. It does not select a product, install a tool, or authorize that milestone.

Principles for the milestone that eventually automates:

1. Automate checks whose oracle is a requirement acceptance criterion and an accepted assumption ID.
2. Prefer automation for boundaries, decision-table rows, and illegal transitions. Leave exploratory charters manual.
3. Every automated check carries `AUTO-{area}-{requirement}-{case}` and runs the matching `TC-*` ID from `docs/traceability_strategy.md`.
4. A manual test is complete without an automation node. Do not wrap it in a script so the matrix looks uniform.
5. A future CI job appends a result. It does not rewrite the requirement. A failed result links to `DEF-*` or to a rejected-test note.
6. Checks that encode `ASM-TRI-08` name that assumption in the test so a failure is read as "rework behavior" and not as "Maximo table drift."
7. Simulated HTTP routes in `REQ-INT-008` and `REQ-INT-009` are contract names. Automation of those routes waits until a simulated service exists. No test sends traffic to Intellum, Verint, or IBM.

Suggested split when automation is eventually allowed:

| Check kind | Candidate class of tool | Workflow fit |
| --- | --- | --- |
| State, score, and contract checks | API-level checks against the simulated lab | All three workflows |
| A thin path a person would click, if a UI is ever built | Browser-level checks | One happy path per workflow, not the boundary matrix |
| Repeatable run and stored result | CI job writing into `reports/` | Automated IDs only |

Until that milestone, the automation cell in the traceability matrix stays empty.

## 9 Entry criteria

### Entry to M1 static review

Met when this repository was created:

- The three public workflow areas are identified.
- Requirement, plan, docs, tools, and reports locations exist.
- Authors have access to the public sources cited in the requirements.

### Entry to later dynamic testing

All of the following are required. **None of the execution-only items are met in M1.**

- M1 exit criteria are met.
- The assumption register in this plan is accepted or revised. Unaccepted assumptions cannot be oracles.
- A simulated implementation of the requirements exists and is identified by a version.
- Test cases exist, cite requirement and assumption IDs, and have been reviewed.
- The environment record says `simulated lab` and names the build. It does not point at a vendor tenant.
- High-risk requirements have at least one written test case per acceptance criterion.

## 10 Exit criteria

### M1 exit (this milestone)

M1 is complete when all of the following are true:

1. The repository contains 20 to 30 requirements, and the actual count is 27: 9 learning, 8 quality, and 10 work.
2. Every requirement has a requirement ID, description, business rule, source link, simulated assumptions, and acceptance criteria.
3. `docs/intellum_workflow.md`, `docs/verint_workflow.md`, and `docs/tririga_workflow.md` each contain an ASCII diagram, a Mermaid diagram, state transitions, decision points, and assumptions.
4. This plan contains sections 1 through 12 and documents the six techniques named for the lab.
5. `docs/defect_template.md` defines every required field.
6. `docs/traceability_strategy.md` defines Requirement → Test case → Automation → CI result.
7. README states the purpose, the scope, the simulated disclaimer, the structure, and the milestone roadmap.
8. The repository contains no simulator, UI, API implementation, test case, automation, CI workflow, or assistant.

M1 exit does **not** mean any business rule has been verified by execution.

### Later execution exit

Defined now so the lab does not invent a new bar after the first run. Not claimed in M1.

- Every High requirement has an executed result against each of its acceptance criteria.
- Every Medium requirement has an executed result against at least one acceptance criterion.
- No open Severity 1 defect remains against the simulated build under test.
- Open Severity 2 defects are either fixed or explicitly deferred with the requirement ID named.
- The traceability matrix shows, for each automated test, the requirement, the test case, the automation ID, and a CI result for the candidate build.
- Manual and exploratory rows show a human result and do not show a fabricated CI result.
- Residual risk, including the TRIRIGA/Maximo composite and `ASM-TRI-08`, is written in the completion notes.

## 11 Risks

| ID | Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- | --- |
| R-01 | A reader treats the lab as a real tenant or as vendor experience. | Medium | High | Simulated banner on every major document. Vendor names only as documentation sources. No network client in M1. |
| R-02 | A public page describes a product at a level that omits the rule a test needs. | High | High | Assumption IDs. Tests cite the assumption. Silent invention is a specification defect. |
| R-03 | Thresholds 80.00 and attempt limit 3 are lab choices and will be mistaken for published vendor constants. | High | High | `ASM-INT-06`, `ASM-INT-07`, and `ASM-VER-03` state that they are sample values. |
| R-04 | The work model mixes TRIRIGA process with Maximo codes. | High | High | `docs/tririga_workflow.md` separates the two sources. `ASM-TRI-01` and `ASM-TRI-08` record the composite and the rework deviation. |
| R-05 | Public URLs move, require sign-in, or change. | Medium | Medium | Each requirement names the page and the statement that was used. A broken link is a documentation defect, not a reason to drop the rule. |
| R-06 | M1 completion is reported as test completion. | Medium | High | Separate exit criteria. Traceability states stay at Specified. `reports/` stays empty of results. |
| R-07 | Later automation encodes a simulated route as if it were a vendor API. | Medium | High | `ASM-INT-10` names `/simulated/intellum/...` as lab identifiers. Section 8 forbids traffic to vendor hosts. |
| R-08 | Customer training PDFs (Arizona TRIRIGA manual, and similar) are read as IBM specification. | Medium | Medium | IBM documents are the primary work sources. The Arizona manual is labeled a secondary public training illustration. |

Contingency for R-02 and R-03: stop test design for the affected requirement until the assumption is accepted or rewritten. Do not fill the gap with an undocumented expected result.

## 12 Deliverables

| Deliverable | M1 | Later |
| --- | --- | --- |
| README with disclaimer, scope, structure, roadmap | `README.md` | Update when a milestone actually starts |
| Requirements | `requirements/REQ-*.md` and inventory | Revise under change control |
| Workflow specifications | `docs/*_workflow.md` | Revise with the requirements |
| Test plan | This document | Revise when scope or assumptions change |
| Defect template | `docs/defect_template.md` | Defect records when execution finds issues |
| Traceability strategy | `docs/traceability_strategy.md` | Matrix rows when test cases exist |
| Test cases | Not delivered | A later milestone |
| Automation | Not delivered | A later milestone |
| CI results | Not delivered | A later milestone |
| Test completion report | Not delivered | After execution exit is assessed |
| Simulator, UI, API, assistant | Not delivered | Only if a later milestone is explicitly started |

## Assumption register

Accepting this register is an entry condition for dynamic testing. Until then, the assumptions are the M1 specification of the gaps. They are simulated lab choices.

### Laboratory

| ID | Statement |
| --- | --- |
| ASM-LAB-01 | No component in this lab connects to Intellum, Verint, IBM TRIRIGA, IBM Maximo, or any customer system. |

### Learning

| ID | Statement |
| --- | --- |
| ASM-INT-01 | Enrollment paths are catalog self-enrollment, administrator enrollment, and rule-based assignment. |
| ASM-INT-02 | At most one active enrollment exists per learner per activity. |
| ASM-INT-03 | Only a published activity can be enrolled. |
| ASM-INT-04 | A new enrollment is `Enrolled` and has no score, completion time, or certificate. |
| ASM-INT-05 | The sample path is ordered. Content modules complete when viewed. The assessment completes only when passed. |
| ASM-INT-06 | Sample pass threshold is 80.00 percent, inclusive, two decimal places, half-up. |
| ASM-INT-07 | Sample maximum is 3 attempts. Reset keeps attempt history. |
| ASM-INT-08 | `Passed` becomes `Completed` once for the sample certification activity. |
| ASM-INT-09 | Certificate codes use `SIM-CERT-{activityCode}-{year}-{sequence}`. No PDF, Credly, or LinkedIn call. |
| ASM-INT-10 | Write and read contracts use `/simulated/intellum/enrollments`. Those paths are lab names. |

### Quality

| ID | Statement |
| --- | --- |
| ASM-VER-01 | Manual employee-perspective evaluation only. |
| ASM-VER-02 | Form `SIM-QM-001` uses section weights 60, 20, and 20 and the percentage rollup described in `docs/verint_workflow.md`. |
| ASM-VER-03 | Sample quality threshold is 80.00 inclusive. The raw score is unchanged by the comparison. |
| ASM-VER-04 | The first acknowledgement time is kept. Acknowledgement does not change score or status. |
| ASM-VER-05 | A dispute needs a question and a comment. The employee does not resolve it. |
| ASM-VER-06 | A coaching link does not change the evaluation score. |
| ASM-VER-07 | Coaching statuses are Pending, Coached, Await Employee Feedback, Await Coach Follow Up, and Completed. A manager may complete a group session early. |

### Work

| ID | Statement |
| --- | --- |
| ASM-TRI-01 | Maximo status names label a TRIRIGA-style corrective process. The products are not claimed to share codes. |
| ASM-TRI-02 | Submit requires request class, requester, building, and description. |
| ASM-TRI-03 | The requester cannot approve their own request. |
| ASM-TRI-04 | Plan `SIM-PLAN-CORRECTIVE` creates one task. |
| ASM-TRI-05 | Simulated assignment rules are Auto-Assign and Do not Assign. |
| ASM-TRI-06 | Time and materials are records. No inventory engine. Close sets `reservations_released` without moving stock. |
| ASM-TRI-07 | Happy path is Draft → WAPPR → APPR → INPRG → COMP → CLOSE. `WMATL` returns to `INPRG`. Completion is submitted from `INPRG` only. |
| ASM-TRI-08 | `COMP` rejected with a reason returns to `INPRG` and keeps actuals. This differs from the Maximo successor of `COMP`, which is `CLOSE` only. |
| ASM-TRI-09 | Close records a requestor notification and can set `survey_due`. It does not send mail or show a survey. |

## Proposed later milestones

These are not started. They are recorded so M1 exit is not confused with them.

| Milestone | Starts only when |
| --- | --- |
| M2 Simulated behavior | This plan's assumption register is accepted, and someone explicitly asks for a simulator. |
| M3 Test cases | M1 exit is met. Cases cite requirement and assumption IDs. |
| M4 Automation | Test cases exist. Section 8 is re-approved with a concrete tool choice. |
| M5 CI results | Automation IDs exist and a pipeline is explicitly requested. |
| M6 Assistant | Explicitly requested. It is absent from M1. |
