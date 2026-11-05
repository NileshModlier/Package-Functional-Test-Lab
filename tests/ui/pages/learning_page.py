"""Learning page. Locators are data-testid values."""

from playwright.sync_api import Page, expect


class LearningPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self) -> None:
        self.page.goto("/learning")

    def enrollment(self, enrollment_id: str):
        return self.page.get_by_test_id(f"enrollment-{enrollment_id}")

    def enroll(self, learner_id: str, activity_id: str) -> None:
        self.page.get_by_test_id("enroll-learner").select_option(learner_id)
        self.page.get_by_test_id("enroll-activity").select_option(activity_id)
        self.page.get_by_test_id("enroll-submit").click()

    def start(self, enrollment_id: str) -> None:
        self.enrollment(enrollment_id).get_by_test_id("start").click()

    def submit_score(self, enrollment_id: str, score: str) -> None:
        card = self.enrollment(enrollment_id)
        card.get_by_test_id("score").fill(score)
        card.get_by_test_id("score-submit").click()

    def complete(self, enrollment_id: str) -> None:
        self.enrollment(enrollment_id).get_by_test_id("complete").click()

    def expect_state(self, enrollment_id: str, state: str) -> None:
        expect(self.enrollment(enrollment_id).get_by_test_id("state")).to_have_text(state)

    def expect_summary_contains(self, enrollment_id: str, text: str) -> None:
        expect(self.enrollment(enrollment_id).get_by_test_id("summary")).to_contain_text(text)

    def expect_module(self, enrollment_id: str, module_id: str, text: str) -> None:
        expect(self.enrollment(enrollment_id).get_by_test_id(f"module-{module_id}")).to_contain_text(text)

    def expect_complete_absent(self, enrollment_id: str) -> None:
        expect(self.enrollment(enrollment_id).get_by_test_id("complete")).to_have_count(0)

    def expect_error(self, text: str) -> None:
        expect(self.page.get_by_test_id("error")).to_contain_text(text)

    def expect_certificate_dates_match(self, learner_id: str) -> None:
        row = self.page.locator("[data-testid^='certificate-row-']").filter(has_text=learner_id)
        expect(row).to_be_visible()
        completed = row.get_by_test_id("certificate-completed").inner_text()
        expect(row.get_by_test_id("certificate-issued")).to_have_text(completed)
