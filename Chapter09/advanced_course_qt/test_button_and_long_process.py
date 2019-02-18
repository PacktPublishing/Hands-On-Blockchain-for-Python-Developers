from button_and_long_process import ButtonAndLongProcess
from PySide2 import QtCore


def test_button_and_long_process(qtbot):
    widget = ButtonAndLongProcess()
    qtbot.addWidget(widget)

    assert widget.label.text() == "label: before clicked"

    qtbot.mouseClick(widget.button, QtCore.Qt.LeftButton)

    def check_label():
        assert widget.label.text() == "label: after clicked"

    qtbot.waitUntil(check_label, 4000)
