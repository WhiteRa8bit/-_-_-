from masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """Функция принемает и маскирует номера карт и счетов"""
    parts = account_card.split()
    name = " ".join(parts[:-1])
    number = parts[-1]

    if name.startswith("Счет"):
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"
