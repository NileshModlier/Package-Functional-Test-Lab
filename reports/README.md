# reports/

These files are the local defect-off regression. GitHub Actions writes a fresh copy on each run and uploads it as `regression-reports`.

| File | Result |
| --- | --- |
| `ui.xml` | Playwright JUnit. 26 tests, 0 failures. |
| `api.xml` | Newman JUnit. 82 tests, 0 failures. |
| `api.json` | Newman JSON for the three collections. |
| `summary.md` | The result table. |

A manual run with `force_defects=true` is expected to fail. Do not replace these files with that run.
