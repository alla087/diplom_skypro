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


@allure.feature("UI")
@allure.story("Навигация")
@pytest.mark.ui
def test_series_link_opens_new_tab(driver):
    """
    Проверяет, что клик по ссылке 'Сериалы' в главном меню открывает новую вкладку,
    а её URL содержит 'series'.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait

    main_page = MainPage(driver)
    main_page.open("https://www.kinopoisk.ru/")

    # Локатор ссылки «Сериалы»
    series_link_locator = (By.XPATH, "//a[contains(text(), 'Сериалы')]")
    series_link = main_page.find_element(series_link_locator)

    # Запоминаем текущие вкладки
    initial_tabs = driver.window_handles

    with allure.step("Кликнуть по ссылке 'Сериалы'"):
        series_link.click()

    with allure.step("Дождаться открытия новой вкладки"):
        WebDriverWait(driver, 10).until(
            lambda d: len(d.window_handles) > len(initial_tabs)
        )

    # Переключаемся на новую вкладку
    new_tab = [tab for tab in driver.window_handles if tab not in initial_tabs][0]
    driver.switch_to.window(new_tab)

    with allure.step("Проверить, что URL новой вкладки содержит 'series'"):
        assert (
            "series" in driver.current_url
        ), f"Ожидался URL с 'series', получен {driver.current_url}"

    # Закрываем новую вкладку и возвращаемся на исходную (чистота)
    driver.close()
    driver.switch_to.window(initial_tabs[0])

    @allure.feature("UI")
    @allure.story("Навигация")
    @pytest.mark.ui
    def test_films_link_opens_new_tab(driver):
        """
        Проверяет, что клик по ссылке 'Фильмы' в главном меню открывает новую вкладку,
        а её URL содержит 'film' или 'movies'.
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait

        main_page = MainPage(driver)
        main_page.open("https://www.kinopoisk.ru/")

        # Локатор ссылки «Фильмы»
        films_link_locator = (By.XPATH, "//a[contains(text(), 'Фильмы')]")
        films_link = main_page.find_element(films_link_locator)

        initial_tabs = driver.window_handles

        with allure.step("Кликнуть по ссылке 'Фильмы'"):
            films_link.click()

        with allure.step("Дождаться открытия новой вкладки"):
            WebDriverWait(driver, 10).until(
                lambda d: len(d.window_handles) > len(initial_tabs)
            )

        new_tab = [tab for tab in driver.window_handles if tab not in initial_tabs][0]
        driver.switch_to.window(new_tab)

        with allure.step(
            "Проверить, что URL новой вкладки содержит 'film' или 'movies'"
        ):
            current_url = driver.current_url
            assert (
                "film" in current_url or "movies" in current_url
            ), f"Ожидался URL с 'film' или 'movies', получен {current_url}"

        # Закрываем новую вкладку и возвращаемся на исходную
        driver.close()
        driver.switch_to.window(initial_tabs[0])

    @allure.feature("UI")
    @allure.story("Навигация")
    @pytest.mark.ui
    def test_news_link_opens_new_tab(driver):
        """
        Проверяет, что клик по ссылке 'Новости' в главном меню открывает новую вкладку,
        а её URL содержит 'news'.
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait

        main_page = MainPage(driver)
        main_page.open("https://www.kinopoisk.ru/")

        # Локатор ссылки «Новости» - возможно, в меню это есть
        news_link_locator = (By.XPATH, "//a[contains(text(), 'Новости')]")
        news_link = main_page.find_element(news_link_locator)

        initial_tabs = driver.window_handles

        with allure.step("Кликнуть по ссылке 'Новости'"):
            news_link.click()

        with allure.step("Дождаться открытия новой вкладки"):
            WebDriverWait(driver, 10).until(
                lambda d: len(d.window_handles) > len(initial_tabs)
            )

        new_tab = [tab for tab in driver.window_handles if tab not in initial_tabs][0]
        driver.switch_to.window(new_tab)

        with allure.step("Проверить, что URL новой вкладки содержит 'news'"):
            current_url = driver.current_url
            assert (
                "news" in current_url
            ), f"Ожидался URL с 'news', получен {current_url}"

        driver.close()
        driver.switch_to.window(initial_tabs[0])


@allure.feature("UI")
@allure.story("Навигация")
@pytest.mark.ui
def test_ratings_link_opens_new_tab(driver):
    """
    Проверяет, что клик по ссылке 'Рейтинги' в главном меню открывает новую вкладку,
    а её URL содержит 'rating' или 'top'.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait

    main_page = MainPage(driver)
    main_page.open("https://www.kinopoisk.ru/")

    # Локатор ссылки «Рейтинги»
    ratings_link_locator = (By.XPATH, "//a[contains(text(), 'Рейтинги')]")
    ratings_link = main_page.find_element(ratings_link_locator)

    # Запоминаем текущие вкладки
    initial_tabs = driver.window_handles

    with allure.step("Кликнуть по ссылке 'Рейтинги'"):
        ratings_link.click()

    with allure.step("Дождаться открытия новой вкладки"):
        WebDriverWait(driver, 10).until(
            lambda d: len(d.window_handles) > len(initial_tabs)
        )

    # Переключаемся на новую вкладку
    new_tab = [tab for tab in driver.window_handles if tab not in initial_tabs][0]
    driver.switch_to.window(new_tab)

    with allure.step("Проверить, что URL новой вкладки содержит 'rating' или 'top'"):
        current_url = driver.current_url
        assert (
            "rating" in current_url or "top" in current_url
        ), f"Ожидался URL с 'rating' или 'top', получен {current_url}"

    # Закрываем новую вкладку и возвращаемся на исходную
    driver.close()
    driver.switch_to.window(initial_tabs[0])
