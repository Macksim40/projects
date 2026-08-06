from datetime import datetime

import pytest


@pytest.fixture
def transactions():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "CANCELED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "EXECUTED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 4, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        # транзакция без даты
        {"id": 5, "state": "EXECUTED"},
        # невалидная дата
        {"id": 6, "state": "EXECUTED", "date": "not-a-date"},
    ]

@pytest.fixture
def card_numbers():
    # валидные 16-значные
    valid = [
        "4111111111111111",
        "5500000000000004",
    ]
    # невалидные
    invalid = [
        "123456789012345",   # 15 цифр
        "12345678901234567", # 17 цифр
        "1234abcd12345678",  # буквы
        "",                  # пустая
        "     ",             # пробелы
    ]
    return {"valid": valid, "invalid": invalid}

@pytest.fixture
def account_numbers():
    valid = [
        "RU98765432109876543210", # буквы в начале не проблема: функция сначала удаляет пробелы, потом проверяет isdigit
        "73654108430135874305",
    ]
    invalid = [
        "123",                 # < 4 цифр
        "",                    # пустая
        "abc",                 # не цифры
    ]
    return {"valid": valid, "invalid": invalid}
