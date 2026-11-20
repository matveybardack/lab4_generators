import pytest

from app.exceptions import InvalidInputError, InvalidListsError, NotEnoughValuesError
from app.generators.multiply_pairs import first_three, multiply_pairs


def test_products_correct(valid_lists):
    first, second = valid_lists
    assert list(multiply_pairs(first, second)) == [5, 12, 21, 32]


def test_negative_and_zero():
    assert list(multiply_pairs([-1, 0, 3], [4, 5, -6])) == [-4, 0, -18]


def test_result_is_lazy_iterator(valid_lists):
    result = multiply_pairs(*valid_lists)
    assert iter(result) is result


def test_first_three_via_next(valid_lists):
    assert first_three(multiply_pairs(*valid_lists)) == [5, 12, 21]


def test_exactly_three_values():
    assert first_three(multiply_pairs([1, 2, 3], [1, 2, 3])) == [1, 4, 9]


def test_first_three_consumes_only_three(valid_lists):
    products = multiply_pairs(*valid_lists)
    first_three(products)
    assert next(products) == 32


def test_less_than_three_values():
    with pytest.raises(NotEnoughValuesError):
        first_three(multiply_pairs([1, 2], [3, 4]))


def test_first_three_on_empty_iterator():
    with pytest.raises(NotEnoughValuesError):
        first_three(iter([]))


def test_different_length_raises():
    with pytest.raises(InvalidListsError):
        multiply_pairs([1, 2, 3], [1, 2])


@pytest.mark.parametrize("first, second", [([], []), ([1, 2], []), ([], [1, 2])])
def test_empty_lists(first, second):
    with pytest.raises(InvalidListsError):
        multiply_pairs(first, second)


def test_too_short_lists():
    with pytest.raises(InvalidListsError):
        multiply_pairs([1], [2])


def test_not_int_items():
    with pytest.raises(InvalidInputError):
        multiply_pairs([1, "a"], [2, 3])
