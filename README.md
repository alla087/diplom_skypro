# Проект автоматизации тестирования Кинопоиска

## Описание
- Автоматизированные тесты для сайта [Кинопоиск](https://www.kinopoisk.ru/).  
- Проект покрывает UI-сценарии (Selenium) и API-эндпоинты (requests).  
- Основан на сценариях из финальной работы по ручному тестированию.

## Структура проекта 
```
final_project/
├── config/
│   └── settings.py          # URL, API-токен, таймауты
├── data/
│   └── test_data.py         # тестовые данные
├── pages/                   # Page Object'ы
│   ├── base_page.py
│   ├── main_page.py
│   ├── search_results_page.py
│   ├── film_page.py
│   └── profile_page.py
├── api/
│   └── api_client.py        # клиент для API
├── tests/
│   ├── conftest.py          # фикстуры
│   ├── test_ui.py           # UI-тесты
│   └── test_api.py          # API-тесты
├── cookies.txt              # куки
├── requirements.txt
├── pytest.ini
└── README.md               
```

## Предварительная настройка

### 1. API-токен
- Зарегистрируйтесь на [api.kinopoisk.dev](https://api.kinopoisk.dev/) и получите ключ.
- Вставьте его в файл `config/settings.py`:
```
API_KEY = 'ваш_токен'
```
> Важно: не выкладывайте этот файл с заполненным токеном, очистите перед коммитом.

### 2. Установка зависимостей
```
pip install -r requirements.txt
```

## Запуск тестов
```
| Режим | Команда |
|-------|---------|
| Только API | `pytest tests/test_api.py -m api --alluredir=./allure-api` |
| Только UI  | `pytest tests/test_ui.py -m ui --alluredir=./allure-ui` |
| Все тесты  | `pytest --alluredir=./allure-all` |
```
> UI-тесты с маркером `auth` используют куки из `cookies.txt`. Убедитесь, что файл заполнен.

## Allure-отчёт
```
allure serve ./allure-api   # или allure-ui, allure-all
```

## Стек технологий
- Python 3.10+
- pytest
- selenium + webdriver-manager
- requests
- allure-pytest

## Финальная работа по ручному тестированию
[Ссылка](https://alla11.yonote.ru/share/9cbea249-5296-4aff-9adb-541c16d8ece3)