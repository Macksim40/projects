from datetime import datetime


def filter_by_state(transactions: list, state: str = 'EXECUTED') -> list:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        transactions (list): Список словарей, каждый из которых должен содержать ключ 'state'.
        state (str): Значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED').


    Returns:
        list: Новый список словарей, где значение ключа 'state' совпадает с указанным.
    """
    return [transaction for transaction in transactions if transaction.get('state') == state]


def sort_by_date(transactions: list, reverse: bool = True) -> list:
    """
    Сортирует список словарей по дате в ключе 'date'.

    Args:
        transactions (list): Список словарей, каждый из которых должен содержать ключ 'date'
            со значением в формате ISO (например, '2019-07-03T18:35:29.512364').
        reverse (bool): Порядок сортировки: True — по убыванию (сначала новые),
            False — по возрастанию (сначала старые) (по умолчанию True).

    Returns:
        list: Новый отсортированный список словарей.
    """

    def parse_date(date_string: str) -> datetime:
        """Парсит строку даты в формате ISO в объект datetime."""
        return datetime.fromisoformat(date_string)

    # Сортируем список, используя ключ — преобразованную дату; сохраняем порядок по параметру reverse
    sorted_transactions = sorted(
        transactions,
        key=lambda x: parse_date(x['date']),
        reverse=reverse
    )
    return sorted_transactions


# Примеры использования и проверки функций
if __name__ == "__main__":
    # Тестовые данные
    test_data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    print("=== filter_by_state ===")
    print("По умолчанию (state='EXECUTED'):")
    result_executed = filter_by_state(test_data)
    for item in result_executed:
        print(item)

    print("\nС параметром state='CANCELED':")
    result_canceled = filter_by_state(test_data, 'CANCELED')
    for item in result_canceled:
        print(item)

    print("\n=== sort_by_date ===")
    print("Сортировка по убыванию (reverse=True):")
    sorted_desc = sort_by_date(test_data, reverse=True)
    for item in sorted_desc:
        print(item)

    print("\nСортировка по возрастанию (reverse=False):")
    sorted_asc = sort_by_date(test_data, reverse=False)
    for item in sorted_asc:
        print(item)
