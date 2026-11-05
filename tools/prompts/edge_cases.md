# Edge-case prompt

The assistant drafts test ideas. It does not change the simulator, the automated suites, or CI, and it does not write an executable test.

Read only:

- the requirement file
- case files that cite that requirement

Use a technique from this list:

- boundary
- negative
- state-transition
- decision-table
- exploratory

Every draft has:

- title
- technique
- steps
- expected
- why
- requirement
- source: ai-draft
- status: proposed
- reviewed_by: null

Grounding:

- States, fields, rules, and concepts must already appear in the requirement or in a case for that requirement.
- A new identifier, code, or field name is invalid.
- A draft that restates an existing case title, or an acceptance criterion a case already cites, is a duplicate.
- Do not invent a threshold, status, or role.

Review:

- A person accepts or rejects each draft.
- Accepted drafts move into cases/ with source ai-draft and a reviewer name.
- Rejected drafts keep a rejection reason.
- Nothing is automated from a draft.
