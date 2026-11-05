"""Work-order page. Locators are data-testid values."""

from playwright.sync_api import Page, expect


class WorkOrderPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self) -> None:
        self.page.goto("/workorders")

    def order(self, order_id: str):
        return self.page.get_by_test_id(f"order-{order_id}")

    def transition(self, order_id: str, target: str, actor_id: str | None = None, reason: str | None = None) -> None:
        card = self.order(order_id)
        card.get_by_test_id("transition-to").select_option(target)
        if actor_id is not None:
            card.get_by_test_id("actor").fill(actor_id)
        if reason is not None:
            card.get_by_test_id("reason").fill(reason)
        card.get_by_test_id("apply").click()

    def assign(self, order_id: str, technician_id: str) -> None:
        card = self.order(order_id)
        card.get_by_test_id("technician").select_option(technician_id)
        card.get_by_test_id("assign").click()

    def expect_state(self, order_id: str, state: str) -> None:
        expect(self.order(order_id).get_by_test_id("state")).to_have_text(state)

    def expect_assignment_contains(self, order_id: str, text: str) -> None:
        expect(self.order(order_id).get_by_test_id("assignment")).to_contain_text(text)

    def expect_error(self, text: str) -> None:
        expect(self.page.get_by_test_id("error")).to_contain_text(text)
