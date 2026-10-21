from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from helpers.locators import FaqLocators, OrderLocators


class FaqPage(BasePage):
    """Страница FAQ «Вопросы о важном» на главной."""

    def open(self, url):
        self.open_url(url)

    def accept_cookies(self):
        self.click_if_present(OrderLocators.COOKIE_ACCEPT)

    def scroll_to_faq_section(self):
        self.scroll_to_element(FaqLocators.FAQ_SECTION_BUTTON)

    def click_question(self, index):
        self.click_element(FaqLocators.question(index))

    def get_answer_text(self, index) -> str:
        return self.get_text(FaqLocators.answer(index)).strip()
