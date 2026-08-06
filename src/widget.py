import re

from masks import get_mask_account, get_mask_card_number


def mask_account_card(input_string: str) -> str:
    """
    Маскирует номер карты или счёта в строке, используя соответствующий тип маскировки.

    Args:
        input_string (str): Строка, содержащая тип и номер карты/счёта, например:
            - 'Visa Platinum 7000792289606361'
            - 'Maestro 7000792289606361'
            - 'Счёт 73654108430135874305'


    Returns:
        str: Исходная строка с замаскированным номером.
    """
    # Ищем последовательность цифр в конце строки
    match = re.search(r'(\d+)$', input_string)
    if not match:
        return input_string  # Если цифр нет, возвращаем исходную строку

    full_number = match.group(1)

    # Определяем тип: счёт или карта
    is_account = 'Счёт' in input_string or 'счет' in input_string.lower()

    try:
        if is_account:
            # Для счетов используем функцию маскировки счёта из модуля masks
            masked_number = get_mask_account(full_number)
        else:
            # Для карт используем функцию маскировки карты из модуля masks
            try:
                masked_number = get_mask_card_number(full_number)
            except ValueError:
                # Если номер карты не 16 цифр, обрабатываем как счёт
                masked_number = get_mask_account(full_number)
    except ValueError as e:
        # Если валидация не прошла ни для карты, ни для счёта, возвращаем исходную строку с предупреждением
        print(f"Предупреждение: {e}. Возвращаем исходную строку.")
        return input_string

    # Заменяем исходный номер на замаскированный в исходной строке
    result = input_string[:-len(full_number)] + masked_number
    return result


from datetime import datetime


def get_date(date_string):
    """
    Преобразует строку с датой из формата ISO (2024-03-11T02:26:18.671407)
    в формат ДД.ММ.ГГГГ (11.03.2024).

    Args:
        date_string (str): Строка с датой в формате ISO (с микросекундами или без)

    Returns:
        str: Строка с датой в формате "ДД.ММ.ГГГГ", или None при ошибке

    Examples:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
        >>> get_date("2023-12-25T15:30:45")
        '25.12.2023'
    """
    try:
        # Парсим строку в объект datetime — %f опционально (может быть или не быть)
        if '.' in date_string:
            # Если есть микросекунды
            dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")
        else:
            # Если микросекунд нет
            dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")

        # Форматируем в нужный вид: день.месяц.год с ведущими нулями
        return dt.strftime("%d.%m.%Y")

    except (ValueError, TypeError) as e:
        # Обрабатываем ошибки парсинга и типы данных
        print(f"Ошибка обработки даты: {e}")
        return None
