from tabbed_window import TabbedWindow
from PySide2 import QtCore


def test_tabbed_window(qtbot):
    tabbed = TabbedWindow()
    qtbot.addWidget(tabbed)

    assert tabbed.widget2.label.text() == "label: before clicked"

    qtbot.mouseClick(tabbed.widget2.button, QtCore.Qt.LeftButton)

    assert tabbed.widget2.label.text() == "label: after clicked"
