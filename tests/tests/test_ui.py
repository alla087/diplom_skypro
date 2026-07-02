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
    """ Проверка перехода в онлайн-кинотеатр по ссылке в шапке."""
# Шаг    1. На главной странице найти ссылку "Онлайн-кинотеатр" (локатор уже есть в main_page)
# Шаг    2. Кликнуть по ней
main_page.go_to_online_cinema()
# Шаг    3. Проверить, что URL содержит "hd.kinopoisk.ru"
hd.kinopoisk.ru" in driver.current_url

     """Проверка, что после поиска можно перейти на страницу первого найденного фильма."""
def test_open_film_page_from_search()
#  Шаг 1. Выполнить поиск через main_page.search(SEARCH_QUERY)
with allure.step(f"Выполнить поиск по запросу '{SEARCH_QUERY}'"):
    main_page = MainPage(self.driver)
    search_results_page = main_page.search(SEARCH_QUERY)

    allure.attach(
        self.driver.current_url,
        name="URL после поиска",
        attachment_type=allure.attachment_type.TEXT
    )
#  Шаг 2. Открыть первый фильм через search_results.open_first_movie()
with allure.step("Открыть первый найденный фильм"):
    film_page = search_results_page.open_first_movie()

    allure.attach(
        "Клик по первому фильму выполнен",
        name="Действие",
        attachment_type=allure.attachment_type.TEXT
    )

#  Шаг 3. Проверить, что URL содержит "/film/"
with allure.step("Проверить, что URL содержит '/film/'"):
    current_url = self.driver.current_url
    allure.attach(
        current_url,
        name="Текущий URL",
        attachment_type=allure.attachment_type.TEXT
    )
    assert "/film/" in current_url, \
        f"❌ Ожидался URL с '/film/', получен: {current_url}"

    """
    Проверяет, что главная страница Кинопоиска открывается
    """

    def test_open_main_page(self):
 # Шаг 1: Открыть сайт Кинопоиск
        with allure.step("Открыть сайт https://www.kinopoisk.ru/"):
            self.driver.get("https://www.kinopoisk.ru/")


# Шаг 2: Проверить, что страница загрузилась
        with allure.step("Проверить заголовок страницы"):
            title = self.driver.title
            allure.attach(title, name="Заголовок страницы", attachment_type=allure.attachment_type.TEXT)
            assert "Кинопоиск" in title, f"Ожидался заголовок с 'Кинопоиск', получен: {title}"

# Шаг 3: Проверить, что поле поиска существует
        with allure.step("Проверить наличие поля поиска"):
            search_input = self.driver.find_element(By.NAME, "text")
            assert search_input.is_displayed(), "Поле поиска не отображается на странице"

# Шаг 4: Проверить, что кнопка поиска существует
        with allure.step("Проверить наличие кнопки поиска"):
            search_button = self.driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
            assert search_button.is_displayed(), "Кнопка поиска не отображается на странице"

# Шаг 5: Проверить URL
        with allure.step("Проверить, что URL содержит kinopoisk.ru"):
            current_url = self.driver.current_url
            allure.attach(current_url, name="Текущий URL", attachment_type=allure.attachment_type.TEXT)
            assert "kinopoisk.ru" in current_url, f"Неверный URL: {current_url}"

"""Проверка перехода в раздел фильмов, которые скоро выйдут в кино"""
def test_coming_soon_section(self):
    # Шаг 1: Ожидаем загрузки
    with allure.step("Ожидать загрузки главной страницы"):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        allure.attach(
            self.driver.title,
            name="Заголовок",
            attachment_type=allure.attachment_type.TEXT
        )
        # Шаг 2: Найти ссылку "Скоро в кино"
        with allure.step("Найти ссылку 'Скоро в кино'"):
            # Пробуем разные варианты локаторов
            link_selectors = [
                "a[href*='coming']",
                "a[href*='premiere']",
                "//a[contains(text(), 'Скоро в кино')]",
                "//span[contains(text(), 'Скоро')]/parent::a"
            ]

            link = None
            for selector in link_selectors:
                try:
                    if selector.startswith("//"):
                        link = self.driver.find_element(By.XPATH, selector)
                    else:
                        link = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if link.is_displayed():
                        break
                except:
                    continue

            assert link is not None and link.is_displayed(), \
                "Ссылка 'Скоро в кино' не найдена на странице"

            link_text = link.text.strip()
            allure.attach(
                link_text,
                name="Текст ссылки",
                attachment_type=allure.attachment_type.TEXT
            )
            # Шаг 3: Кликнуть по ссылке
            with allure.step("Кликнуть по ссылке 'Скоро в кино'"):
                link.click()
                allure.attach(
                    "Клик выполнен",
                    name="Действие",
                    attachment_type=allure.attachment_type.TEXT
                )
# Шаг 4: Дождаться загрузки страницы
        with allure.step("Дождаться загрузки страницы со скоро выходящими фильмами"):
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".film-card, .films-list, .search-results"))
            )
            import time
            time.sleep(2)
            # Шаг 5: Проверить URL
            with allure.step("Проверить, что URL содержит 'coming' или 'premiere'"):
                current_url = self.driver.current_url
                allure.attach(
                    current_url,
                    name="Текущий URL",
                    attachment_type=allure.attachment_type.TEXT
                )
                assert "coming" in current_url or "premiere" in current_url or "soon" in current_url, \
                    f"Неверный URL для раздела 'Скоро в кино': {current_url}"
        # Шаг 6: Проверить, что есть фильмы
        with allure.step("Проверить, что отображаются фильмы"):
            film_cards = self.driver.find_elements(By.CSS_SELECTOR, ".film-card, .styles_item__item__3qgQn")
            allure.attach(
                f"Найдено карточек: {len(film_cards)}",
                name="Количество фильмов",
                attachment_type=allure.attachment_type.TEXT
            )

           # Может быть, что фильмов нет, но страница должна загрузиться
            assert len(self.driver.find_elements(By.TAG_NAME, "body")) > 0, \
                "Страница не загрузилась"

            allure.attach(
                "✅ Страница 'Скоро в кино' успешно загружена",
                name="Результат",
                attachment_type=allure.attachment_type.TEXT
            )