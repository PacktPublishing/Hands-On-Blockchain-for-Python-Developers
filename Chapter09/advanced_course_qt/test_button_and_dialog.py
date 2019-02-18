from button_and_dialog import ButtonAndDialog
from PySide2.QtWidgets import QInputDialog
from PySide2 import QtCore


def test_button_and_dialog(qtbot, monkeypatch):
    widget = ButtonAndDialog()
    qtbot.addWidget(widget)

    monkeypatch.setattr(QInputDialog, 'getText', lambda *args: ("New Text", True))
    qtbot.mouseClick(widget.button, QtCore.Qt.LeftButton)

    assert widget.label.text() == "New Text"
