from typing import Callable

from PySide6.QtWidgets import QLineEdit

from app.ui.base_tab import BaseTab
from app.ui.workers import run_task1
from app.validators import parse_int, validate_range


class Task1Tab(BaseTab):
    def __init__(self) -> None:
        super().__init__("Выполнить")
        self.a_edit = QLineEdit()
        self.b_edit = QLineEdit()
        self.form.addRow("Левая граница a:", self.a_edit)
        self.form.addRow("Правая граница b:", self.b_edit)

    def build_task(self) -> Callable[[], list[str]]:
        a = parse_int(self.a_edit.text(), "a")
        b = parse_int(self.b_edit.text(), "b")
        validate_range(a, b)
        return lambda: run_task1(a, b)
