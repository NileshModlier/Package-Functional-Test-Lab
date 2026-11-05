"""Quality evaluation page. Locators are data-testid values."""

from playwright.sync_api import Page, expect


class EvaluationPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self) -> None:
        self.page.goto("/quality")

    def evaluation(self, evaluation_id: str):
        return self.page.get_by_test_id(f"evaluation-{evaluation_id}")

    def submit(self, evaluation_id: str, earned_a: str, earned_b: str, earned_c: str) -> None:
        card = self.evaluation(evaluation_id)
        card.get_by_test_id("earned-a").fill(earned_a)
        card.get_by_test_id("earned-b").fill(earned_b)
        card.get_by_test_id("earned-c").fill(earned_c)
        card.get_by_test_id("submit").click()

    def acknowledge(self, evaluation_id: str) -> None:
        self.evaluation(evaluation_id).get_by_test_id("acknowledge").click()

    def dispute(self, evaluation_id: str, comment: str) -> None:
        card = self.evaluation(evaluation_id)
        card.get_by_test_id("dispute-comment").fill(comment)
        card.get_by_test_id("dispute").click()

    def coach(self, evaluation_id: str, note: str) -> None:
        card = self.evaluation(evaluation_id)
        card.get_by_test_id("coach-note").fill(note)
        card.get_by_test_id("coach").click()

    def expect_state(self, evaluation_id: str, state: str) -> None:
        expect(self.evaluation(evaluation_id).get_by_test_id("state")).to_have_text(state)

    def expect_summary_contains(self, evaluation_id: str, text: str) -> None:
        expect(self.evaluation(evaluation_id).get_by_test_id("summary")).to_contain_text(text)

    def expect_acknowledge_absent(self, evaluation_id: str) -> None:
        expect(self.evaluation(evaluation_id).get_by_test_id("acknowledge")).to_have_count(0)
