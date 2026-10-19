from selenium.webdriver.common.by import By


class OrderLocators:
    ORDER_BTN_TOP = (By.XPATH, "(//button[normalize-space(text())='Заказать'])[1]")
    ORDER_BTN_BOTTOM = (By.XPATH, "(//button[normalize-space(text())='Заказать'])[2]")

    COOKIE_ACCEPT = (By.ID, "rcc-confirm-button")

    FORM_NAME = (By.XPATH, "//input[contains(@placeholder,'Имя')]")
    FORM_SURNAME = (By.XPATH, "//input[contains(@placeholder,'Фамилия')]")
    FORM_ADDRESS = (By.XPATH, "//input[contains(@placeholder,'Адрес')]")
    FORM_PHONE = (By.XPATH, "//input[contains(@placeholder,'Телефон')]")
    STATION_INPUT = (By.CLASS_NAME, "select-search__input")
    BTN_NEXT = (By.XPATH, "//button[normalize-space(text())='Далее']")

    FORM_DATE = (By.XPATH, "//div[contains(@class,'react-datepicker__input-container')]/input")
    RENTAL_PERIOD = (By.XPATH, "(//div[@class='Dropdown-control'])[1]")
    RENTAL_PERIOD_OPTION = (By.XPATH, "(//div[@class='Dropdown-option'])[1]")
    COLOR_BLACK = (By.XPATH, "//input[@id='black']")
    COLOR_GREY = (By.XPATH, "//input[@id='grey']")
    BTN_ORDER = (By.XPATH, "(//button[normalize-space(text())='Заказать'])[last()]")

    ORDER_CONFIRM = (By.XPATH, "//div[text()='Хотите оформить заказ?']")
    SUCCESS_HEADER = (By.XPATH, "//div[contains(@class,'Order_ModalHeader') and contains(., 'Заказ оформлен')]")

    CONFIRM_NO_BTN = (By.XPATH, "(//button[normalize-space(text())='нет' or normalize-space(text())='Нет'])[1]")

    LOGO_SCOOTER = (By.XPATH, "(//a[@href='/'])[1]")
    LOGO_YANDEX = (By.XPATH, "//a[@href='//yandex.ru']")


class FaqLocators:
    QUESTION_BUTTON = (By.XPATH, "//div[@class='accordion__button']")
    ANSWER_PANEL = (By.XPATH, "following::div[@class='accordion__panel'][1]")
