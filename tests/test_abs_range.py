import types

import pytest

from app.exceptions import InvalidInputError, InvalidRangeError
from app.generators import take
from app.generators.abs_range import DEFAULT_COUNT, abs_range


def test_negative_and_positive():
    assert list(abs_range(-3, 2)) == [3, 2, 1, 0, 1, 2]


def test_right_border_included():
    assert list(abs_range(1, 3)) == [1, 2, 3]


def test_all_negative():
    assert list(abs_range(-5, -2)) == [5, 4, 3, 2]


def test_range_with_zero():
    assert take(abs_range(-1, 1), DEFAULT_COUNT) == [1, 0, 1]


def test_less_than_four_values():
    assert take(abs_range(5, 6), DEFAULT_COUNT) == [5, 6]


def test_more_than_four_values():
    result = take(abs_range(-10, 10), DEFAULT_COUNT)
    assert result == [10, 9, 8, 7]
    assert len(result) == DEFAULT_COUNT


def test_take_custom_count():
    assert take(abs_range(1, 100), 2) == [1, 2]


def test_result_is_lazy_generator():
    assert isinstance(abs_range(1, 10), types.GeneratorType)


def test_huge_range_is_not_materialized():
    assert take(abs_range(0, 10**12), 4) == [0, 1, 2, 3]


@pytest.mark.parametrize("a, b", [(3, 3), (5, 1)])
def test_wrong_range(a, b):
    with pytest.raises(InvalidRangeError):
        abs_range(a, b)


def test_not_int_borders():
    with pytest.raises(InvalidInputError):
        abs_range(1.5, 4)
