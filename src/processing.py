from datetime import datetime
from typing import List, Dict, Any, Optional
import re

Transaction = Dict[str, Any]


def filter_by_state(transactions: List[Transaction], state: str = "EXECUTED") -> List[Transaction]:
    """
    Фильтрует список транзакций по значению ключа 'state'.

    Args:
        transactions: Список словарей, представляющих транзакции.
        state: Значение статуса для фильтрации (по умолчанию 'EXECUTED').

    Returns:
        Список отфильтрованных транзакций.
    """
    return [t for t in transactions if t.get("state") == state]


def sort_by_date(transactions: List[Transaction], reverse: bool = True) -> List[Transaction]:
    """
    Сортирует список транзакций по дате в ключе 'date' (формат ISO 8601).

    Транзакции без ключа 'date' или с невалидным форматом даты исключаются.

    Args:
        transactions: Список словарей транзакций с ключом 'date'.
        reverse: Порядок сортировки: True — по убыванию, False — по возрастанию.

    Returns:
        Отсортированный список транзакций.
    """

    def parse_iso_date(date_string: Optional[str]) -> Optional[datetime]:
        if not isinstance(date_string, str):
            return None
        normalized = date_string.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(normalized)
        except (ValueError, TypeError):
            return None

    # Сначала собираем пары (транзакция, datetime), где дата точно валидна
    parsed_pairs: List[tuple[Transaction, datetime]] = []
    for t in transactions:
        date_str = t.get("date")
        if isinstance(date_str, str):
            dt = parse_iso_date(date_str)
            if dt is not None:
                parsed_pairs.append((t, dt))

    # Сортируем по datetime (тип здесь гарантированно datetime, без Optional)
    sorted_pairs = sorted(parsed_pairs, key=lambda x: x[1], reverse=reverse)

    # Возвращаем только транзакции
    return [t for t, _ in sorted_pairs]


def get_date(date_string: str) -> Optional[str]:
    """
    Преобразует дату из формата ISO 8601 в формат ДД.ММ.ГГГГ.

    Args:
        date_string: Строка даты в формате ISO.

    Returns:
        Дата в формате 'ДД.ММ.ГГГГ' или None, если формат невалиден.
    """
    normalized = date_string.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(normalized)
        return dt.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return None


def mask_account_card(input_string: str) -> str:
    """
    Маскирует 16‑значный номер карты в строке.

    Args:
        input_string: Входная строка, потенциально содержащая номер карты.

    Returns:
        Строка с замаскированным номером карты или исходная строка.
    """
    pattern = r"\b(\d{4})\s?(\d{4})\s?(\d{4})\s?(\d{4})\b"
    match = re.search(pattern, input_string)
    if not match:
        return input_string

    g1, g2, g3, g4 = match.groups()
    masked_part = f"{g1} {g2}** **** {g4}"
    return input_string[:match.start()] + masked_part + input_string[match.end():]


if __name__ == "__main__":
    test_data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    print("=== filter_by_state ===")
    print(filter_by_state(test_data))
    print(filter_by_state(test_data, "CANCELED"))

    print("\n=== sort_by_date ===")
    print(sort_by_date(test_data, reverse=True))
    print(sort_by_date(test_data, reverse=False))

    print("\n=== get_date ===")
    print(get_date("2024-03-11T02:26:18.671407"))
    print(get_date("invalid-date"))

    print("\n=== mask_account_card ===")
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("No card number here"))

