from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from time import sleep


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_element(self, by, value):
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        sleep(1.5)

    def send_keys_to_element(self, by, value, text):
        element = self.wait.until(EC.presence_of_element_located((by, value)))
        element.send_keys(text)
        sleep(1.5)

    def get_element_text(self, by, value):
        element = self.wait.until(EC.presence_of_element_located((by, value)))
        return element.text

    def get_element(self, by, value):
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        return element

    def is_element_visible(self, by, value):
        try:
            self.wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except:
            return False

    def scroll_to(self, script, element):
        self.driver.execute_script(script, element)
        self.driver.execute_script("window.scrollBy(0,-200)", "")

    def select_option_by_visible_text(self, by, value, text):
        """Select an option from a dropdown by visible text."""
        dropdown_element = self.wait.until(EC.element_to_be_clickable((by, value)))
        select = Select(dropdown_element)
        select.select_by_visible_text(text)
        sleep(1.5)
