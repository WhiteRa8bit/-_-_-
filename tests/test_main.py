import pytest

from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card


def test_mask_card_correct_masking():
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert get_mask_card_number("123412341234123412") == "1234 12** **** **34 12"


def test_mask_card_type_error():
    with pytest.raises(TypeError):
        get_mask_card_number(1234567890123456)


def test_mask_card_value_error():
    with pytest.raises(ValueError):
        get_mask_card_number("")
    with pytest.raises(ValueError):
        get_mask_card_number("123456789A")
    with pytest.raises(ValueError):
        get_mask_card_number("1234567890")
    with pytest.raises(ValueError):
        get_mask_card_number("12345678901234567")


def test_mask_account_correct_masking():
    assert get_mask_account("12345678901234567890") == "**7890"
    assert get_mask_account("00000000000000000001") == "**0001"


def test_mask_account_value_error():
    with pytest.raises(ValueError):
        get_mask_account("")
    with pytest.raises(ValueError):
        get_mask_account("1234567890123456789")
    with pytest.raises(ValueError):
        get_mask_account("123456789012345678901")
    with pytest.raises(ValueError):
        get_mask_account("12345678901234567A90")


def test_mask_account_card():
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"
    assert mask_account_card("MasterCard 7158300734726758") == "MasterCard 7158 30** **** 6758"
    assert mask_account_card("Maestro 1234567890123456") == "Maestro 1234 56** **** 3456"


def test_mask_account_card_invalid_input():
    with pytest.raises(ValueError):
        mask_account_card("")
    with pytest.raises(ValueError):
        mask_account_card("Invalid Input")


def test_filter_by_state():
    data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]
    assert filter_by_state(data) == [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]
    assert filter_by_state(data, 'CANCELED') == [
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]
    assert filter_by_state(data, 'PENDING') == []


def test_sort_by_date():
    data = [
        {"name": "John", "date": "2022-01-01"},
        {"name": "Jane", "date": "2021-12-31"},
        {"name": "Bob", "date": "2022-01-02"},
        {"name": "Alice", "date": "2021-12-30"}
    ]

    assert sort_by_date(data) == [
        {"name": "Alice", "date": "2021-12-30"},
        {"name": "Jane", "date": "2021-12-31"},
        {"name": "John", "date": "2022-01-01"},
        {"name": "Bob", "date": "2022-01-02"}
    ]
    assert sort_by_date(data, ascending=False) == [
        {"name": "Bob", "date": "2022-01-02"},
        {"name": "John", "date": "2022-01-01"},
        {"name": "Jane", "date": "2021-12-31"},
        {"name": "Alice", "date": "2021-12-30"}
    ]

def test_value_error():
    data = [
        {"name": "John", "date": "2022-01-01"},
        123,
        {"name": "Bob", "date": "2022-01-02"}
    ]
    with pytest.raises(ValueError):
        sort_by_date(data)

    data = [
        {"name": "John"},
        {"name": "Bob", "date": "2022-01-02"}
    ]
    with pytest.raises(ValueError):
        sort_by_date(data)
