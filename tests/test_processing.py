import pytest

from src.processing import filter_by_state, get_date, sort_by_date


def test_filter_by_state_default(transactions):
    filtered = filter_by_state(transactions)  # по умолчанию EXECUTED
    assert all(t["state"] == "EXECUTED" for t in filtered)
    assert len(filtered) == 3  # id 1,3,5

def test_filter_by_state_custom(transactions):
    filtered = filter_by_state(transactions, "CANCELED")
    assert all(t["state"] == "CANCELED" for t in filtered)
    assert len(filtered) == 2  # id 2,4

def test_filter_by_state_empty(transactions):
    filtered = filter_by_state(transactions, "UNKNOWN")
    assert filtered == []

@pytest.mark.parametrize("state", ["EXECUTED", "CANCELED"])
def test_filter_by_state_parametrized(transactions, state):
    filtered = filter_by_state(transactions, state)
    assert all(t["state"] == state for t in filtered)

def test_sort_by_date_descending(transactions):
    sorted_list = sort_by_date(transactions, reverse=True)
    dates = [t["date"] for t in sorted_list if "date" in t]
    # сортируем ISO-строки: лексикографически совпадает с хронологией
    assert dates == sorted(dates, reverse=True)

def test_sort_by_date_ascending(transactions):
    sorted_list = sort_by_date(transactions, reverse=False)
    dates = [t["date"] for t in sorted_list if "date" in t]
    assert dates == sorted(dates)

def test_sort_by_date_drops_invalid_and_missing(transactions):
    # sort_by_date должен исключить транзакции без даты и с невалидной датой
    sorted_list = sort_by_date(transactions)
    ids = [t["id"] for t in sorted_list]
    # id 5 (нет даты) и id 6 (невалидная дата) должны отсутствовать
    assert 5 not in ids
    assert 6 not in ids

@pytest.mark.parametrize(
    "iso_str,expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2023-12-25T15:30:45", "25.12.2023"),
    ],
)
def test_get_date_valid(iso_str, expected):
    assert get_date(iso_str) == expected

@pytest.mark.parametrize(
    "bad_input",
    ["", None, "not-a-date", "2024/01/10"],
)
def test_get_date_invalid(bad_input):
    result = get_date(bad_input)
    assert result is None
