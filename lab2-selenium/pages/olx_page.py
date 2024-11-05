from selenium.webdriver.common.by import By

from .base_page import BasePage


class OlxPage(BasePage):
    SEARCH_INPUT = (By.ID, "search")
    SEARCH_BUTTON = (By.XPATH, """//*[@id="searchmain-container"]/div[1]/div/div/div/form/div/div[3]/button""")
    CATEGORY_FILTER = (By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/form/div[3]/div[5]/ul/li[6]/a")
    PRICE_MIN_INPUT = (By.NAME, "range-from")
    PRICE_MAX_INPUT = (By.NAME, "range-to")
    SORT_DROPDOWN = (By.ID, "sort-dropdown")
    PRICE_SORT_OPTION = (By.XPATH, "//option[contains(text(),'Najtańsze')]")
    FIRST_RESULT = (By.CLASS_NAME, "offer-wrapper")
    RESULTS_COUNT = (By.CLASS_NAME, "results-count")
    COOKIE_BTN = (By.ID, "onetrust-accept-btn-handler")
    FIFTH_RESULT = (By.XPATH, "(//div[@class='css-l9drzq'])[5]")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.olx.pl"

    def open(self):
        self.driver.get(self.url)
        self.click_element(*self.COOKIE_BTN)

    def search_item(self, item):
        self.send_keys_to_element(*self.SEARCH_INPUT, item)
        self.click_element(*self.SEARCH_BUTTON)

    def select_category(self):
        self.click_element(*self.CATEGORY_FILTER)

    def set_price_range(self, min_price, max_price):
        self.send_keys_to_element(*self.PRICE_MIN_INPUT, min_price)
        self.send_keys_to_element(*self.PRICE_MAX_INPUT, max_price)

    def sort_by_price(self):
        self.click_element(*self.SORT_DROPDOWN)
        self.click_element(*self.PRICE_SORT_OPTION)

    def get_results_count(self):
        return self.get_element_text(*self.RESULTS_COUNT)

    def open_first_result(self):
        self.click_element(*self.FIRST_RESULT)

    def select_fifth_element(self):
        fifth_element = self.get_element(*self.FIFTH_RESULT)
        self.scroll_to("arguments[0].scrollIntoView();", fifth_element)
        self.click_element(*self.FIFTH_RESULT)
