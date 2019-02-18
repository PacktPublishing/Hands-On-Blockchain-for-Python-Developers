from button_and_list import ButtonAndList
from PySide2 import QtCore


def test_button_and_list(qtbot):
    widget = ButtonAndList()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.button, QtCore.Qt.LeftButton)
    qtbot.mouseClick(widget.button, QtCore.Qt.LeftButton)
    qtbot.mouseClick(widget.button, QtCore.Qt.LeftButton)

    label_item = widget.v_layout.takeAt(2)
    assert label_item.widget().text() == "3"

    label_item = widget.v_layout.takeAt(1)
    assert label_item.widget().text() == "2"

    label_item = widget.v_layout.takeAt(0)
    assert label_item.widget().text() == "1"
