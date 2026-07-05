from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.film_page import FilmPage
import allure


class SearchResultsPage(BasePage):
    FIRST_MOVIE_LINK = (By.XPATH, '(//div[contains(@class, "film-card")]//a)[1]')
    FILM_CARDS = (By.CSS_SELECTOR, ".film-card")

    @allure.step("Открыть первый найденный фильм")
    def open_first_movie(self):
        self.click(self.FIRST_MOVIE_LINK)
        return FilmPage(self.driver)

    @allure.step('Проверить наличие фильма "{title}" в результатах')
    def is_movie_present(self, title):
        return title in self.driver.page_source

    @allure.step("Получить список карточек фильмов")
    def get_film_cards(self, limit=5):
        return self.driver.find_elements(*self.FILM_CARDS)[:limit]
