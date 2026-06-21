from datetime import datetime
from typing import List, Dict, Any

def filter_by_state(transactions: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу.

    Args:
        transactions: список словарей с транзакциями.
        state: значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED').

    Returns:
        Список транзакций с указанным статусом.
    """
    return [transaction for transaction in transactions if transaction.get('state') == state]



def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    Args:
        transactions: список словарей с транзакциями, содержащих ключ 'date'.
        reverse: порядок сортировки (True — по убыванию, False — по возрастанию).
    Returns:
        Отсортированный список транзакций.
    Raises:
        ValueError: если дата в транзакции имеет некорректный формат.
    """
    def parse_date(date_str: str) -> datetime:
        """Парсит строку даты в формате ISO в объект datetime."""
        if '.' in date_str:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        else:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

    try:
        return sorted(
            transactions,
            key=lambda x: parse_date(x['date']),
            reverse=reverse
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Ошибка при парсинге даты: {e}")
