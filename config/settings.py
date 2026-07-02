import os

# Настройки окружения
BASE_URL = "https://www.kinopoisk.ru/"
API_BASE_URL = "https://api.kinopoisk.dev/"
API_KEY = "E87R7GE-H6A4YFW-PHZWKBP-W4PT0VY"

# Таймауты
UI_TIMEOUT = 10
API_TIMEOUT = 30

# Путь к файлу с куками (относительно корня проекта)
COOKIES_FILE = os.path.join(os.path.dirname(__file__), "..", "cookies.txt")
