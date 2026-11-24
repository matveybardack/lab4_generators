from typing import Callable

from PySide6.QtCore import QThread, Signal

from app.exceptions import AppError
from app.generators import take
from app.generators.abs_range import DEFAULT_COUNT as TASK1_COUNT
from app.generators.abs_range import abs_range
from app.generators.multiply_pairs import first_three, multiply_pairs
from app.generators.passwords import DEFAULT_COUNT as TASK2_COUNT
from app.generators.passwords import passwords
from app.threading_utils.threaded_generator import ThreadedGenerator


def run_task1(a: int, b: int, count = TASK1_COUNT) -> list[str]:
    with ThreadedGenerator(lambda: abs_range(a, b)) as gen:
        return [str(v) for v in take(gen, count)]

def run_task2(count = TASK2_COUNT) -> list[str]:
    with ThreadedGenerator(lambda: passwords()) as gen:
        return take(gen, count)

def run_task3(first: list[int], second: list[int]) -> list[str]:
    with ThreadedGenerator(lambda: multiply_pairs(first, second)) as gen:
        return [str(v) for v in first_three(gen)]

class TaskWorker(QThread):
    """Выполняет задание в фоновом потоке и возвращает результат сигналами."""

    result_ready = Signal(list)
    error = Signal(str)

    def __init__(self, task: Callable[[], list[str]]) -> None:
        super().__init__()
        self._task = task

    def run(self) -> None:
        try:
            result = self._task()
        except AppError as exc:
            self.error.emit(str(exc))
        except Exception as exc:
            self.error.emit(f"Непредвиденная ошибка: {exc}")
        else:
            self.result_ready.emit(result)
