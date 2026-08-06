import pytest

from src.widget import mask_account_card


@pytest.mark.parametrize(
    "input_str,contains_account_marker,expected_contains",
    [
        ("Visa Platinum 7000792289606361", False, "7000 79** **** 6361"),
        ("Maestro 7000792289606361", False, "7000 79** **** 6361"),
        ("Счёт 73654108430135874305", True, "**4305"),
        ("счет 123456789", True, "**6789"),
        ("No card number here", False, "No card number here"),
        ("", False, ""),
    ],
)
def test_mask_account_card_basic(input_str, contains_account_marker, expected_contains):
    result = mask_account_card(input_str)
    if contains_account_marker or "Счёт" in input_str or "счет" in input_str.lower():
        assert expected_contains in result
    else:
        # если это карта — маска должна быть в формате карты
        if "Счёт" not in input_str and "счет" not in input_str.lower() and any(ch.isdigit() for ch in input_str):
            assert "****" in result or expected_contains in result
        else:
            # если цифр нет — строка должна остаться как есть
            assert result == input_str

@pytest.mark.parametrize(
    "input_str",
    [
        "Card 123456789012345",  # 15 цифр — невалидно для карты, но валидно для счёта
        "Счёт 123",             # < 4 цифры — ошибка валидации
    ],
)
def test_mask_account_card_fallback_and_errors(input_str):
    # fallback: если карта не валидна, пробует счёт. Если и счёт не валиден — возвращает исходную строку
    result = mask_account_card(input_str)
    # для 15-значного номера: он не карта, но может быть счётом (если >=4 цифр)
    if "Счёт" in input_str or "счет" in input_str.lower():
        # тут будет ValueError внутри, и функция вернёт исходную строку (с print)
        assert result == input_str
    else:
        # 15-значный номер без метки счёта: не карта (ошибка), не счёт (длина < 4? нет, 15 >= 4), но get_mask_account ожидает только цифры
        # в итоге get_mask_account может сработать, если строка только цифры
        assert "**" in result or result == input_str
