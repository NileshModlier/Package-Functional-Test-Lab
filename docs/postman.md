# Postman and Newman

**Milestone:** M5
**Identifier:** SIMULATED

Package Sim is the system under test. These collections call its JSON API. They do not call Intellum, Verint, IBM TRIRIGA, or IBM Maximo.

CI and an assistant are out of scope for this milestone.

## Collection architecture

Three collections live in `postman/collections/`. Each one can run alone.

| Collection | File | Data file |
| --- | --- | --- |
| Package Sim Learning | `learning.postman_collection.json` | `postman/data/pass_mark_boundaries.csv` |
| Package Sim Quality | `quality.postman_collection.json` | `postman/data/quality_boundaries.csv` |
| Package Sim Work Orders | `workorders.postman_collection.json` | `postman/data/work_hours_boundaries.csv` |

Each collection has three folders:

1. **Setup** checks `/health`, reloads the seed with `POST /test/reset`, and turns the planted switches that this workflow cares about to OFF.
2. **Workflow** runs once, on iteration 0. Later CSV iterations skip it. Requests pass ids through collection variables such as `enrollmentId`, `evalDisputeId`, and `newOrderId`.
3. **Boundaries** run on every CSV row. The folder is skipped when Newman is started without a data file.

`postman/build_collections.py` regenerates the collection JSON, the environment, the CSV files, and the request rows in `docs/api_traceability.md`.

## Variable strategy

`postman/environments/local.postman_environment.json` supplies:

| Variable | Value | Use |
| --- | --- | --- |
| baseUrl | `http://127.0.0.1:18765` | Every request URL is `{{baseUrl}}` plus a path. |
| forceDefects | `false` | When `true`, the Disable requests are skipped and the seed switches stay ON. |

Collection variables hold ids created earlier in the same iteration. CSV columns are read with `pm.iterationData` and substituted into JSON bodies (`{{score}}`, `{{earned_a}}`, `{{hours}}`).

Environment values override collection values. Newman `--env-var forceDefects=true` is the defect-on run.

## Boundary testing

Scores use half-up rounding to two decimals. The pass mark and the quality threshold are inclusive when the matching switch is OFF.

| File | Rows | Rule under test |
| --- | --- | --- |
| `pass_mark_boundaries.csv` | 79.99, 80.00, 80.01, 79.994, 79.995 | 79.994 fails as 79.99. 79.995 and 80.00 pass. 80.01 passes. |
| `quality_boundaries.csv` | section points for 79.99, 80.00, and 80.01 | Weighted score and classification. 80.00 meets standard. |
| `work_hours_boundaries.csv` | 0, 0.01, 24, 24.01 | 0 and 24.01 are rejected. 0.01 and 24 are stored. The order stays APPR. |

## Negative testing

Assertions expect the simulator error body `detail` and the HTTP status.

| Check | Status |
| --- | --- |
| Duplicate active enrollment | 409 |
| Unpublished activity, assessment before start, second completion, failed completion | 409 |
| Unknown enrollment or interaction | 404 |
| Missing quality section, empty dispute, blank request title, rework without a reason, hours out of range, zero material | 422 |
| Self-approval, inactive technician, start without a technician | 409 |
| INPRG to CLOSE, WMATL to COMP, APPR to COMP, CLOSE to INPRG | 409 |
| Time on a closed order | 409 |

## Reporting

Start Package Sim, then run each collection with the CLI, JUnit, and JSON reporters:

```text
python -m uvicorn sim.app:app --host 127.0.0.1 --port 18765
```

```text
npx newman run postman/collections/learning.postman_collection.json -e postman/environments/local.postman_environment.json -d postman/data/pass_mark_boundaries.csv --reporters cli,junit,json --reporter-junit-export reports/learning.xml --reporter-json-export reports/learning.json
npx newman run postman/collections/quality.postman_collection.json -e postman/environments/local.postman_environment.json -d postman/data/quality_boundaries.csv --reporters cli,junit,json --reporter-junit-export reports/quality.xml --reporter-json-export reports/quality.json
npx newman run postman/collections/workorders.postman_collection.json -e postman/environments/local.postman_environment.json -d postman/data/work_hours_boundaries.csv --reporters cli,junit,json --reporter-junit-export reports/workorders.xml --reporter-json-export reports/workorders.json
```

The milestone copies those three results into `reports/api.xml` and `reports/api.json`. Those combined files are the defect-off execution. The JUnit file has one testsuite per request. The JSON file keeps every CSV iteration. `forceDefects` stays false, so every Disable request runs and the assertions check the M1 rules.

The defect-on command adds `--env-var forceDefects=true`. The same assertions then fail for the six planted switches. See `docs/api_defect_matrix.md`.

## Traceability

`docs/api_traceability.md` maps each requirement and M3 case to the Postman request and the Newman result. `tests/test_postman_contract.py` checks that every request is listed, that the CSV files contain the boundary values, that the environment loads, and that the combined report has no assertion failures.
