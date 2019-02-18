from PySide2.QtWidgets import QWidget, QApplication, QLabel, QComboBox, QVBoxLayout
from PySide2.QtCore import Qt
import sys


class ComboBoxAndLabel(QWidget):

    def __init__(self):
        super(ComboBoxAndLabel, self).__init__()

        self.combobox = QComboBox()
        self.combobox.addItems(["Orange", "Apple", "Grape"])
        self.combobox.currentTextChanged.connect(self.comboboxSelected)

        self.label = QLabel("label: before selecting combobox")

        layout = QVBoxLayout()
        layout.addWidget(self.combobox)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def comboboxSelected(self, value):
        self.label.setText(value)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    combobox_and_label = ComboBoxAndLabel()
    combobox_and_label.show()
    sys.exit(app.exec_())
