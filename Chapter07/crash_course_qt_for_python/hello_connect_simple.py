import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide2 import QtCore

app = QApplication(sys.argv)

hello_button = QPushButton("Hello")
world_label = QLabel("Sun")

layout = QVBoxLayout()
layout.addWidget(hello_button)
layout.addWidget(world_label)

def set_text_in_world_label():
    world_label.setText("World")

hello_button.connect(QtCore.SIGNAL('clicked()'), set_text_in_world_label)

window = QWidget()
window.setLayout(layout)
window.resize(200, 200)

window.show()
sys.exit(app.exec_())
