Автоматизация тестирования учебного стенда [qa-scooter.praktikum-services.ru](https://qa-scooter.praktikum-services.ru/).

## Структура проекта

- `tests/` — тестовые сценарии (флоу заказа, FAQ);
- `pages/` — Page Object-модели страниц (`order_page.py`, `faq_page.py`);
- `helpers/locators.py` — локаторы элементов;
- `conftest.py` — фикстуры pytest (драйвер, открытие страниц, принятие куки).

Тесты выполняются в Firefox. Установленный Firefox обязателен: geckodriver подбирается автоматически через Selenium Manager.