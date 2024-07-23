def get_mask_card_number(card_number: str) -> str:
    """Функция принимает номер карты и маскирует 6 цифр в середине"""
    if not isinstance(card_number, str):
        raise TypeError("Номер карты должен быть строкой.")

    if not card_number:
        raise ValueError("Номер карты не может быть пустой строкой.")

    if not card_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры.")

    if len(card_number) not in (16, 18):
        raise ValueError("Номер карты должен состоять из 16 или 18 цифр.")

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
    if not account_number:
        raise ValueError("Номер счета не может быть пустой строкой.")

    if not account_number.isdigit():
        raise ValueError("Номер счета должен содержать только цифры.")

    if len(account_number) != 20:
        raise ValueError("Номер счета должен состоять из 20 цифр.")

    mask_account_number = []
    last_six_digits = account_number[-6:]
    for i, num in enumerate(last_six_digits):
        if i < 2:
            mask_account_number.append("*")
        else:
            mask_account_number.append(num)

    return "".join(mask_account_number)


def get_date(data_time: str) -> str:
    """Функция принимает дату и время и возвращает дату в формате ХХ.ХХ.ХХХХ"""
    try:
        if not isinstance(data_time, str):
            raise ValueError("Значение должно быть строкой")

        # Проверяем, что строка имеет достаточную длину для даты
        if len(data_time) < 10:
            raise ValueError("Некорректный формат даты")

        # Извлекаем только часть с датой
        date_part = data_time[:10]

        # Проверяем, что дата содержит именно символ '-'
        if '-' not in date_part:
            raise ValueError("Дата должна содержать символ '-' как разделитель")

        date_parts = date_part.split("-")

        if len(date_parts) != 3:
            raise ValueError("Некорректный формат даты")

        year, month, day = date_parts

        # Проверяем, что части даты являются числами
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            raise ValueError("Части даты должны быть числами")

        # Проверяем, что месяц и день имеют правильную длину
        if len(month) != 2 or len(day) != 2:
            raise ValueError("Месяц и день должны быть двузначными")

        return ".".join(date_parts[::-1])
    except Exception as e:
        raise ValueError(f"Некорректный ввод: {e}")
