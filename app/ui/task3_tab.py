from typing import Callable

from PySide6.QtWidgets import QLineEdit

from app.ui.base_tab import BaseTab
from app.ui.workers import run_task3
from app.validators import parse_int_list, validate_lists


class Task3Tab(BaseTab):
    def __init__(self) -> None:
        super().__init__("Выполнить")
        self.first_edit = QLineEdit()
        self.first_edit.setPlaceholderText("например: 1, 2, 3, 4")
        self.second_edit = QLineEdit()
        self.second_edit.setPlaceholderText("например: 5 6 7 8")
        self.form.addRow("Первый список:", self.first_edit)
        self.form.addRow("Второй список:", self.second_edit)

    def build_task(self) -> Callable[[], list[str]]:
        first = parse_int_list(self.first_edit.text(), "Первый список")
        second = parse_int_list(self.second_edit.text(), "Второй список")
        validate_lists(first, second)
        return lambda: run_task3(first, second)
