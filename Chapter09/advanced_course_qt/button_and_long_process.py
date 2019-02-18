from PySide2.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout
from PySide2.QtCore import Qt, QThread, Signal
import sys
from time import sleep


class LongProcessThread(QThread):

    transaction = Signal()

    def __init__(self, parent=None):
        super(LongProcessThread, self).__init__(parent)

    def run(self):
        sleep(3)
        self.transaction.emit()


class ButtonAndLongProcess(QWidget):

    def __init__(self):
        super(ButtonAndLongProcess, self).__init__()

        self.button = QPushButton("button")
        self.button.clicked.connect(self.buttonClicked)

        self.label = QLabel("label: before clicked")

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.long_process_thread = LongProcessThread()
        self.long_process_thread.transaction.connect(self.afterLongProcess)

    def afterLongProcess(self):
        self.label.setText("label: after clicked")

    def buttonClicked(self):
        self.long_process_thread.start()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    button_and_long_process = ButtonAndLongProcess()
    button_and_long_process.show()
    sys.exit(app.exec_())
