from app.generators import take
from app.validators import validate_range
from typing import Iterator

DEFAULT_COUNT = 4


def abs_range(a: int, b: int) -> Iterator[int]:
    """Лениво отдать модули всех целых чисел от a до b включительно."""
    validate_range(a, b)
    return (abs(x) for x in range(a, b + 1))
