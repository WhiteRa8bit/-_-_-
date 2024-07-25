def filter_by_currency(transactions, currency_code):
    """Принимает на вход список словарей, представляющих транзакции,
    возвращает транзакции, где валюта операции соответствует заданной"""
    if not isinstance(transactions, list):
        raise TypeError("Колекция транзакций должна быть списком")
    if not isinstance(currency_code, str):
        raise TypeError("Код валюты должен быть строкой")

    for transaction in transactions:
        if not isinstance(transaction, dict):
            raise TypeError("Транзакция должна быть словарем")
        if "operationAmount" not in transaction or not isinstance(transaction["operationAmount"], dict):
            raise ValueError("Транзакция должна иметь поле 'operationAmount' со значением словаря")
        if "currency" not in transaction["operationAmount"] or not isinstance(
            transaction["operationAmount"]["currency"], dict
        ):
            raise ValueError("Должно быть поле 'currency' со значением словаря в поле 'operationAmount'")
        if "code" not in transaction["operationAmount"]["currency"] or not isinstance(
            transaction["operationAmount"]["currency"]["code"], str
        ):
            raise ValueError("Должно быть поле 'code' со значением строки в поле 'currency' поля 'operationAmount'")

        if transaction["operationAmount"]["currency"]["code"] == currency_code:
            yield transaction


def transaction_descriptions(transactions):
    """Принимает список словарей с транзакциями и возвращает описание каждой операции по очереди"""
    if not isinstance(transactions, list):
        raise TypeError("Колекция транзакций должна быть списком")

    for transaction in transactions:
        if not isinstance(transaction, dict):
            raise TypeError("Транзакция должна быть словарем")
        if "description" not in transaction or not isinstance(transaction["description"], str):
            raise ValueError("Транзакция должна иметь поле 'description' со значением строки")

        yield transaction["description"]


def card_number_generator(start, end):
    """Генерирует номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999"""
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("Начальное и конечное значения должны быть целыми числами")
    if start < 1 or end > 9999999999999999 or start > end:
        raise ValueError("Некорректный диапазон значений")

    for number in range(start, end + 1):
        yield f"{number:016}"
