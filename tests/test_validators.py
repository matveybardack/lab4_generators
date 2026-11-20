import pytest

from app.exceptions import (
    InvalidInputError,
    InvalidListsError,
    InvalidRangeError,
    NotEnoughValuesError,
)
from app.validators import (
    check_enough_values,
    parse_int,
    parse_int_list,
    validate_lists,
    validate_range,
)


@pytest.mark.parametrize(
    "text, expected",
    [("5", 5), ("  -7 ", -7), ("+3", 3), ("0", 0), ("007", 7)],
)
def test_parse_int_ok(text, expected):
    assert parse_int(text) == expected


@pytest.mark.parametrize("text", ["", "   ", "abc", "1.5", "1e3", "1_000", "5 6", "--5"])
def test_parse_int_invalid(text):
    with pytest.raises(InvalidInputError):
        parse_int(text)


def test_parse_int_not_string():
    with pytest.raises(InvalidInputError):
        parse_int(5)


def test_parse_int_message_contains_name():
    with pytest.raises(InvalidInputError, match="поле a"):
        parse_int("", "поле a")


def test_validate_range_ok():
    assert validate_range(-3, 2) == (-3, 2)


@pytest.mark.parametrize("a, b", [(2, 2), (5, 1), (0, -1)])
def test_validate_range_wrong_order(a, b):
    with pytest.raises(InvalidRangeError):
        validate_range(a, b)


@pytest.mark.parametrize("a, b", [(1.5, 3), (1, "3"), (True, 5), (None, 1)])
def test_validate_range_not_int(a, b):
    with pytest.raises(InvalidInputError):
        validate_range(a, b)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("1 2 3", [1, 2, 3]),
        ("1,2,3", [1, 2, 3]),
        (" 1, 2  3 ,4 ", [1, 2, 3, 4]),
        ("-1, 0, +2", [-1, 0, 2]),
    ],
)
def test_parse_int_list_ok(text, expected):
    assert parse_int_list(text) == expected


@pytest.mark.parametrize("text", ["", "   ", ",", " , , "])
def test_parse_int_list_empty(text):
    with pytest.raises(InvalidListsError):
        parse_int_list(text)


@pytest.mark.parametrize("text", ["1 a 3", "1, 2.5", "x"])
def test_parse_int_list_invalid_item(text):
    with pytest.raises(InvalidInputError):
        parse_int_list(text)


def test_parse_int_list_not_string():
    with pytest.raises(InvalidInputError):
        parse_int_list(None)


def test_validate_lists_ok(valid_lists):
    first, second = valid_lists
    assert validate_lists(first, second) == (first, second)


@pytest.mark.parametrize("first, second", [([], []), ([1, 2], []), ([], [1, 2])])
def test_validate_lists_empty(first, second):
    with pytest.raises(InvalidListsError):
        validate_lists(first, second)


@pytest.mark.parametrize("first, second", [([1], [2]), ([1], [2, 3])])
def test_validate_lists_too_short(first, second):
    with pytest.raises(InvalidListsError):
        validate_lists(first, second)


def test_validate_lists_different_length():
    with pytest.raises(InvalidListsError):
        validate_lists([1, 2, 3], [1, 2])


def test_validate_lists_not_int():
    with pytest.raises(InvalidInputError):
        validate_lists([1, 2.5], [1, 2])


def test_check_enough_values_ok():
    check_enough_values(3)
    check_enough_values(10)


@pytest.mark.parametrize("count", [0, 1, 2])
def test_check_enough_values_not_enough(count):
    with pytest.raises(NotEnoughValuesError):
        check_enough_values(count)
