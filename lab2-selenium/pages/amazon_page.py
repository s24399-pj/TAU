from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AmazonPage(BasePage):
    COOKIE_BTN = (By.XPATH, "//input[@id='sp-cc-accept']")
    SEARCH_INPUT = (By.XPATH, "//input[@id='twotabsearchtextbox']")
    SEARCH_APPLY_BTN = (By.XPATH, "//input[@id='nav-search-submit-button']")
    FIRST_RESULT_ITEM = (By.XPATH, "(//a[contains(@class, 'a-link-normal') and contains(@class, 's-link-style')])[2]")
    ADD_TO_CART_BTN = (By.XPATH, "//input[@id='add-to-cart-button']")
    GO_TO_CART_BTN = (By.XPATH, "//span[@id='sw-gtc']")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.amazon.pl"

    def open(self):
        self.driver.get(self.url)
        self.click_element(*self.COOKIE_BTN)

    def search_item(self, item):
        self.send_keys_to_element(*self.SEARCH_INPUT, item)
        self.click_element(*self.SEARCH_APPLY_BTN)

    def click_first_result(self):
        self.click_element(*self.FIRST_RESULT_ITEM)

    def add_to_cart(self):
        self.click_element(*self.ADD_TO_CART_BTN)

    def go_to_cart(self):
        self.click_element(*self.GO_TO_CART_BTN)