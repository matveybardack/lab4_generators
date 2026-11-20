import re
from typing import Sequence

from app.exceptions import (
    InvalidInputError,
    InvalidListsError,
    InvalidRangeError,
    NotEnoughValuesError,
)

MIN_LIST_LENGTH = 2
MIN_RESULT_COUNT = 3

_INT_RE = re.compile(r"[+-]?[0-9]+")
_SEPARATORS_RE = re.compile(r"[,\s]+")


def parse_int(text: str, name: str = "значение") -> int:
    """Преобразовать строку в целое число."""
    if not isinstance(text, str):
        raise InvalidInputError(f"{name}: ожидается строка.")
    cleaned = text.strip()
    if not cleaned:
        raise InvalidInputError(f"{name}: поле не должно быть пустым.")
    if _INT_RE.fullmatch(cleaned) is None:
        raise InvalidInputError(
            f"{name}: «{cleaned}» не является целым числом."
        )
    try:
        return int(cleaned)
    except ValueError as exc:  # например, слишком длинная запись числа
        raise InvalidInputError(
            f"{name}: не удалось преобразовать «{cleaned[:20]}...» в число."
        ) from exc


def validate_range(a: int, b: int) -> tuple[int, int]:
    """Проверить границы диапазона."""
    for label, value in (("a", a), ("b", b)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise InvalidInputError(f"Граница {label} должна быть целым числом.")
    if a >= b:
        raise InvalidRangeError(
            f"Левая граница a ({a}) должна быть меньше правой границы b ({b})."
        )
    return a, b


def parse_int_list(text: str, name: str = "список") -> list[int]:
    """Разобрать строку в список целых чисел."""
    if not isinstance(text, str):
        raise InvalidInputError(f"{name}: ожидается строка.")
    tokens = [t for t in _SEPARATORS_RE.split(text.strip()) if t]
    if not tokens:
        raise InvalidListsError(f"{name}: список не должен быть пустым.")
    return [
        parse_int(token, f"{name}, элемент №{index}")
        for index, token in enumerate(tokens, start=1)
    ]


def validate_lists(
    first: Sequence[int], second: Sequence[int]
) -> tuple[Sequence[int], Sequence[int]]:
    """Проверить пару списков для задания №3."""
    for label, items in (("Первый список", first), ("Второй список", second)):
        if len(items) == 0:
            raise InvalidListsError(f"{label} не должен быть пустым.")
        if len(items) < MIN_LIST_LENGTH:
            raise InvalidListsError(
                f"{label} должен содержать не менее {MIN_LIST_LENGTH} элементов."
            )
        if any(isinstance(x, bool) or not isinstance(x, int) for x in items):
            raise InvalidInputError(f"{label} должен состоять из целых чисел.")
    if len(first) != len(second):
        raise InvalidListsError(
            f"Списки должны быть одной длины: {len(first)} и {len(second)}."
        )
    return first, second


def check_enough_values(count: int, required: int = MIN_RESULT_COUNT) -> None:
    """Проверить, что получено достаточно значений."""
    if count < required:
        raise NotEnoughValuesError(
            f"Получено значений: {count}, требуется не менее {required}."
        )
