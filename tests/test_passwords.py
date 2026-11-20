import pytest

from app.exceptions import InvalidInputError
from app.generators import take
from app.generators.passwords import CHARS, DEFAULT_COUNT, PASSWORD_LENGTH, passwords


def test_chars_set():
    expected = set(
        "abcdefghijklmnopqrstuvwxyz" "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "0123456789" "!?@#$*"
    )
    assert set(CHARS) == expected


def test_password_length():
    for pwd in take(passwords(), 50):
        assert len(pwd) == PASSWORD_LENGTH == 12


def test_password_chars():
    allowed = set(CHARS)
    for pwd in take(passwords(), 50):
        assert set(pwd) <= allowed


def test_five_passwords():
    assert len(take(passwords(), DEFAULT_COUNT)) == 5


def test_generator_is_infinite():
    gen = passwords()
    for _ in range(1000):
        next(gen)
    assert len(next(gen)) == 12


def test_reproducible_with_seed(seeded_random):
    import random

    first = take(passwords(), 5)
    random.seed(seeded_random)
    second = take(passwords(), 5)
    assert first == second

def test_custom_length_and_chars():
    result = take(passwords(length=4, chars="ab"), 20)
    assert all(len(p) == 4 and set(p) <= {"a", "b"} for p in result)


@pytest.mark.parametrize("length", [0, -1, 1.5, "12", True, None])
def test_invalid_length(length):
    with pytest.raises(InvalidInputError):
        passwords(length=length)


@pytest.mark.parametrize("chars", ["", None, 123])
def test_invalid_chars(chars):
    with pytest.raises(InvalidInputError):
        passwords(chars=chars)
