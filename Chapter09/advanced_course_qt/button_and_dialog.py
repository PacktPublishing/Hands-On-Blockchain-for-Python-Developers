from PySide2.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout, QInputDialog, QLineEdit
from PySide2.QtCore import Qt
import sys


class ButtonAndDialog(QWidget):

    def __init__(self):
        super(ButtonAndDialog, self).__init__()

        self.button = QPushButton("button")
        self.button.clicked.connect(self.buttonClicked)

        self.label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def buttonClicked(self):
        new_text, ok = QInputDialog.getText(self, "Create A Text",
                 "New Text:", QLineEdit.Normal)
        if ok and new_text != '':
            self.label.setText(new_text)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    button_and_dialog = ButtonAndDialog()
    button_and_dialog.show()
    sys.exit(app.exec_())
