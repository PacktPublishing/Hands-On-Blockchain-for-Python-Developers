import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

app = QApplication(sys.argv)

hello_button = QPushButton('Hello')
very_label = QLabel('Very Very')
beautiful_button = QPushButton('Beautiful')
world_label = QLabel('World')

vertical_hello_button = QPushButton('Hello')
vertical_very_label = QLabel('Very Very')
vertical_beautiful_button = QPushButton('Beautiful')
vertical_world_label = QLabel('World')

vertical_layout = QVBoxLayout()
vertical_layout.addWidget(vertical_hello_button)
vertical_layout.addWidget(vertical_very_label)
vertical_layout.addWidget(vertical_beautiful_button)
vertical_layout.addWidget(vertical_world_label)

horizontal_layout = QHBoxLayout()
horizontal_layout.addWidget(hello_button)
horizontal_layout.addWidget(very_label)
horizontal_layout.addLayout(vertical_layout)
horizontal_layout.addWidget(beautiful_button)
horizontal_layout.addWidget(world_label)

window = QWidget()
window.setLayout(horizontal_layout)
window.resize(200, 200)

window.show()
sys.exit(app.exec_())
