from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from helpers.locators import OrderLocators


class OrderPage:
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

    def click_order_top(self):
        self.wait.until(
            EC.element_to_be_clickable(OrderLocators.ORDER_BTN_TOP),
            message="Верхняя кнопка «Заказать» не найдена на главной"
        ).click()

    def click_order_bottom(self):
        self.wait.until(
            EC.element_to_be_clickable(OrderLocators.ORDER_BTN_BOTTOM),
            message="Нижняя кнопка «Заказать» не найдена на главной"
        ).click()

    def select_station(self, station):
        inp = self.wait.until(
            EC.element_to_be_clickable(OrderLocators.STATION_INPUT),
            message="Поле «Станция метро» не найдено или недоступно на первом шаге"
        )
        inp.click()
        inp.send_keys(station)
        inp.send_keys(Keys.ARROW_DOWN)
        inp.send_keys(Keys.ENTER)

        def station_chosen(d):
            value = (inp.get_attribute("value") or "").strip()
            if value != station:
                return False
            uls = d.find_elements(By.XPATH, "//ul[contains(@class,'select-search')]")
            return not uls or not any(u.is_displayed() for u in uls)

        try:
            WebDriverWait(self.driver, 5).until(station_chosen)
        except TimeoutException:
            # запасной путь: клик по кнопке нужной станции в списке
            try:
                btn = WebDriverWait(self.driver, 3).until(
                    lambda d: self.driver.find_elements(
                        By.XPATH,
                        f"//ul[contains(@class,'select-search')]//button[normalize-space()='{station}']"
                    ) or False
                )[0]
                self.driver.execute_script("arguments[0].click();", btn)
                WebDriverWait(self.driver, 5).until(station_chosen)
            except TimeoutException:
                raise TimeoutException(
                    f"Станция не выбралась: в поле {inp.get_attribute('value')!r} "
                    f"вместо «{station}»"
                )

    def fill_first_step(self, name, surname, phone, address, station):
        name_input = self.wait.until(
            EC.visibility_of_element_located(OrderLocators.FORM_NAME),
            message="Поле «Имя» не появилось на первом шаге формы"
        )
        name_input.clear()
        name_input.send_keys(name)

        surname_input = self.wait.until(
            EC.visibility_of_element_located(OrderLocators.FORM_SURNAME),
            message="Поле «Фамилия» не появилось на первом шаге формы"
        )
        surname_input.clear()
        surname_input.send_keys(surname)

        address_input = self.wait.until(
            EC.visibility_of_element_located(OrderLocators.FORM_ADDRESS),
            message="Поле «Адрес» не появилось на первом шаге формы"
        )
        address_input.clear()
        address_input.send_keys(address)

        phone_input = self.wait.until(
            EC.visibility_of_element_located(OrderLocators.FORM_PHONE),
            message="Поле «Телефон» не появилось на первом шаге формы"
        )
        phone_input.clear()
        phone_input.send_keys(phone)

        self.select_station(station)

        self.wait.until(
            EC.element_to_be_clickable(OrderLocators.BTN_NEXT),
            message="Кнопка «Далее» недоступна после заполнения первой части формы"
        ).click()

    def fill_second_step(self, date, color):
        date_input = self.wait.until(
            EC.visibility_of_element_located(OrderLocators.FORM_DATE),
            message="Поле «Когда привезти самокат» не появилось на втором шаге"
        )
        date_input.clear()
        date_input.send_keys(date)
        date_input.send_keys(Keys.ESCAPE)

        self.wait.until(
            EC.element_to_be_clickable(OrderLocators.RENTAL_PERIOD),
            message="Выпадающий список «Срок аренды» не открылся для клика"
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(OrderLocators.RENTAL_PERIOD_OPTION),
            message="Пункт срока аренды не появился в списке"
        ).click()

        if color == "чёрный жемчуг":
            checkbox = self.wait.until(
                EC.presence_of_element_located(OrderLocators.COLOR_BLACK),
                message="Чекбокс «чёрный жемчуг» не найден на втором шаге"
            )
        elif color == "серая безысходность":
            checkbox = self.wait.until(
                EC.presence_of_element_located(OrderLocators.COLOR_GREY),
                message="Чекбокс «серая безысходность» не найден на втором шаге"
            )
        else:
            checkbox = None

        if checkbox is not None and not checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", checkbox)

    def submit_order(self):
        self.wait.until(
            EC.element_to_be_clickable(OrderLocators.BTN_ORDER),
            message="Кнопка «Заказать» на втором шаге недоступна"
        ).click()

    def confirm_order(self):
        title = self.wait.until(
            EC.visibility_of_element_located(OrderLocators.ORDER_CONFIRM),
            message="Окно «Хотите оформить заказ?» не открылось после нажатия «Заказать»"
        )
        modal = title.find_element(By.XPATH, "./ancestor::div[contains(@class,'Order_Modal__')]")

        # «Да» — вторая кнопка в контейнере кнопок окна (разметка стенда),
        # поиск по тексту как запасной вариант, затем по всей странице
        candidates = modal.find_elements(
            By.CSS_SELECTOR, "div.Order_Buttons__1xGrp > button:nth-child(2)"
        )
        if not candidates:
            candidates = modal.find_elements(By.XPATH, ".//button[normalize-space()='Да']")
        if not candidates:
            candidates = self.driver.find_elements(By.XPATH, "//button[normalize-space()='Да']")
        if not candidates:
            raise TimeoutException("Кнопка «Да» не найдена в окне подтверждения")
        yes = candidates[0]

        def success_shown(d):
            headers = d.find_elements(*OrderLocators.SUCCESS_HEADER)
            return any(h.is_displayed() for h in headers)

        def collect_state():
            parts = []
            try:
                dv = self.driver.find_element(*OrderLocators.FORM_DATE).get_attribute("value")
                parts.append(f"дата в поле={dv!r}")
            except Exception:
                parts.append("дата в поле=<не найдено>")
            try:
                sv = self.driver.find_element(
                    By.CLASS_NAME, "select-search__input"
                ).get_attribute("value")
                parts.append(f"станция в поле={sv!r}")
            except Exception:
                parts.append("станция в поле=<не найдено>")
            try:
                rt = self.driver.find_element(*OrderLocators.RENTAL_PERIOD).text
                parts.append(f"срок аренды={rt!r}")
            except Exception:
                parts.append("срок аренды=<не найдено>")
            errors = [
                e.text for e in self.driver.find_elements(
                    By.XPATH, "//*[contains(text(),'Ошибка') or contains(text(),'ошибка')]"
                ) if e.is_displayed() and e.text.strip()
            ]
            parts.append(f"ошибки на странице={errors!r}")
            return "; ".join(parts)

        try:
            yes.click()
            WebDriverWait(self.driver, 10).until(success_shown)
        except TimeoutException:
            diag = collect_state()
            try:
                self.driver.execute_script("arguments[0].click();", yes)
                WebDriverWait(self.driver, 10).until(success_shown)
            except TimeoutException:
                raise TimeoutException(
                    f"Клик «Да» выполнен (обычный и JS), но окно «Заказ оформлен!» не появилось. "
                    f"Кнопка: text={yes.text!r}, class={yes.get_attribute('class')!r}. "
                    f"Состояние формы: {diag}"
                )


    def get_order_number(self):
        header = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(OrderLocators.SUCCESS_HEADER),
            message="Окно «Заказ оформлен!» не появилось после подтверждения заказа"
        )
        modal = header.find_element(By.XPATH, "./ancestor::div[contains(@class,'Order_Modal__')]")
        try:
            WebDriverWait(self.driver, 10).until(lambda d: any(ch.isdigit() for ch in modal.text))
        except TimeoutException:
            raise TimeoutException(
                f"Окно успеха открыто, но цифр в нём нет. Фактический текст окна: {modal.text!r}"
            )
        return modal.text

    def close_success_modal(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(OrderLocators.CONFIRM_NO_BTN)
            ).click()
        except TimeoutException:
            pass

    def click_scooter_logo(self):
        self.close_success_modal()
        logo = self.wait.until(
            EC.presence_of_element_located(OrderLocators.LOGO_SCOOTER),
            message="Логотип «Самоката» не найден в шапке"
        )
        self.driver.execute_script("arguments[0].click();", logo)
        self.wait.until(
            lambda d: d.current_url.rstrip("/") == "https://qa-scooter.praktikum-services.ru",
            message=f"После клика по логотипу «Самоката» открылась не главная, а {self.driver.current_url}"
        )

    def click_yandex_logo(self):
        current_window = self.driver.current_window_handle
        logo = self.wait.until(
            EC.presence_of_element_located(OrderLocators.LOGO_YANDEX),
            message="Логотип Яндекса не найден в шапке"
        )
        self.driver.execute_script("arguments[0].click();", logo)
        self.wait.until(
            lambda d: len(d.window_handles) > 1,
            message="Клик по логотипу Яндекса не открыл новое окно"
        )
        new_window = [w for w in self.driver.window_handles if w != current_window][0]
        self.driver.switch_to.window(new_window)
        self.wait.until(
            lambda d: "dzen" in d.current_url.lower(),
            message=f"Логотип Яндекса не привёл на Дзен, а открыл {self.driver.current_url}"
        )
