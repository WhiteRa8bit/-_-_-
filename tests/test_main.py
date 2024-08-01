import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
from src.masks import get_mask_account, get_mask_card_number, get_date
from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card


@pytest.fixture
def card_data():
    return "1234567890123456", "123412341234123412"


@pytest.fixture
def account_data():
    return "12345678901234567890", "00000000000000000001"


@pytest.fixture
def filter_data():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def sort_data():
    return [
        {"name": "John", "date": "2022-01-01"},
        {"name": "Jane", "date": "2021-12-31"},
        {"name": "Bob", "date": "2022-01-02"},
        {"name": "Alice", "date": "2021-12-30"},
    ]


@pytest.mark.parametrize(
    "card_number, expected",
    [("1234567890123456", "1234 56** **** 3456"), ("123412341234123412", "1234 12** **** **34 12")],
)
def test_mask_card_correct_masking(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account_number, expected", [("12345678901234567890", "**7890"), ("00000000000000000001", "**0001")]
)
def test_mask_account_correct_masking(account_number, expected):
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "input_data, exception",
    [
        (1234567890123456, TypeError),
        ("", ValueError),
        ("123456789A", ValueError),
        ("1234567890", ValueError),
        ("12345678901234567", ValueError),
    ],
)
def test_mask_card_exceptions(input_data, exception):
    with pytest.raises(exception):
        get_mask_card_number(input_data)


@pytest.mark.parametrize(
    "input_data, exception",
    [
        ("", ValueError),
        ("1234567890123456789", ValueError),
        ("123456789012345678901", ValueError),
        ("12345678901234567A90", ValueError),
    ],
)
def test_mask_account_exceptions(input_data, exception):
    with pytest.raises(exception):
        get_mask_account(input_data)


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
    ],
)
def test_mask_account_card(input_data, expected):
    assert mask_account_card(input_data) == expected


@pytest.mark.parametrize("input_data, exception", [("", ValueError), ("Invalid Input", ValueError)])
def test_mask_account_card_invalid_input(input_data, exception):
    with pytest.raises(exception):
        mask_account_card(input_data)


def test_filter_by_state(filter_data):
    assert filter_by_state(filter_data) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    assert filter_by_state(filter_data, "CANCELED") == [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    assert filter_by_state(filter_data, "PENDING") == []


def test_sort_by_date(sort_data):
    assert sort_by_date(sort_data) == [
        {"name": "Alice", "date": "2021-12-30"},
        {"name": "Jane", "date": "2021-12-31"},
        {"name": "John", "date": "2022-01-01"},
        {"name": "Bob", "date": "2022-01-02"},
    ]
    assert sort_by_date(sort_data, ascending=False) == [
        {"name": "Bob", "date": "2022-01-02"},
        {"name": "John", "date": "2022-01-01"},
        {"name": "Jane", "date": "2021-12-31"},
        {"name": "Alice", "date": "2021-12-30"},
    ]


@pytest.mark.parametrize(
    "data, exception",
    [
        ([{"name": "John", "date": "2022-01-01"}, 123, {"name": "Bob", "date": "2022-01-02"}], ValueError),
        ([{"name": "John"}, {"name": "Bob", "date": "2022-01-02"}], ValueError),
    ],
)
def test_sort_by_date_value_error(data, exception):
    with pytest.raises(exception):
        sort_by_date(data)


@pytest.fixture
def correct_dates():
    return [
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2018-06-30T02:08:58.425572", "30.06.2018"),
        ("2018-09-12T21:27:25.241689", "12.09.2018"),
        ("2018-10-14T08:21:33.419441", "14.10.2018"),
    ]


@pytest.fixture
def correct_dates():
    return [
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2018-06-30T02:08:58.425572", "30.06.2018"),
        ("2018-09-12T21:27:25.241689", "12.09.2018"),
        ("2018-10-14T08:21:33.419441", "14.10.2018"),
    ]


@pytest.fixture
def incorrect_dates():
    return [
        (1234567890, ValueError),
        (["2019-07-03T18:35:29.512364"], ValueError),
        ("2019/07/03T18:35:29.512364", ValueError),
        ("2019-07-03", ValueError),
        ("invalid-date-string", ValueError),
    ]


@pytest.mark.parametrize(
    "input_date, expected_output",
    [
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2018-06-30T02:08:58.425572", "30.06.2018"),
        ("2018-09-12T21:27:25.241689", "12.09.2018"),
        ("2018-10-14T08:21:33.419441", "14.10.2018"),
    ],
)
def test_get_date_correct(input_date, expected_output):
    assert get_date(input_date) == expected_output


@pytest.fixture
def transactions():
    return [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}},
        {"id": 3, "operationAmount": {"currency": {"code": "USD"}}},
    ]


@pytest.mark.parametrize("currency_code, expected_ids", [("USD", [1, 3]), ("EUR", [2]), ("RUB", [])])
def test_filter_by_currency(transactions, currency_code, expected_ids):
    filtered_transactions = list(filter_by_currency(transactions, currency_code))
    assert [transaction["id"] for transaction in filtered_transactions] == expected_ids


def test_filter_by_currency_invalid_input(transactions):
    with pytest.raises(TypeError):
        list(filter_by_currency("invalid", "USD"))
    with pytest.raises(TypeError):
        list(filter_by_currency(transactions, 123))
    with pytest.raises(ValueError):
        list(filter_by_currency([{"id": 1, "operationAmount": {}}], "USD"))
    with pytest.raises(ValueError):
        list(filter_by_currency([{"id": 1, "operationAmount": {"currency": {}}}], "USD"))
    with pytest.raises(ValueError):
        list(filter_by_currency([{"id": 1, "operationAmount": {"currency": {"code": 123}}}], "USD"))


@pytest.fixture
def transactions():
    return [
        {"id": 1, "description": "Перевод со счета на счет", "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "description": "Перевод с карты на карту", "operationAmount": {"currency": {"code": "EUR"}}},
        {"id": 3, "description": "Перевод организации", "operationAmount": {"currency": {"code": "USD"}}},
    ]


def test_transaction_descriptions(transactions):
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == [transaction.get("description", "") for transaction in transactions]


@pytest.mark.parametrize("invalid_input", ["invalid", [{"id": 1}], [{"id": 1, "description": 123}]])
def test_transaction_descriptions_invalid_input(invalid_input):
    with pytest.raises(Exception):
        list(transaction_descriptions(invalid_input))


@pytest.mark.parametrize(
    "start, end, expected_numbers",
    [
        (1, 3, ["0000000000000001", "0000000000000002", "0000000000000003"]),
        (10, 12, ["0000000000000010", "0000000000000011", "0000000000000012"]),
        (9999999999999998, 9999999999999999, ["9999999999999998", "9999999999999999"]),
    ],
)
def test_card_number_generator(start, end, expected_numbers):
    card_numbers = list(card_number_generator(start, end))
    assert card_numbers == expected_numbers


def test_card_number_generator_invalid_input():
    with pytest.raises(TypeError):
        list(card_number_generator("invalid", 3))
    with pytest.raises(TypeError):
        list(card_number_generator(1, "invalid"))
    with pytest.raises(ValueError):
        list(card_number_generator(0, 3))
    with pytest.raises(ValueError):
        list(card_number_generator(1, 10000000000000000))
    with pytest.raises(ValueError):
        list(card_number_generator(3, 1))
