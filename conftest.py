import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT = 10
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    yield driver
    driver.quit()


@pytest.fixture()
def wait(driver):
    return WebDriverWait(driver, TIMEOUT)
