from combobox_and_label import ComboBoxAndLabel
from PySide2 import QtCore


def test_combobox_and_label(qtbot):
    widget = ComboBoxAndLabel()
    qtbot.addWidget(widget)

    assert widget.label.text() == "label: before selecting combobox"

    qtbot.keyClicks(widget.combobox, "Grape")

    assert widget.label.text() == "Grape"
