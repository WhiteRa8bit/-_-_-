from .masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """Функция принемает и маскирует номера карт и счетов"""
    parts = account_card.split()
    if len(parts) < 2:
        raise ValueError("Некорректный формат номера карты или счета.")

    name = " ".join(parts[:-1])
    number = parts[-1].replace(" ", "")

    if not name or not number:
        raise ValueError("Номер карты или счета не введен.")

    if not all(c.isalnum() or c.isspace() for c in name) or not number.isdigit():
        raise ValueError("Номер карты или счета содержит некорректные символы.")

    if name.startswith("Счет"):
        if len(number) != 20:
            raise ValueError("Номер счета должен состоять из 20 цифр.")
        masked_number = get_mask_account(number)
    else:
        if len(number) not in (16, 18):
            raise ValueError("Номер карты должен состоять из 16 или 18 цифр.")
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"
