import requests
import allure
from config.settings import API_BASE_URL, API_KEY


class APIClient:
    def __init__(self, api_key=API_KEY):
        self.base_url = API_BASE_URL
        self.headers = {"X-API-KEY": api_key} if api_key else {}

    def _request(self, method, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        with allure.step(f"API {method} {endpoint} с params={params}"):
            response = requests.request(
                method, url, headers=self.headers, params=params
            )
            allure.attach(
                str(response.status_code),
                name="Status code",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                response.text,
                name="Response body",
                attachment_type=allure.attachment_type.TEXT,
            )
            return response

    def search_movie(self, query):
        return self._request("GET", "v1.4/movie/search", {"query": query})

    def get_movies_by_year_and_genre(self, year, genre):
        return self._request("GET", "v1.4/movie", {"year": year, "genres.name": genre})

    def get_movies_by_rating(self, min_rating, max_rating):
        return self._request(
            "GET", "v1.4/movie", {"rating.imdb": f"{min_rating}-{max_rating}"}
        )

    def get_movies_by_year(self, year):
        return self._request("GET", "v1.4/movie", {"year": year})
