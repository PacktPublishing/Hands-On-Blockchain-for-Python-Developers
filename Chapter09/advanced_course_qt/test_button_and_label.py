from button_and_label import ButtonAndLabel
from PySide2 import QtCore


def test_button_and_label(qtbot):
    widget = ButtonAndLabel()
    qtbot.addWidget(widget)

    assert widget.label.text() == "label: before clicked"

    qtbot.mouseClick(widget.button, QtCore.Qt.LeftButton)

    assert widget.label.text() == "label: after clicked"
