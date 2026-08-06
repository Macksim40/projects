import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_valid(card_numbers):
    for n in card_numbers["valid"]:
        masked = get_mask_card_number(n)
        assert len(masked) == 19
        assert masked.startswith("****") is False  # первые 4 цифры видны
        assert "**" in masked
        assert masked.endswith("****") is False     # последние 4 цифры видны

@pytest.mark.parametrize("bad", [
    "123456789012345",
    "12345678901234567",
    "1234abcd12345678",
    "",
    "     ",
])
def test_get_mask_card_number_invalid(bad):
    with pytest.raises(ValueError):
        get_mask_card_number(bad)

def test_get_mask_account_valid(account_numbers):
    for n in account_numbers["valid"]:
        # сначала удалим нецифровые символы, чтобы передать в функцию только цифры
        digits_only = "".join(ch for ch in n if ch.isdigit())
        if len(digits_only) < 4:
            continue
        masked = get_mask_account(digits_only)
        assert masked.startswith("**")
        assert len(masked) >= 6  # ** + 4 цифры

@pytest.mark.parametrize("bad", [
    "123",
    "",
    "abc",
])
def test_get_mask_account_invalid(bad):
    with pytest.raises(ValueError):
        get_mask_account(bad)
