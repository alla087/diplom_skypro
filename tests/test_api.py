import pytest
import allure
import json
from data.test_data import (
    API_SEARCH_QUERY,
    INVALID_API_KEY,
    NON_EXISTENT_QUERY,
    YEAR_FOR_FILTER,
    GENRE_FOR_FILTER,
    RATING_MIN,
    RATING_MAX,
)
from api.api_client import APIClient


@allure.feature("api")
@allure.story("Поиск")
@pytest.mark.api
def test_search_movie_by_name(api_client):
    """
    Поиск фильма по названию.
    Проверяет, что запрос возвращает статус 200 и список фильмов не пуст.
    """
    with allure.step(f'Отправить запрос на поиск фильма "{API_SEARCH_QUERY}"'):
        response = api_client.search_movie(API_SEARCH_QUERY)

    with allure.step("Проверить статус-код 200"):
        assert (
            response.status_code == 200
        ), f"Ожидался 200, получен {response.status_code}"

    resp_body = response.json()

    with allure.step('Проверить, что ответ содержит поле "docs"'):
        assert "docs" in resp_body, 'Ответ не содержит поле "docs"'

    with allure.step("Проверить, что список фильмов не пуст"):
        assert len(resp_body["docs"]) > 0, "Список фильмов пуст"

    allure.attach(
        json.dumps(resp_body, indent=4, ensure_ascii=False),
        name="api Response",
        attachment_type=allure.attachment_type.JSON,
    )


@allure.feature("API")
@allure.story("Авторизация")
@pytest.mark.api
def test_invalid_token():
    """
    Негативный тест: запрос с неверным API-ключом.
    Ожидаем статус 401 и сообщение об ошибке.
    """
    with allure.step("Создать клиента с недействительным ключом"):
        bad_client = APIClient(api_key=INVALID_API_KEY)

    with allure.step("Отправить запрос на поиск фильма 'Матрица'"):
        response = bad_client.search_movie("Матрица")

    with allure.step("Проверить статус-код 401"):
        assert (
            response.status_code == 401
        ), f"Ожидался 401, получен {response.status_code}"

    with allure.step("Проверить наличие сообщения о некорректном ключе"):
        assert (
            "некорректен" in response.text.lower()
        ), "В ответе отсутствует сообщение о некорректном ключе"


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


@allure.feature("API")
@allure.story("Фильтрация")
@pytest.mark.api
def test_movies_by_rating(api_client):
    """
    Позитивный тест: фильтрация фильмов по рейтингу IMDB.
    Проверяем, что у первых 5 фильмов рейтинг (если есть) находится в заданном диапазоне.
    """
    from data.test_data import RATING_MIN, RATING_MAX

    with allure.step(f"Отправить запрос с рейтингом от {RATING_MIN} до {RATING_MAX}"):
        response = api_client.get_movies_by_rating(RATING_MIN, RATING_MAX)

    with allure.step("Проверить статус-код 200"):
        assert (
            response.status_code == 200
        ), f"Ожидался 200, получен {response.status_code}"

    data = response.json()
    docs = data.get("docs", [])

    with allure.step("Проверить, что список фильмов не пуст"):
        assert len(docs) > 0, "Список фильмов пуст"

    with allure.step("Проверить рейтинг IMDB у первых 5 фильмов"):
        for film in docs[:5]:
            rating = film.get("rating", {}).get("imdb")
            if rating is not None:
                assert (
                    RATING_MIN <= rating <= RATING_MAX
                ), f"Рейтинг {rating} вне диапазона [{RATING_MIN}, {RATING_MAX}]"
            else:
                # Если рейтинг отсутствует, пропускаем проверку (API может не возвращать)
                allure.attach(
                    f"У фильма {film.get('name')} нет рейтинга IMDB", name="Пропущено"
                )
