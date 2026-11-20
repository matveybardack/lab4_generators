import itertools
import threading

import pytest

from app.exceptions import GeneratorStoppedError, InvalidRangeError
from app.generators import take
from app.generators.abs_range import abs_range
from app.threading_utils.threaded_generator import ThreadedGenerator


def failing_source():
    yield 1
    raise ValueError("сбой в потоке")


def test_finite_generator_ends_with_stop_iteration():
    gen = ThreadedGenerator(lambda: iter([1, 2, 3]))
    assert list(gen) == [1, 2, 3]
    with pytest.raises(StopIteration):
        next(gen)
    gen.stop()


def test_order_preserved_with_small_queue():
    with ThreadedGenerator(lambda: iter(range(200)), maxsize=2) as gen:
        assert list(gen) == list(range(200))


def test_accepts_ready_iterator():
    with ThreadedGenerator(iter("abc")) as gen:
        assert list(gen) == ["a", "b", "c"]


def test_infinite_generator_stops():
    gen = ThreadedGenerator(lambda: itertools.count(), maxsize=2)
    assert take(gen, 5) == [0, 1, 2, 3, 4]
    gen.stop()
    gen.thread.join(timeout=2)
    assert not gen.thread.is_alive()


def test_next_after_stop_raises():
    gen = ThreadedGenerator(lambda: itertools.count(), maxsize=2)
    next(gen)
    gen.stop()
    with pytest.raises(GeneratorStoppedError):
        next(gen)


def test_stop_is_idempotent():
    gen = ThreadedGenerator(lambda: itertools.count())
    gen.stop()
    gen.stop()
    gen.close()
    assert not gen.thread.is_alive()


def test_exception_from_worker_is_propagated():
    with ThreadedGenerator(failing_source) as gen:
        assert next(gen) == 1
        with pytest.raises(ValueError, match="сбой в потоке"):
            next(gen)
        with pytest.raises(StopIteration):
            next(gen)


def test_app_error_from_factory_is_propagated():
    with ThreadedGenerator(lambda: abs_range(5, 1)) as gen:
        with pytest.raises(InvalidRangeError):
            next(gen)


def test_thread_finishes_after_finite_source():
    gen = ThreadedGenerator(lambda: iter([1, 2]))
    assert list(gen) == [1, 2]
    gen.thread.join(timeout=2)
    assert not gen.thread.is_alive()


def test_thread_is_daemon():
    with ThreadedGenerator(lambda: itertools.count()) as gen:
        assert gen.thread.daemon


def test_context_manager_stops_thread():
    with ThreadedGenerator(lambda: itertools.count(), maxsize=1) as gen:
        next(gen)
    gen.thread.join(timeout=2)
    assert not gen.thread.is_alive()


def test_get_timeout():
    release = threading.Event()

    def blocked():
        release.wait()
        yield 1

    gen = ThreadedGenerator(blocked, get_timeout=0.1)
    try:
        with pytest.raises(GeneratorStoppedError):
            next(gen)
    finally:
        release.set()
        gen.stop()
    assert not gen.thread.is_alive()
