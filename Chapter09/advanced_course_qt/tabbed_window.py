from PySide2.QtWidgets import QTabWidget, QApplication, QWidget
import sys
from button_and_label import ButtonAndLabel


class TabbedWindow(QTabWidget):

    def __init__(self, parent=None):
        super(TabbedWindow, self).__init__(parent)
        widget1 = QWidget()
        self.widget2 = ButtonAndLabel()
        widget3 = QWidget()
        self.addTab(widget1, "Tab 1")
        self.addTab(self.widget2, "Tab 2")
        self.addTab(widget3, "Tab 3")


if __name__ == "__main__":

    app = QApplication(sys.argv)
    tabbedWindow = TabbedWindow()
    tabbedWindow.show()
    sys.exit(app.exec_())
