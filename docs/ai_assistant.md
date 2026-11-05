# AI test assistant

**Milestone:** M7
**Identifier:** SIMULATED

The assistant drafts missing edge cases from written requirements and the existing catalog. A person reviews every draft. The tool does not call an external model, and it does not change the simulator, the Playwright suite, the Postman collections, or the CI test commands.

## Architecture

```text
requirements/*.md
cases/*.yaml
        │
        ▼
tools/prompts/edge_cases.md
        │
        ▼
tools/ai_assistant.py propose
        │
        ├── invalid or duplicate  → counted, not written
        └── proposals/REQ-XXX-NN.yaml   status: proposed
                    │
                    ▼
            human review
              ├── accept → new cases/TC-*.yaml
              └── reject → proposals/rejected/
                    │
                    ▼
        tools/check_reviewed.py
        (GitHub Actions step, before the suites)
```

`propose` reads the prompt, then one requirement and the cases that cite it. It drafts at most two acceptance criteria that no case cites. On the first requirement it also builds two contrast drafts: a copy of an existing title, and a draft that introduces `biometric_signature`. Those two exist so the validator is exercised on every run. They are counted and then dropped.

`review` is the only path from a draft to a case. Accept writes a new `TC-*.yaml` and deletes the proposal. Reject stores the reason under `proposals/rejected/`. The tool refuses to overwrite an existing case file.

## Prompt strategy

`tools/prompts/edge_cases.md` is loaded before any draft is written. The file must name the five techniques and must require `reviewed_by`. The techniques are `boundary`, `negative`, `state-transition`, `decision-table`, and `exploratory`.

Each surviving draft copies one acceptance-criterion sentence into the title, the step, and the expected result. The `why` line names the criterion id and says no existing case cites it. The drafter does not invent steps, data, or status values beyond that sentence.

## Validation strategy

Three checks run before a file is written.

| Check | Rule | Result |
| --- | --- | --- |
| Schema | `source` is `ai-draft`, `status` is `proposed`, `reviewed_by` is null, the technique is one of the five names, the requirement id matches `REQ-INT`, `REQ-VER`, or `REQ-TRI`, and title, steps, expected, and why are present | `invalid` |
| Terminology | Backtick phrases, short all-caps tokens, numbers, and snake_case names in the draft must already appear in the requirement or in a case for that requirement | `invalid` |
| Duplicate | The criterion id is already cited, or the normalized title matches an existing case for that requirement | `duplicate` |

`proposals/metrics.yaml` records `proposals_generated`, `accepted`, `rejected`, `duplicates`, `invalid`, and `acceptance_rate`. The rate is accepted divided by generated.

## Review process

1. The drafter writes `proposals/REQ-XXX-NN.yaml` with `status: proposed` and `reviewed_by: null`.
2. A person runs `python tools/ai_assistant.py review <file> --decision accept|reject --reviewer "Lab reviewer"`.
3. Accept moves the idea into a new case. The case keeps `source: ai-draft`, sets `reviewed_by`, sets `automation_intent: not-executable`, and leaves `execution.automated` false.
4. Reject moves the file to `proposals/rejected/` and stores `rejection_reason`.
5. `python tools/check_reviewed.py` fails the build when an `ai-draft` case has no reviewer, no requirement, no source, or an invalid id, or when an accepted draft is still sitting in `proposals/`. Catalog cases from M3 have no `source` field and are not gated.

## Limitations

- The drafter is deterministic. It restates an uncited acceptance criterion. It does not explore combinations the requirement text does not already state.
- It does not call an external model. Replacing the sentence copy with a model would still have to pass the same schema, terminology, duplicate, and human-review gates.
- A grounded sentence can still be the wrong case for this build. `CAN`, unread scopes, and `started_at` are in the requirements, so the drafter may propose them. Review rejects them when an existing case already records that this build does not store or expose that behavior.
- Accepted cases are design records. They are not Playwright tests, Newman requests, or simulator changes.
- The next CI run is what adds the new cases to `trace/regression_status.md` as Not run. This milestone did not regenerate that file and did not execute the workflow on GitHub.
