from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Общий родитель для всех страниц проекта.

    Всё обращение к драйверу живёт только здесь: ожидания,
    прокрутка, клики, чтение текста и атрибутов, работа с окнами.
    Страницы-наследники вызывают только эти методы.
    """

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- навигация -------------------------------------------------------

    def open_url(self, url):
        """Открывает страницу по адресу."""
        self.driver.get(url)

    def get_current_url(self) -> str:
        """Возвращает адрес текущей страницы."""
        return self.driver.current_url

    # --- поиск и ожидания ---------------------------------------------------

    def make_wait(self, timeout: int = 10):
        """Отдельное ожидание с нестандартным таймаутом (для мелких сценариев)."""
        return WebDriverWait(self.driver, timeout)

    def wait_for_element(self, locator):
        """Ждёт появления элемента в DOM и возвращает его."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_visibility(self, locator):
        """Ждёт, пока элемент станет видимым, и возвращает его."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        """Возвращает список элементов (может быть пустым, без ожиданий)."""
        return self.driver.find_elements(*locator)

    def fill_input(self, locator, text):
        """Ждёт видимости поля, очищает и вводит текст."""
        element = self.wait_for_visibility(locator)
        element.clear()
        element.send_keys(text)
        return element

    # --- прокрутка и клики ---------------------------------------------------

    def scroll_to_element(self, locator):
        """Прокручивает страницу до элемента и возвращает кликабельный элемент.

        Прокрутка через JS-скрипт: стандартный scrollIntoView не всегда
        срабатывает, если элемент перекрыт закреплённой шапкой сайта.
        """
        element = self.wait_for_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click_element(self, locator):
        """Прокручивает до элемента и кликает по-настоящему (как пользователь).

        Если клик перехватил другой элемент — повторяет через JS.
        """
        element = self.scroll_to_element(locator)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
        return element

    def click_if_present(self, locator, timeout: int = 3):
        """Кликает по элементу, если он появился, иначе молча пропускает.

        Для необязательных действий: согласие на куки, закрытие модалок.
        """
        try:
            self.make_wait(timeout).until(
                EC.element_to_be_clickable(locator)
            ).click()
            return True
        except TimeoutException:
            return False

    def get_text(self, locator) -> str:
        """Возвращает текст элемента после прокрутки до него."""
        return self.scroll_to_element(locator).text

    # --- скрипты и окна -------------------------------------------------------

    def execute_js(self, script, *args):
        """Выполняет JS-скрипт с передачей элементов-аргументов."""
        return self.driver.execute_script(script, *args)

    def get_current_window(self):
        """Возвращает идентификатор текущей вкладки."""
        return self.driver.current_window_handle

    def switch_to_new_window(self, current_handle):
        """Ждёт появления новой вкладки и переключается на неё."""
        self.wait.until(lambda d: len(d.window_handles) > 1)
        new_window = [w for w in self.driver.window_handles if w != current_handle][0]
        self.driver.switch_to.window(new_window)
        return new_window
