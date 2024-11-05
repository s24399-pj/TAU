# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="firefox", help="Browser to use for test execution"
    )

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    if browser == "firefox":
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    elif browser == "chrome":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif browser == "edge":
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    else:
        raise ValueError(f"Przeglądarka '{browser}' nie jest obsługiwana. Użyj 'firefox', 'chrome' lub 'edge'.")

    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
