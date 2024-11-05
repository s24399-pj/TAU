from time import sleep

from selenium.webdriver.common.by import By

from conftest import driver
from .base_page import BasePage


class FilmwebPage(BasePage):
    RANKING_LINK = (By.ID, "rankingsMenuLink")
    COOKIE_BTN = (By.CSS_SELECTOR, "#didomi-notice-agree-button"),
    ACTION_FILTER = (
    By.XPATH, "/html/body/div[4]/header/div[2]/div[2]/div[3]/div/div/div[2]/ul/li[4]/div/ul/li[2]/a/span")
    FIRST_MOVIE = (By.XPATH, "//a[contains(text(), 'Skazani na Shawshank')]")
    CAST_TAB = (By.XPATH, "/html/body/div[3]/div[3]/div[2]/div[2]/div[7]/section/div[4]/div/a/span")
    REVIEWS_TAB = (By.XPATH, "//a[contains(text(),'Recenzje')]")
    ACTOR_LIST = (By.CLASS_NAME, "actors-list")
    REVIEWS_LIST = (By.CLASS_NAME, "reviews-list")
    CAST_BUTTON = (By.XPATH, "/html/body/div[3]/div[3]/div[2]/div[2]/div[7]/section/div[4]/div/a/span")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.filmweb.pl"

    def open(self):
        self.driver.get(self.url)
        self.click_element(*self.COOKIE_BTN)

    def go_to_ranking(self):
        self.click_element(*self.RANKING_LINK)

    def select_action_genre(self):
        self.click_element(*self.ACTION_FILTER)

    def open_first_movie(self):
        self.click_element(*self.FIRST_MOVIE)

    def go_to_cast(self):
        self.click_element(*self.CAST_BUTTON)

    def go_to_reviews(self):
        self.click_element(*self.REVIEWS_TAB)

    def is_actor_list_visible(self):
        return self.is_element_visible(*self.ACTOR_LIST)

    def is_reviews_list_visible(self):
        return self.is_element_visible(*self.REVIEWS_LIST)

    def scroll_to_cast(self):
        element = self.get_element(*self.CAST_BUTTON)
        self.scroll_to("arguments[0].scrollIntoView();", element)

