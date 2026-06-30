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


@allure.feature("API")
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
        name="API Response",
        attachment_type=allure.attachment_type.JSON,
    )


def test_invalid_token(self):
#    📌 Что проверяем: отправка запроса с неверным API-ключом.
#    Шаги:
#      1. Импортирую INVALID_API_KEY из data.test_data.
from data.test_data import INVALID_API_KEY
#      2. Создаю клиента с неверным ключом:
    bad_client = APIClient(api_key=INVALID_API_KEY)
#      3. Отправляю запрос на поиск фильма "Матрица":
    response = bad_client.search_movie('Матрица')
#      4. Проверяю статус-код 401.
    assert response.status_code == 401, \
    f"Ожидался статус 401, получен {response.status_code}"
#      5. Проверею, что в теле ответа есть слово "некорректен".
    assert 'некорректен' in response.text.lower(), \
            "В ответе отсутствует сообщение о некорректном ключе"



def test_search_non_existent()
#    📌 Что проверяем: поиск по несуществующему запросу.
#    Шаги:
#      1. Импортирую NON_EXISTENT_QUERY из data.test_data.
from data.test_data import NON_EXISTENT_QUERY
#      2. Отправляю запрос:
    api_client.search_movie(NON_EXISTENT_QUERY)
#      3. Проверяю статус-код 200.
    assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}"
#      4. Проверяю, что поле docs – пустой список.
#      5. Проверяю, что поле total равно 0.

    assert response.status_code == 200
    data = response.json()
    assert data.get('docs') == []
    assert data.get('total') == 0


def test_movies_by_year_and_genre()
#    📌 Что проверяем: фильтрация по году и жанру.
#    Шаги:
#      1. Импортирую YEAR_FOR_FILTER и GENRE_FOR_FILTER из data.test_data.
from data.test_data import (
    YEAR_FOR_FILTER,
    GENRE_FOR_FILTER,
    )
#      2. Отправляю запрос: api_client.get_movies_by_year_and_genre(YEAR_FOR_FILTER, GENRE_FOR_FILTER)
    response = api_client.get_movies_by_year_and_genre(
            YEAR_FOR_FILTER,
            GENRE_FOR_FILTER
        )
#      3. Проверяю статус-код 200.
#      4. Проверяю, что список фильмов не пуст.
#      5. Проверяю у первых 5 фильмов:
#          - год равен YEAR_FOR_FILTER
#          - в списке жанров есть GENRE_FOR_FILTER

        assert response.status_code == 200
        data = response.json()
        docs = data.get('docs', [])
        assert len(docs) > 0
        for film in docs[:5]:
            assert film.get('year') == YEAR_FOR_FILTER
            genres = [g.get('name') for g in film.get('genres', [])]
            assert GENRE_FOR_FILTER in genres


def  test_movies_by_rating()
#    📌 Что проверяем: фильтрация по рейтингу IMDB.
#    Шаги:
#      1. Импортирую RATING_MIN и RATING_MAX из data.test_data.
from data.test_data import (
    RATING_MIN,
    RATING_MAX,
)
#      2. Отправляю запрос: api_client.get_movies_by_rating(RATING_MIN, RATING_MAX)
    response = api_client.get_movies_by_rating(RATING_MIN, RATING_MAX)
#      3. Проверяю статус-код 200.
#      4. Проверяю что список фильмов не пуст.
#      5. Проверяю у первых 5 фильмов, что rating.imdb (если есть) находится в диапазоне.

        assert response.status_code == 200
         data = response.json()
        docs = data.get('docs', [])
        assert len(docs) > 0
        for film in docs[:5]:
             rating = film.get('rating', {}).get('imdb')
            if rating is not None:
                assert RATING_MIN <= rating <= RATI
