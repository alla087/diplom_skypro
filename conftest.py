import pytest
from selenium import webdriver
from api.api_client import APIClient
from config.settings import BASE_URL


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def api_client():
    return APIClient()
