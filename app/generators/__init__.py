from itertools import islice
from typing import Iterable, TypeVar

T = TypeVar("T")

def take(iterable: Iterable[T], n: int) -> list[T]:
    """Взять первые n значений (или меньше, если данных меньше)."""
    return list(islice(iterable, n))
