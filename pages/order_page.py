from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from helpers.locators import OrderLocators


class OrderPage(BasePage):

    def open(self, url):
        self.open_url(url)

    def accept_cookies(self):
        self.click_if_present(OrderLocators.COOKIE_ACCEPT)

    def click_order_top(self):
        self.click_element(OrderLocators.ORDER_BTN_TOP)

    def click_order_bottom(self):
        self.click_element(OrderLocators.ORDER_BTN_BOTTOM)

    def select_station(self, station):
        inp = self.wait_for_visibility(OrderLocators.STATION_INPUT)
        inp.click()
        inp.send_keys(station)
        inp.send_keys(Keys.ARROW_DOWN)
        inp.send_keys(Keys.ENTER)

        def station_chosen(d):
            value = (inp.get_attribute("value") or "").strip()
            if value != station:
                return False
            dropdowns = self.find_all(OrderLocators.STATION_DROPDOWN)
            return not dropdowns or not any(u.is_displayed() for u in dropdowns)

        try:
            self.wait.until(station_chosen)
        except TimeoutException:
            try:
                options = self.make_wait(3).until(
                    lambda d: self.find_all(OrderLocators.station_option(station)) or False
                )
                self.execute_js("arguments[0].click();", options[0])
                self.wait.until(station_chosen)
            except TimeoutException:
                raise TimeoutException(
                    f"Станция не выбралась: в поле {inp.get_attribute('value')!r} "
                    f"вместо «{station}»"
                )

    def fill_first_step(self, name, surname, phone, address, station):
        self.fill_input(OrderLocators.FORM_NAME, name)
        self.fill_input(OrderLocators.FORM_SURNAME, surname)
        self.fill_input(OrderLocators.FORM_ADDRESS, address)
        self.fill_input(OrderLocators.FORM_PHONE, phone)
        self.select_station(station)
        self.click_element(OrderLocators.BTN_NEXT)

    def fill_second_step(self, date, color):
        date_input = self.fill_input(OrderLocators.FORM_DATE, date)
        date_input.send_keys(Keys.ESCAPE)

        self.click_element(OrderLocators.RENTAL_PERIOD)
        self.click_element(OrderLocators.RENTAL_PERIOD_OPTION)

        if color == "чёрный жемчуг":
            checkbox = self.wait_for_element(OrderLocators.COLOR_BLACK)
        elif color == "серая безысходность":
            checkbox = self.wait_for_element(OrderLocators.COLOR_GREY)
        else:
            checkbox = None

        if checkbox is not None and not checkbox.is_selected():
            self.execute_js("arguments[0].click();", checkbox)

    def submit_order(self):
        self.click_element(OrderLocators.BTN_ORDER)

    def confirm_order(self):
        title = self.wait_for_visibility(OrderLocators.ORDER_CONFIRM)
        modal = title.find_element(*OrderLocators.MODAL_ANCESTOR)

        yes_candidates = modal.find_elements(*OrderLocators.YES_BTN_IN_MODAL)
        if not yes_candidates:
            yes_candidates = self.find_all(OrderLocators.YES_BTN_ANY)
        if not yes_candidates:
            raise TimeoutException("Кнопка «Да» не найдена в окне подтверждения")
        yes = yes_candidates[0]


        def success_shown(d):
            return any(h.is_displayed() for h in self.find_all(OrderLocators.SUCCESS_HEADER))

        def collect_state():
            parts = []
            try:
                parts.append(f"дата в поле={self.find_all(OrderLocators.FORM_DATE)[0].get_attribute('value')!r}")
            except IndexError:
                parts.append("дата в поле=<не найдено>")
            try:
                parts.append(f"станция в поле={self.find_all((OrderLocators.STATION_INPUT))[0].get_attribute('value')!r}")
            except IndexError:
                parts.append("станция в поле=<не найдено>")
            try:
                parts.append(f"срок аренды={self.find_all(OrderLocators.RENTAL_PERIOD)[0].text!r}")
            except IndexError:
                parts.append("срок аренды=<не найдено>")
            errors = [
                e.text for e in self.find_all(OrderLocators.DIAG_ERROR)
                if e.is_displayed() and e.text.strip()
            ]

            parts.append(f"ошибки на странице={errors!r}")
            return "; ".join(parts)

        try:
            yes.click()
            self.wait.until(success_shown)
        except TimeoutException:
            diag = collect_state()
            try:
                self.execute_js("arguments[0].click();", yes)
                self.wait.until(success_shown)
            except TimeoutException:
                raise TimeoutException(
                    f"Клик «Да» выполнен (обычный и JS), но окно «Заказ оформлен!» не появилось. "
                    f"Кнопка: text={yes.text!r}, class={yes.get_attribute('class')!r}. "
                    f"Состояние формы: {diag}"
                )

    def get_order_number(self):
        header = self.make_wait(15).until(
            lambda d: self.find_all(OrderLocators.SUCCESS_HEADER)
            and self.find_all(OrderLocators.SUCCESS_HEADER)[0].is_displayed()
            and self.find_all(OrderLocators.SUCCESS_HEADER)[0]
        )
        modal = header.find_element(*OrderLocators.MODAL_ANCESTOR)
        try:
            self.make_wait(10).until(lambda d: any(ch.isdigit() for ch in modal.text))
        except TimeoutException:
            raise TimeoutException(
                f"Окно успеха открыто, но цифр в нём нет. Фактический текст окна: {modal.text!r}"
            )
        return modal.text

    def close_success_modal(self):
        self.click_if_present(OrderLocators.CONFIRM_NO_BTN)

    def click_scooter_logo(self):
        self.close_success_modal()
        self.click_element(OrderLocators.LOGO_SCOOTER)
        self.wait.until(
            lambda d: self.get_current_url().rstrip("/") == "https://qa-scooter.praktikum-services.ru",
            message=f"После клика по логотипу «Самоката» открылась не главная, а {self.get_current_url()}"
        )

    def click_yandex_logo(self):
        current_window = self.get_current_window()
        self.click_element(OrderLocators.LOGO_YANDEX)
        self.switch_to_new_window(current_window)
        self.wait.until(
            lambda d: "dzen" in self.get_current_url().lower(),
            message=f"Логотип Яндекса не привёл на Дзен, а открыл {self.get_current_url()}"
        )
