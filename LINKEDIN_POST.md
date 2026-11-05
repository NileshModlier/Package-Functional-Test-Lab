# LinkedIn post

Copy the body below as the post. The disclaimer stays in the text.

---

I finished a personal portfolio lab I am calling Package Functional Test Lab, and I want to share what the exercise taught me about functional testing.

SIMULATED – Not affiliated with Intellum, Verint, IBM TRIRIGA, or IBM Maximo.

I wanted one repository where a requirement, a test case, a browser check, an API check, and a pipeline result all point at the same rule. The workflows are study models I built from publicly available documentation on learning administration, quality evaluations, and facilities work orders. This is my own study lab. It is not a job at IBM or at a vendor, and I do not claim product access, employment, certification, or partnership.

The hard parts were the ones that usually get smoothed over. Public pages do not always state the threshold, so I wrote assumption IDs and tested those. The running simulator is smaller than the study diagrams, so cases record that difference. A score of exactly 80.00 is a pass only when a planted defect is off, and half-up rounding means 79.995 becomes 80.00 while 79.994 becomes 79.99. I left six known defects in the seed on purpose. The matching tests pass when the switch is off and fail when it stays on.

Stack I actually used: FastAPI and Jinja2 for the simulator, pytest, Playwright on Chromium, Postman collections with Newman, GitHub Actions, JUnit XML, and a small Python review gate. The drafting helper reads the requirement text and proposes missing cases. It does not call an external model. I reviewed every draft. Accepted cases stay design notes and are not executable tests.

Local results I am willing to quote: 27 requirements, 68 test cases, 26 Chromium tests with 0 failures, Newman JUnit 82 tests with 0 failures, and Newman JSON 138 assertions with 0 failed. The 82 and the 138 are the same defect-off run. JUnit folds data-driven iterations into one result per request, and the JSON file keeps every row. Review metrics: 14 proposals, 8 accepted, 4 rejected, 1 duplicate, 1 invalid. A person accepted eight and rejected four, including a draft that expected a cancel status the simulator does not implement.

The GitHub Actions workflow is in the repo and I verified it locally. I have not executed it on GitHub from this machine, so I am not claiming a green hosted check.

Lessons I will reuse: clear a defect flag before the next green run, publish both reporter totals, let a reviewer reject a draft that is grounded in the spec and wrong for the build, and keep a review gate pointed at new drafts so the original catalog is left intact.

#QualityEngineering #FunctionalTesting #TestAutomation #SDET #SoftwareTesting #Playwright #Postman #Newman #GitHubActions #RequirementsEngineering #PortfolioProject
