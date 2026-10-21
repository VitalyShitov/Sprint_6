import pytest
import allure

from urls import BASE_URL, ORDER_URL


@allure.feature("Заказ самоката")
class TestOrderFlow:
    """Полный позитивный сценарий заказа самоката."""

    @allure.story("Полный позитивный сценарий заказа")
    @pytest.mark.parametrize(
        "entry_point, name, surname, phone, address, station, date, color",
        [
            pytest.param(
                "top", "Иван", "Иванов", "+79990000001",
                "Москва, ул. Примерная, д. 1", "Тверская",
                "01.11.2026", "чёрный жемчуг",
                id="top_test_order_1",
            ),
            pytest.param(
                "bottom", "Пётр", "Петров", "+79990000002",
                "Москва, ул. Тестовая, д. 2", "Охотный Ряд",
                "02.11.2026", "серая безысходность",
                id="bottom_test_order_2",
            ),
        ],
    )
    def test_order_full_flow(self, order_page, entry_point, name, surname, phone,
                             address, station, date, color):
        with allure.step(f"Нажимаем кнопку «Заказать» ({entry_point})"):
            if entry_point == "top":
                order_page.click_order_top()
            else:
                order_page.click_order_bottom()

        with allure.step("Заполняем форму заказа: первая часть"):
            order_page.fill_first_step(name, surname, phone, address, station)

        with allure.step("Заполняем форму заказа: вторая часть"):
            order_page.fill_second_step(date, color)

        with allure.step("Отправляем заказ"):
            order_page.submit_order()

        with allure.step("Подтверждаем заказ"):
            order_page.confirm_order()

        with allure.step("Проверяем всплывающее окно об успешном создании заказа"):
            order_number = order_page.get_order_number()
            assert any(ch.isdigit() for ch in order_number), \
                f"В окне успеха нет номера заказа, текст: {order_number!r}"


@allure.feature("Логотипы в шапке")
class TestHeaderLogos:
    """Переходы по логотипам в шапке сайта."""

    @allure.story("Логотип «Самоката» возвращает на главную")
    def test_scooter_logo_redirect(self, order_page):
        order_page.open(ORDER_URL)
        order_page.click_scooter_logo()
        assert order_page.get_current_url().rstrip("/") == BASE_URL.rstrip("/"), \
            f"После клика по логотипу «Самоката» открылась не главная, а {order_page.get_current_url()}"

    @allure.story("Логотип Яндекса открывает Дзен в новом окне")
    def test_yandex_logo_redirect(self, order_page):
        order_page.open(BASE_URL)
        order_page.click_yandex_logo()
        assert "dzen" in order_page.get_current_url().lower(), \
            f"Логотип Яндекса не привёл на Дзен, а открыл {order_page.get_current_url()}"
