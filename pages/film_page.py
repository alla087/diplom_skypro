from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class FilmPage(BasePage):
    TITLE = (By.XPATH, '//h1[contains(@class, "film-title")]')

    @allure.step("Получить название фильма")
    def get_title(self):
        return self.get_text(self.TITLE)
