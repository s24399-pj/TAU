from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class FmicPage(BasePage):
    ENGINE_CATEGORY_BTN = (By.CSS_SELECTOR, "div.block:nth-child(7) > span:nth-child(1) > a:nth-child(1)")
    TURBO_CATEGORY_BTN = (By.XPATH, "(//li[@class='item my-1 first:mt-0'])[1]")
    SELECT_MAKER_DROPDOWN = (By.CSS_SELECTOR, "select.form-select")
    THIRD_PRODUCT = (By.XPATH, "(//a[@class='product-item-link hover:underline'])[4]")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://fmic.pl/"

    def open(self):
        self.driver.get(self.url)

    def go_to_category(self):
        self.click_element(*self.ENGINE_CATEGORY_BTN)

    def go_to_turbo_category(self):
        self.click_element(*self.TURBO_CATEGORY_BTN)

    def select_maker(self, maker_name):
        self.select_option_by_visible_text(*self.SELECT_MAKER_DROPDOWN, maker_name)

    def select_third(self):
        self.click_element(*self.THIRD_PRODUCT)