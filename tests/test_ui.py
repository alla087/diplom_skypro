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


@allure.feature("UI")
@allure.story("Поиск")
@pytest.mark.ui
def test_search_empty_query(driver):
    """
    Негативный тест: поиск с пустым запросом.
    Ожидаем, что результаты не отображаются (список карточек пуст).
    """
    main_page = MainPage(driver)
    main_page.open("https://www.kinopoisk.ru/")

    with allure.step("Выполнить поиск с пустой строкой"):
        search_results = main_page.search("")

    with allure.step("Проверить, что карточки фильмов отсутствуют"):
        cards = search_results.get_film_cards(limit=10)
        assert len(cards) == 0, f"Найдено карточек: {len(cards)}, ожидалось 0"


@allure.feature("API")
@allure.story("Поиск фильмов")
@pytest.mark.api
def test_search_non_existent(api_client):
    """
    Негативный тест: поиск по несуществующему запросу.
    Ожидаем статус 200, пустой список docs и total = 0.
    """
    with allure.step(f'Отправить запрос на поиск "{NON_EXISTENT_QUERY}"'):
        response = api_client.search_movie(NON_EXISTENT_QUERY)

    with allure.step("Проверить статус-код 200"):
        assert (
            response.status_code == 200
        ), f"Ожидался 200, получен {response.status_code}"

    data = response.json()

    with allure.step('Проверить, что поле "docs" – пустой список'):
        assert data.get("docs") == [], 'Поле "docs" не пустое'

    with allure.step('Проверить, что поле "total" равно 0'):
        assert data.get("total") == 0, f'Ожидался total=0, получен {data.get("total")}'


@allure.feature("API")
@allure.story("Фильтрация")
@pytest.mark.api
def test_movies_by_year_and_genre(api_client):
    """
    Позитивный тест: фильтрация по году и жанру.
    Проверяем, что первые 5 фильмов соответствуют заданным году и жанру.
    """
    with allure.step(
        f'Отправить запрос с годом {YEAR_FOR_FILTER} и жанром "{GENRE_FOR_FILTER}"'
    ):
        response = api_client.get_movies_by_year_and_genre(
            YEAR_FOR_FILTER, GENRE_FOR_FILTER
        )

    with allure.step("Проверить статус-код 200"):
        assert (
            response.status_code == 200
        ), f"Ожидался 200, получен {response.status_code}"

    data = response.json()
    docs = data.get("docs", [])

    with allure.step("Проверить, что список фильмов не пуст"):
        assert len(docs) > 0, "Список фильмов пуст"

    with allure.step("Проверить год и жанр у первых 5 фильмов"):
        for film in docs[:5]:
            assert (
                film.get("year") == YEAR_FOR_FILTER
            ), f"Ожидался год {YEAR_FOR_FILTER}, получен {film.get('year')}"
            genres = [g.get("name") for g in film.get("genres", [])]
            assert (
                GENRE_FOR_FILTER in genres
            ), f'Жанр "{GENRE_FOR_FILTER}" не найден в {genres}'


@allure.feature("UI")
@allure.story("Поиск")
@pytest.mark.ui
def test_search_non_existent(driver):
    """
    Негативный тест: поиск по несуществующему запросу.
    Ожидаем, что карточки фильмов отсутствуют (или появляется сообщение об отсутствии).
    """
    from data.test_data import NON_EXISTENT_QUERY

    main_page = MainPage(driver)
    main_page.open("https://www.kinopoisk.ru/")

    with allure.step(f'Выполнить поиск по запросу "{NON_EXISTENT_QUERY}"'):
        search_results = main_page.search(NON_EXISTENT_QUERY)

    with allure.step("Проверить, что результаты поиска пусты"):
        # Проверяем, что нет ни одной карточки фильма
        cards = search_results.get_film_cards(limit=10)
        assert len(cards) == 0, f"Найдено карточек: {len(cards)}, ожидалось 0"
