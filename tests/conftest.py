import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pages.faq_page import FaqPage
from pages.order_page import OrderPage

from urls import BASE_URL


@pytest.fixture
def driver():
    options = Options()
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def faq_page(driver):
    page = FaqPage(driver)
    page.open(BASE_URL)
    page.accept_cookies()
    return page


@pytest.fixture
def order_page(driver):
    page = OrderPage(driver)
    page.open(BASE_URL)
    page.accept_cookies()
    return page
