class AppError(Exception):
    """Базовое исключение приложения.

    Все ожидаемые ошибки наследуются от него, поэтому GUI может ловить
    только AppError и показывать пользователю понятное сообщение.
    """


class InvalidInputError(AppError):
    """Некорректный ввод: пустая строка, не число, неверные параметры."""


class InvalidRangeError(AppError):
    """Некорректный диапазон: нарушено условие a < b."""


class InvalidListsError(AppError):
    """Пустые или несовместимые списки (разная длина, слишком короткие)."""


class NotEnoughValuesError(AppError):
    """Генератор выдал меньше значений, чем требуется."""


class GeneratorStoppedError(AppError):
    """Обращение к многопоточному генератору, рабочий поток которого остановлен."""
