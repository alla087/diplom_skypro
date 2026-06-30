import pytest
import allure
from pages.main_page import MainPage
from data.test_data import SEARCH_QUERY, EXPECTED_MOVIE


@allure.feature("UI")
@allure.story("Поиск")
@pytest.mark.ui
def test_search_existing_movie(driver):
    """
    Поиск фильма по названию.
    Проверяет, что в результатах поиска есть ожидаемый фильм.
    """
    with allure.step(f'Открыть главную страницу и выполнить поиск "{SEARCH_QUERY}"'):
        main_page = MainPage(driver)
        search_results = main_page.search(SEARCH_QUERY)

    with allure.step(f'Проверить, что фильм "{EXPECTED_MOVIE}" присутствует'):
        assert search_results.is_movie_present(
            EXPECTED_MOVIE
        ), f'Фильм "{EXPECTED_MOVIE}" не найден'

    allure.attach(
        driver.get_screenshot_as_png(),
        name="search_result",
        attachment_type=allure.attachment_type.PNG,
    )

def test_go_to_online_cinema()
#    Проверяет переход в онлайн-кинотеатр по ссылке в шапке.
#
#    Шаги:
#      1. На главной странице найти ссылку "Онлайн-кинотеатр" (локатор уже есть в main_page)
#      2. Кликнуть по ней
main_page.go_to_online_cinema()
#      3. Проверить, что URL содержит "hd.kinopoisk.ru"
hd.kinopoisk.ru" in driver.current_url



def test_open_film_page_from_search()
#    Проверяет, что после поиска можно перейти на страницу первого найденного фильма.
#    Шаги:
#      1. Выполнить поиск через main_page.search(SEARCH_QUERY)
with allure.step(f"Выполнить поиск по запросу '{SEARCH_QUERY}'"):
    main_page = MainPage(self.driver)
    search_results_page = main_page.search(SEARCH_QUERY)

    allure.attach(
        self.driver.current_url,
        name="URL после поиска",
        attachment_type=allure.attachment_type.TEXT
    )
#      2. Открыть первый фильм через search_results.open_first_movie()
with allure.step("Открыть первый найденный фильм"):
    film_page = search_results_page.open_first_movie()

    allure.attach(
        "Клик по первому фильму выполнен",
        name="Действие",
        attachment_type=allure.attachment_type.TEXT
    )

#      3. Проверить, что URL содержит "/film/"
with allure.step("Проверить, что URL содержит '/film/'"):
    current_url = self.driver.current_url
    allure.attach(
        current_url,
        name="Текущий URL",
        attachment_type=allure.attachment_type.TEXT
    )
    assert "/film/" in current_url, \
        f"❌ Ожидался URL с '/film/', получен: {current_url}"




