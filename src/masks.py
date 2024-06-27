def get_mask_card_number(card_number: str) -> str:
    """Функция принемает номер карты и маскирует 6 цифр в серидине"""
    mask_card_number = []
    visible_start = 6
    visible_end = 4

    for i, num in enumerate(card_number):
        if i < visible_start or i >= len(card_number) - visible_end:
            mask_card_number.append(num)
        else:
            mask_card_number.append("*")

        if (i + 1) % 4 == 0 and (i + 1) != len(card_number):
            mask_card_number.append(" ")

    return "".join(mask_card_number)


def get_mask_account(account_number: str) -> str:
    """Функция принемает номер счёта и возвращает последние 6 цифр, первые две замаскированы"""
    mask_account_number = []
    last_six_digits = account_number[-6:]
    for i, num in enumerate(last_six_digits):
        if i < 2:
            mask_account_number.append("*")
        else:
            mask_account_number.append(num)
    return "".join(mask_account_number)


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


def get_date(data_time: str) -> str:
    """Функция принемает дату, время и возвращает дату в формате ХХ.ХХ.ХХХХ"""
    date_parts = data_time[:10].split("-")
    return ".".join(date_parts[::-1])
