# tools

`ci_summary.py` reads JUnit XML and writes `reports/summary.md`, the combined Newman report, and `trace/regression_status.md`.

`--check` fails when a requirement has no case, an automated test names a missing case, or a planted defect is not wired to an assertion.

`ai_assistant.py` drafts proposals from requirement files and existing cases. `propose` writes `proposals/` only. `review` accepts a draft into a new case file or rejects it into `proposals/rejected/`.

`check_reviewed.py` fails when an `ai-draft` case has no reviewer, no requirement, no source, or an invalid id. Catalog cases with no `source` field are left alone.

`prompts/edge_cases.md` is the constraint list the drafter loads before it writes.
