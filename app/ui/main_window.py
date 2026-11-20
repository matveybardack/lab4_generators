from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow, QTabWidget

from app.ui.base_tab import BaseTab
from app.ui.task1_tab import Task1Tab
from app.ui.task2_tab import Task2Tab
from app.ui.task3_tab import Task3Tab


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Generators Lab - лабораторная работа №4")
        self.setMinimumSize(520, 380)

        self.tabs = QTabWidget()
        self._task_tabs: list[BaseTab] = [Task1Tab(), Task2Tab(), Task3Tab()]
        titles = ("Задание №1", "Задание №2", "Задание №3")
        for tab, title in zip(self._task_tabs, titles):
            self.tabs.addTab(tab, title)
        self.setCentralWidget(self.tabs)

    def closeEvent(self, event: QCloseEvent) -> None:
        for tab in self._task_tabs:
            tab.shutdown()
        super().closeEvent(event)
