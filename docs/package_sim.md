# Package Sim

**Milestone:** M2
**Identifier:** SIMULATED

Package Sim is a local application the lab can point later browser and API checks at. It is not Intellum, Verint, IBM TRIRIGA, or IBM Maximo, and it does not connect to those products. The banner on every page is:

SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.

M1 requirement IDs remain the specification. This document is the integration map where the running simulator uses a smaller state list than the M1 workflow write-ups.

## Architecture

```text
Browser or API client
        |
        v
sim/app.py          FastAPI routes, Jinja pages, /health, /test/reset
        |
        +-- sim/learning.py
        +-- sim/quality.py
        +-- sim/workorders.py
        +-- sim/defects.py
        |
        v
sim/models.py       in-memory store
        |
        v
sim/seed.json       restored by POST /test/reset
```

Pages are server-rendered with Jinja2. The same Python functions serve `/api/...` JSON. There is no database. `POST /test/reset` reads `seed.json` again and replaces learners, enrollments, evaluations, work orders, certificates, and defect switches.

Run it from `package-test-lab`:

```text
python -m pip install -r sim/requirements.txt
python -m uvicorn sim.app:app --reload
```

Open `http://127.0.0.1:8000/`. Generated OpenAPI is at `/docs`. The API description repeats the simulated disclaimer. JSON responses carry `X-Simulated: true`.

Illegal workflow transitions return HTTP 409 with a `detail` that names the source and target states. Missing fields return HTTP 422. Unknown IDs return HTTP 404.

## State models

### Learning

Catalog status is separate from enrollment status.

| Object | States |
| --- | --- |
| Activity | Available, Draft |
| Enrollment | Enrolled, In Progress, Passed, Failed, Completed |

| From | Event | To | Guard |
| --- | --- | --- | --- |
| Available activity | Enroll | Enrolled | No other active enrollment for that learner and activity. Draft activities are rejected. |
| Enrolled | Start | In Progress | Content modules are marked complete. |
| In Progress | Assessment score | Passed or Failed | Pass mark below. Attempt count increases. The fourth attempt is rejected. |
| Failed | Reset | Enrolled | Attempts used is below 3. History is kept. |
| Passed | Complete | Completed | A certificate is issued when the activity is configured for one. |

`Passed` then `Completed` follows M1: the score outcome and the completion record are different states. A certificate is a record, not a state. `Available` is the catalog word for what M1 called a published activity.

Pass rule, defect off: rounded score `>= 80.00`. Scores use half-up rounding to two decimal places, so 79.995 is stored as 80.00.

### Quality

M1 describes an evaluation status and a separate coaching status. The simulator keeps one `state` on the evaluation so the M2 list is a single machine. Score, acknowledgement time, dispute comment, and coaching note stay on the same record.

| From | Event | To |
| --- | --- | --- |
| Pending | Submit sections A, B, and C | Under Review |
| Under Review | Acknowledge | Acknowledged |
| Under Review | Dispute with a comment | Disputed |
| Under Review | Coach with a note | Coached |
| Disputed | Resolve | Under Review |
| Acknowledged | Coach with a note | Coached |
| Acknowledged | Complete | Completed |
| Coached | Acknowledge | Acknowledged |
| Coached | Complete | Completed |

Pending cannot jump to Acknowledged, Coached, or Completed. Disputed cannot complete until it returns to Under Review.

Score, defect off: section percent times weight, divided by 100. Weights are A 60, B 20, C 20. Classification is `Meets standard` at 80.00 or above, otherwise `Below standard`. The learning pass-mark switch does not affect this threshold.

M1 states map onto this machine as follows.

| M1 idea | Simulator |
| --- | --- |
| Evaluation in progress | Pending |
| Submitted or waiting for review | Under Review |
| Accepted, plus the acknowledgement fact | Acknowledged |
| Disputed | Disputed |
| Coaching held | Coached |
| Session or evaluation finished | Completed |

### Work orders

M1 splits a service request from a work task. The simulator uses one work-order record that travels the whole path. Request, approval, assignment, labor, materials, completion, and closure are fields and transitions on that record.

| From | To | Guard |
| --- | --- | --- |
| Draft | WAPPR | Required request fields are already present. |
| WAPPR | APPR | `actor_id` is present and is not the requester. |
| APPR | INPRG | A technician is assigned. |
| APPR | WMATL | — |
| INPRG | WMATL | — |
| INPRG | COMP | — |
| WMATL | INPRG | — |
| COMP | CLOSE | — |
| COMP | INPRG | A rework reason is present. Actuals stay. `completed_at` is cleared. This is M1 assumption ASM-TRI-08. |

`INPRG -> CLOSE` is rejected. `CLOSE` has no legal successor unless the reopen defect is on. Time and materials are accepted in `APPR`, `INPRG`, `WMATL`, and `COMP`. Hours must be greater than 0 and at most 24.00.

`CAN`, `WSCH`, `WPCOND`, and `HISTEDIT` are not states in this simulator.

## Defect catalog

Switches live in `sim/defects.py` and default to ON in `seed.json`. Change one with `POST /api/defects/{id}` and `{"enabled": false}`. `POST /test/reset` turns them back on. A switch changes new decisions. It does not rewrite scores already stored in the seed.

| ID | What ON does | What OFF does | Requirement |
| --- | --- | --- | --- |
| `pass_mark` | Score passes only when it is greater than 80.00. Exactly 80.00 fails. | Score passes at 80.00 and above. | REQ-INT-004 |
| `certificate_date` | `issued_on` is one day before `completion_date`. | The two dates are the same day. | REQ-INT-007 |
| `quality_score` | Total is the unweighted mean of the three section percents. | Total uses weights 60, 20, and 20. | REQ-VER-003 |
| `reopen_closed` | `CLOSE -> INPRG` is accepted and `reopened` becomes true. | That transition returns HTTP 409. | REQ-TRI-009 |
| `invalid_completion` | `APPR -> COMP` is accepted. | `COMP` is accepted only from `INPRG`. | REQ-TRI-008 |
| `inactive_assignment` | Inactive technician `TEC-02` can be assigned. | That assignment returns HTTP 409. | REQ-TRI-004 |

`invalid_completion` does not allow `INPRG -> CLOSE`. `inactive_assignment` does not allow assignment onto a closed order.

Worked quality example, sections A 1/2, B 1/1, C 1/1:

- Defect off: 70.00, Below standard.
- Defect on: 83.33, Meets standard.

## API inventory

| Method | Path | Role |
| --- | --- | --- |
| GET | `/health` | Liveness. `status` is `ok`. |
| POST | `/test/reset` | Reload `seed.json`. |
| GET | `/` | Home page. |
| GET | `/learning` | Learning page. |
| GET | `/quality` | Quality page. |
| GET | `/workorders` | Work-order page. |
| GET | `/defects` | Defect switches. |
| GET | `/api/learning/activities` | Catalog. |
| GET | `/api/learning/learners` | Five seeded learners. |
| GET | `/api/learning/enrollments` | Enrollment records. |
| GET | `/api/learning/certificates` | Certificate records. |
| POST | `/api/learning/enrollments` | Body `learner_id`, `activity_id`. |
| POST | `/api/learning/enrollments/{id}/start` | Enrolled to In Progress. |
| POST | `/api/learning/enrollments/{id}/assessment` | Body `score`. |
| POST | `/api/learning/enrollments/{id}/reset` | Failed back to Enrolled when attempts remain. |
| POST | `/api/learning/enrollments/{id}/complete` | Passed to Completed. |
| GET | `/api/quality/interactions` | Seeded interactions. |
| GET | `/api/quality/evaluations` | Five seeded evaluations. |
| POST | `/api/quality/evaluations` | Body `interaction_id`. |
| POST | `/api/quality/evaluations/{id}/submit` | Body `sections` with A, B, and C. |
| POST | `/api/quality/evaluations/{id}/acknowledge` | To Acknowledged. |
| POST | `/api/quality/evaluations/{id}/dispute` | Body `comment`. |
| POST | `/api/quality/evaluations/{id}/resolve` | Disputed to Under Review. |
| POST | `/api/quality/evaluations/{id}/coach` | Body `note`. |
| POST | `/api/quality/evaluations/{id}/complete` | To Completed. |
| GET | `/api/work/orders` | Ten seeded work orders. |
| GET | `/api/work/technicians` | `TEC-01` active, `TEC-02` inactive. |
| POST | `/api/work/orders` | Create a Draft. |
| POST | `/api/work/orders/{id}/transition` | Body `to`, optional `actor_id` and `reason`. |
| POST | `/api/work/orders/{id}/assign` | Body `technician_id`. |
| POST | `/api/work/orders/{id}/time` | Body `technician_id`, `hours`. |
| POST | `/api/work/orders/{id}/materials` | Body `item_id`, `quantity`. |
| GET | `/api/defects` | Catalog and current switches. |
| POST | `/api/defects/{id}` | Body `enabled`. |

HTML forms post to `/ui/...` and redirect back to the page. Those form routes are for the browser. API clients should use `/api/...`.

## Seed

| Collection | Count | Notes |
| --- | --- | --- |
| Learners | 5 | `LN-01` through `LN-05` |
| Evaluations | 5 | One each of Pending, Under Review, Acknowledged, Disputed, Coached |
| Work orders | 10 | Draft, WAPPR, APPR, INPRG, WMATL, COMP, and CLOSE are all present |

`ACT-102` is an empty available course used to exercise new enrollments. `ACT-103` is Draft and cannot be enrolled. `TEC-02` is the inactive technician.

## Verification

`tests/test_package_sim.py` checks health, the simulated banner, reset, seed counts, legal transitions, illegal transitions, each defect switch, and restoration of seed state. It is simulator verification. It is not the M3 test-case catalog, and it is not Playwright, Postman, Newman, or CI.

## Readiness for M3

M3 can write test cases against this running target. Case IDs should still cite M1 requirement IDs. Where this document simplifies a status, the case should name the simulator state and the M1 requirement together.

Before writing cases, note:

- Quality uses one state field, not the two M1 machines.
- A work order is one record, not a separate request and task.
- Planted defects default to ON. A case that expects the M1 rule must turn the related switch OFF first, or it will observe the defect on purpose.
- `POST /test/reset` is the way back to the seed, including switches.
