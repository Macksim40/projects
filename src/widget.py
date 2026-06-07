import re


def mask_account_card(input_string):
    """
    Маскирует номер карты или счёта в строке, оставляя видимыми только первые 6 и последние 4 цифры.

    Args:
        input_string (str): Строка, содержащая тип и номер карты/счёта, например:
            - 'Visa Platinum 7000792289606361'
            - 'Maestro 7000792289606361'
            - 'Счёт 73654108430135874305'

    Returns:
        str: Исходная строка с замаскированным номером.
    """
    # Регулярное выражение для поиска последовательности цифр в конце строки
    pattern = r'(\d+)$'
    match = re.search(pattern, input_string)

    if not match:
        # Если цифр не найдено, возвращаем исходную строку без изменений
        return input_string

    full_number = match.group(1)  # Получаем номер как строку
    number_length = len(full_number)

    # Определяем, какой шаблон маски использовать
    if 'Счёт' in input_string or number_length > 16:
        # Для счетов или номеров длиннее 16 цифр: показываем первые 4 и последние 4
        if number_length <= 8:
            # Если номер слишком короткий, маскируем всё, кроме крайних цифр
            masked_number = full_number[0] + '*' * (number_length - 2) + full_number[-1]
        else:
            masked_part = '*' * (number_length - 8)
            masked_number = full_number[:4] + masked_part + full_number[-4:]
    else:
        # Для карт (обычно 16 цифр): показываем первые 6 и последние 4
        masked_part = '*' * (number_length - 10)
        masked_number = full_number[:6] + masked_part + full_number[-4:]

    # Заменяем оригинальный номер на замаскированный в исходной строке
    result = input_string.replace(full_number, masked_number)
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
