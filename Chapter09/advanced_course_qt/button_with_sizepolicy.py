from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, QSizePolicy
from PySide2.QtCore import Qt
import sys


class ButtonWithSizePolicy(QWidget):

    def __init__(self):
        super(ButtonWithSizePolicy, self).__init__()

        button1 = QPushButton("button default")
        button2 = QPushButton("button maximum")
        button2.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button3 = QPushButton("button preferred")
        button3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        button4 = QPushButton("button expanding")
        button4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button5 = QPushButton("button minimum")
        button5.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        button6 = QPushButton("button minimum expanding")
        button6.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        layout = QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)
        layout.addWidget(button5)
        layout.addWidget(button6)

        self.setLayout(layout)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    button_with_size_policy_widget = ButtonWithSizePolicy()
    button_with_size_policy_widget.resize(500, 200)
    button_with_size_policy_widget.show()
    sys.exit(app.exec_())
