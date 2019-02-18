from PySide2.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout
from PySide2.QtCore import Qt
import sys


class ButtonAndList(QWidget):

    index = 0

    def __init__(self):
        super(ButtonAndList, self).__init__()

        self.button = QPushButton("button")
        self.button.clicked.connect(self.buttonClicked)

        self.v_layout = QVBoxLayout()

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addLayout(self.v_layout)

        self.setLayout(layout)

    def buttonClicked(self):
        self.index += 1
        label = QLabel(str(self.index))
        self.v_layout.addWidget(label)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    button_and_list = ButtonAndList()
    button_and_list.show()
    sys.exit(app.exec_())
