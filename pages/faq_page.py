from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from helpers.locators import OrderLocators


class FaqPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        self.driver.get(url)

    def accept_cookies(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(OrderLocators.COOKIE_ACCEPT)
            ).click()
        except TimeoutException:
            pass

    def scroll_to_faq_section(self):
        section = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='accordion__button']")
            ),
            message="Блок «Вопросы о важном» не найден на главной"
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", section)

    def click_question(self, index):
        btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[@id='accordion__heading-{index}']")
            ),
            message=f"Вопрос №{index} не найден или недоступен для клика"
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        try:
            btn.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", btn)

    def get_answer_text(self, index):
        panel = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//div[@id='accordion__panel-{index}']")
            ),
            message=f"Ответ №{index} не раскрылся после клика по вопросу"
        )
        return panel.text.strip()
