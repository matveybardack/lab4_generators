import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox

from app.ui.main_window import MainWindow


def handle_exception(exc_type, exc, tb) -> None:
    traceback.print_exception(exc_type, exc, tb)
    if QApplication.instance() is not None:
        QMessageBox.critical(
            None, "Непредвиденная ошибка", f"{exc_type.__name__}: {exc}"
        )


def main() -> int:
    app = QApplication(sys.argv)
    sys.excepthook = handle_exception
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
