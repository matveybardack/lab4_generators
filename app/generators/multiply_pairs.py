from operator import mul
from typing import Iterator, Sequence

from app.exceptions import NotEnoughValuesError
from app.validators import MIN_RESULT_COUNT, check_enough_values, validate_lists


def multiply_pairs(first: Sequence[int], second: Sequence[int]) -> Iterator[int]:
    """Лениво отдать попарные произведения элементов двух списков."""
    validate_lists(first, second)
    return map(mul, first, second)
    # return map(lambda pair: mul(*pair), zip(first, second))

def first_three(products: Iterator[int]) -> list[int]:
    """Получить первые три значения тремя последовательными вызовами next."""
    result: list[int] = []
    try:
        result.append(next(products))
        result.append(next(products))
        result.append(next(products))
    except StopIteration:
        check_enough_values(len(result), MIN_RESULT_COUNT)
        raise NotEnoughValuesError("Генератор завершился раньше времени.")
    return result
