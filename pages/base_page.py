from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open_url(self, url):
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url


    def make_wait(self, timeout: int = 10):
        return WebDriverWait(self.driver, timeout)

    def wait_for_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_visibility(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def fill_input(self, locator, text):
        element = self.wait_for_visibility(locator)
        element.clear()
        element.send_keys(text)
        return element


    def scroll_to_element(self, locator):
        element = self.wait_for_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click_element(self, locator):
        element = self.scroll_to_element(locator)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
        return element

    def click_if_present(self, locator, timeout: int = 3):
        try:
            self.make_wait(timeout).until(
                EC.element_to_be_clickable(locator)
            ).click()
            return True
        except TimeoutException:
            return False

    def get_text(self, locator) -> str:
        return self.scroll_to_element(locator).text


    def execute_js(self, script, *args):
        return self.driver.execute_script(script, *args)

    def get_current_window(self):
        return self.driver.current_window_handle

    def switch_to_new_window(self, current_handle):
        self.wait.until(lambda d: len(d.window_handles) > 1)
        new_window = [w for w in self.driver.window_handles if w != current_handle][0]
        self.driver.switch_to.window(new_window)
        return new_window
