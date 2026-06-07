def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в формате XXXX XX** **** XXXX.
    """
    # Удаляем пробелы
    card_number = card_number.replace(' ', '')

    # Валидация
    if not card_number.isdigit() or len(card_number) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр")

    # Извлекаем части номера
    first_4 = card_number[:4]
    next_2 = card_number[4:6]
    last_4 = card_number[-4:]

    # Формируем маску через f‑строку
    return f"{first_4} {next_2}** **** {last_4}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта в формате **XXXX.
    """
    # Удаляем пробелы
    account_number = account_number.replace(' ', '')

    # Валидация
    if not account_number.isdigit():
        raise ValueError("Номер счёта должен состоять только из цифр")
    if len(account_number) < 4:
        raise ValueError("Номер счёта должен содержать минимум 4 цифры")

    # Берём последние 4 цифры
    last_4 = account_number[-4:]

    # Формируем маску
    return f"**{last_4}"
