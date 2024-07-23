import pytest
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
        ('2019-07-03T18:35:29.512364', '03.07.2019'),
        ('2018-06-30T02:08:58.425572', '30.06.2018'),
        ('2018-09-12T21:27:25.241689', '12.09.2018'),
        ('2018-10-14T08:21:33.419441', '14.10.2018')
    ]


@pytest.fixture
def correct_dates():
    return [
        ('2019-07-03T18:35:29.512364', '03.07.2019'),
        ('2018-06-30T02:08:58.425572', '30.06.2018'),
        ('2018-09-12T21:27:25.241689', '12.09.2018'),
        ('2018-10-14T08:21:33.419441', '14.10.2018')
    ]


@pytest.fixture
def incorrect_dates():
    return [
        (1234567890, ValueError),
        (['2019-07-03T18:35:29.512364'], ValueError),
        ('2019/07/03T18:35:29.512364', ValueError),
        ('2019-07-03', ValueError),
        ('invalid-date-string', ValueError)
    ]


@pytest.mark.parametrize("input_date, expected_output", [
    ('2019-07-03T18:35:29.512364', '03.07.2019'),
    ('2018-06-30T02:08:58.425572', '30.06.2018'),
    ('2018-09-12T21:27:25.241689', '12.09.2018'),
    ('2018-10-14T08:21:33.419441', '14.10.2018')
])
def test_get_date_correct(input_date, expected_output):
    assert get_date(input_date) == expected_output

