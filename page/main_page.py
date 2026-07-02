import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.search_results_page import SearchResultsPage
from pages.profile_page import ProfilePage


class MainPage(BasePage):
    SEARCH_INPUT = (By.NAME, "text")
    SEARCH_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')
    ONLINE_CINEMA_LINK = (By.CSS_SELECTOR, "a[href*='hd.kinopoisk.ru']")
    YEAR_SELECT = (By.CSS_SELECTOR, "select[name='year']")
    GENRE_SELECT = (By.CSS_SELECTOR, "select[name='genre']")
    APPLY_FILTER_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    @allure.step('Поиск фильма по названию "{query}"')
    def search(self, query):
        self.input_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        return SearchResultsPage(self.driver)

    @allure.step("Перейти в онлайн-кинотеатр")
    def go_to_online_cinema(self):
        self.click(self.ONLINE_CINEMA_LINK)

    @allure.step('Выбрать год "{year}" и жанр "{genre}"')
    def select_year_and_genre(self, year, genre):
        from selenium.webdriver.support.ui import Select

        year_select = Select(self.find_element(self.YEAR_SELECT))
        year_select.select_by_visible_text(str(year))
        genre_select = Select(self.find_element(self.GENRE_SELECT))
        genre_select.select_by_visible_text(genre)

    @allure.step("Применить фильтр")
    def apply_filter(self):
        self.click(self.APPLY_FILTER_BUTTON)
