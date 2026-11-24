import queue
import threading
from typing import Any, Callable, Iterator, Union

from app.exceptions import GeneratorStoppedError

_END = object()

class _Failure:
    """Контейнер для исключения из рабочего потока."""

    def __init__(self, exc: BaseException) -> None:
        self.exc = exc


Source = Union[Iterator[Any], Callable[[], Iterator[Any]]]

class ThreadedGenerator:
    """Итератор, который исполняет исходный генератор в рабочем потоке.

    Значения передаются через ограниченную очередь. Исключение из рабочего
    потока повторно возникает в потребителе при вызове __next__.
    После stop() вызов __next__ бросает GeneratorStoppedError.
    """

    _PUT_POLL = 0.05
    _JOIN_TIMEOUT = 2.0

    def __init__(
        self, source: Source, maxsize: int = 100, get_timeout: float = 5.0
    ) -> None:
        self._source = source
        self._queue: queue.Queue = queue.Queue(maxsize=maxsize)
        self._stop_event = threading.Event()
        self._get_timeout = get_timeout
        self._finished = False
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    @property
    def thread(self) -> threading.Thread:
        return self._thread

    def _put(self, item: Any) -> bool:
        """Положить элемент; False, если запрошена остановка."""
        while not self._stop_event.is_set():
            try:
                self._queue.put(item, timeout=self._PUT_POLL)
                return True
            except queue.Full:
                continue
        return False

    def _run(self) -> None:
        iterator = None
        try:
            iterator = self._source() if callable(self._source) else self._source
            for item in iterator:
                if not self._put(item):
                    return
            self._put(_END)
        except BaseException as exc:  # передаём любую ошибку потребителю
            self._put(_Failure(exc))
        finally:
            close = getattr(iterator, "close", None)
            if close is not None:
                close()

    def __iter__(self) -> "ThreadedGenerator":
        return self

    def __next__(self) -> Any:
        if self._finished:
            raise StopIteration
        if self._stop_event.is_set():
            raise GeneratorStoppedError("Генератор остановлен.")
        try:
            item = self._queue.get(timeout=self._get_timeout)
        except queue.Empty:
            raise GeneratorStoppedError(
                "Рабочий поток не выдал значение за отведённое время."
            ) from None
        if item is _END:
            self._finished = True
            raise StopIteration
        if isinstance(item, _Failure):
            self._finished = True
            raise item.exc
        return item

    def stop(self) -> None:
        """Остановить рабочий поток; повторный вызов безопасен."""
        self._stop_event.set()
        try:
            while True:
                self._queue.get_nowait()
        except queue.Empty:
            pass
        if self._thread is not threading.current_thread():
            self._thread.join(timeout=self._JOIN_TIMEOUT)

    close = stop

    def __enter__(self) -> "ThreadedGenerator":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()
