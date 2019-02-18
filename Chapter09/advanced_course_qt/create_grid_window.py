from PySide2.QtWidgets import QWidget, QApplication, QLabel, QGridLayout
from PySide2.QtCore import Qt
import sys


class GridWindow(QWidget):

    def __init__(self):
        super(GridWindow, self).__init__()

        layout = QGridLayout()

        label = QLabel("Label A")
        layout.addWidget(label, 0, 0)

        label = QLabel("Label B")
        layout.addWidget(label, 1, 0)

        label = QLabel("Label C")
        layout.addWidget(label, 2, 0)

        label = QLabel("Label D")
        layout.addWidget(label, 3, 0)

        label = QLabel("Label E")
        layout.addWidget(label, 0, 1)

        label = QLabel("Label F")
        layout.addWidget(label, 0, 2)

        label = QLabel("Label G")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 1, 2, 2)

        self.setLayout(layout)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    gridWindow = GridWindow()
    gridWindow.show()
    sys.exit(app.exec_())
