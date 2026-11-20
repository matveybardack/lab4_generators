import random
import string
from typing import Iterator

from app.exceptions import InvalidInputError

CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!?@#$*"
PASSWORD_LENGTH = 12
DEFAULT_COUNT = 5


def passwords(length: int = PASSWORD_LENGTH, chars: str = CHARS) -> Iterator[str]:
    """Бесконечно отдавать случайные пароли заданной длины."""
    if isinstance(length, bool) or not isinstance(length, int) or length <= 0:
        raise InvalidInputError("Длина пароля должна быть положительным целым числом.")
    if not isinstance(chars, str) or not chars:
        raise InvalidInputError("Набор символов не должен быть пустым.")
    return _generate(length, chars)


def _generate(length: int, chars: str) -> Iterator[str]:
    while True:
        yield "".join(random.choice(chars) for _ in range(length))
