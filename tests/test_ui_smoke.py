import pytest

pytest.importorskip("pytestqt")

from app.ui.main_window import MainWindow


@pytest.fixture
def window(qtbot):
    win = MainWindow()
    qtbot.addWidget(win)
    win.show()
    return win


def run_and_wait(qtbot, tab):
    tab.run_button.click()
    qtbot.waitUntil(lambda: tab.run_button.isEnabled(), timeout=5000)


def test_three_tabs(window):
    assert window.tabs.count() == 3
    assert [window.tabs.tabText(i) for i in range(3)] == [
        "Задание №1",
        "Задание №2",
        "Задание №3",
    ]


def test_task1_invalid_input_shows_error(window):
    tab = window.tabs.widget(0)
    tab.a_edit.setText("abc")
    tab.b_edit.setText("5")
    tab.run_button.click()
    assert tab.status.text()
    assert tab.run_button.isEnabled()
    assert tab.output.toPlainText() == ""


def test_task1_wrong_range_shows_error(window):
    tab = window.tabs.widget(0)
    tab.a_edit.setText("5")
    tab.b_edit.setText("5")
    tab.run_button.click()
    assert "меньше" in tab.status.text()


def test_task1_valid(qtbot, window):
    tab = window.tabs.widget(0)
    tab.a_edit.setText("-3")
    tab.b_edit.setText("2")
    run_and_wait(qtbot, tab)
    assert tab.output.toPlainText() == "3\n2\n1\n0"
    assert tab.status.text() == ""


def test_task2_five_passwords(qtbot, window):
    tab = window.tabs.widget(1)
    run_and_wait(qtbot, tab)
    lines = tab.output.toPlainText().splitlines()
    assert len(lines) == 5
    assert all(len(line) == 12 for line in lines)
    tab.clear_button.click()
    assert tab.output.toPlainText() == ""


def test_task3_valid(qtbot, window):
    tab = window.tabs.widget(2)
    tab.first_edit.setText("1 2 3 4")
    tab.second_edit.setText("5, 6, 7, 8")
    run_and_wait(qtbot, tab)
    assert tab.output.toPlainText() == "5\n12\n21"


def test_task3_different_length(window):
    tab = window.tabs.widget(2)
    tab.first_edit.setText("1 2 3")
    tab.second_edit.setText("1 2")
    tab.run_button.click()
    assert tab.status.text()
    assert tab.run_button.isEnabled()


def test_task3_two_values_not_enough(qtbot, window):
    tab = window.tabs.widget(2)
    tab.first_edit.setText("1 2")
    tab.second_edit.setText("3 4")
    run_and_wait(qtbot, tab)
    assert "не менее 3" in tab.status.text()


def test_close_window(window):
    assert window.close()
