from typing import Callable, Optional

from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.exceptions import AppError
from app.ui.workers import TaskWorker


class BaseTab(QWidget):
    """Общая основа вкладки: поля ввода, кнопки, вывод и статус ошибок."""

    def __init__(self, run_text: str) -> None:
        super().__init__()
        self._worker: Optional[TaskWorker] = None

        self.form = QFormLayout()
        self.run_button = QPushButton(run_text)
        self.run_button.clicked.connect(self._on_run_clicked)
        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.run_button)
        self.buttons.addStretch()

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.status = QLabel()
        self.status.setWordWrap(True)
        self.status.setStyleSheet("color: #c0392b;")

        layout = QVBoxLayout(self)
        layout.addLayout(self.form)
        layout.addLayout(self.buttons)
        layout.addWidget(QLabel("Результат:"))
        layout.addWidget(self.output)
        layout.addWidget(self.status)

    def build_task(self) -> Callable[[], list[str]]:
        """Разобрать ввод и вернуть задание; при ошибке бросить AppError."""
        raise NotImplementedError

    def _on_run_clicked(self) -> None:
        self.status.clear()
        try:
            task = self.build_task()
        except AppError as exc:
            self.status.setText(str(exc))
            return
        self.run_button.setEnabled(False)
        self._worker = TaskWorker(task)
        self._worker.result_ready.connect(self._on_result)
        self._worker.error.connect(self.status.setText)
        self._worker.finished.connect(self._on_finished)
        self._worker.start()

    def _on_result(self, values: list) -> None:
        self.output.setPlainText("\n".join(values))

    def _on_finished(self) -> None:
        if self._worker is not None:
            self._worker.wait()
        self.run_button.setEnabled(True)

    def shutdown(self) -> None:
        """Дождаться завершения фонового потока (вызывается при закрытии окна)."""
        if self._worker is not None and self._worker.isRunning():
            self._worker.wait(5000)
