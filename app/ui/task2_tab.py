from typing import Callable

from PySide6.QtWidgets import QPushButton

from app.ui.base_tab import BaseTab
from app.ui.workers import run_task2


class Task2Tab(BaseTab):
    def __init__(self) -> None:
        super().__init__("Сгенерировать")
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self._on_clear)
        self.buttons.insertWidget(1, self.clear_button)

    def build_task(self) -> Callable[[], list[str]]:
        return run_task2

    def _on_clear(self) -> None:
        self.output.clear()
        self.status.clear()
