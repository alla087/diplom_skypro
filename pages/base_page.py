import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        with allure.step(f"Открыть {url}"):
            self.driver.get(url)

    def find_element(self, locator, timeout=10):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        with allure.step(f"Кликнуть на {locator}"):
            self.find_element(locator).click()

    def input_text(self, locator, text):
        with allure.step(f'Ввести "{text}" в поле {locator}'):
            el = self.find_element(locator)
            el.clear()
            el.send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text
