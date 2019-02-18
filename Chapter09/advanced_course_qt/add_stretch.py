from PySide2.QtWidgets import QFrame, QLabel, QWidget, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy, QSizePolicy
from PySide2.QtCore import Qt
import sys


class AddStretch(QWidget):

    def __init__(self):
        super(AddStretch, self).__init__()

        label1 = QLabel("label 1")
        label1.setFrameStyle(QFrame.Box)
        label2 = QLabel("label 2")
        label2.setFrameStyle(QFrame.Box)
        label3 = QLabel("label 3")
        label3.setFrameStyle(QFrame.Box)
        label4 = QLabel("label 4")
        label4.setFrameStyle(QFrame.Box)
        label5 = QLabel("label 5")
        label5.setFrameStyle(QFrame.Box)
        label6 = QLabel("label 6")
        label6.setFrameStyle(QFrame.Box)
        label7 = QLabel("label 7")
        label7.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        label7.setFrameStyle(QFrame.Box)
        label8 = QLabel("label 8")
        label8.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        label8.setFrameStyle(QFrame.Box)

        layout = QHBoxLayout()

        v_layout1 = QVBoxLayout()
        v_layout1.addWidget(label1)
        v_layout1.addWidget(label2)

        v_layout2 = QVBoxLayout()
        v_layout2.addWidget(label3)
        v_layout2.addWidget(label4)
        v_layout2.addStretch()

        v_layout3 = QVBoxLayout()
        v_layout3.addStretch()
        v_layout3.addWidget(label5)
        v_layout3.addWidget(label6)

        v_layout4 = QVBoxLayout()
        v_layout4.addWidget(label7)
        v_layout4.addWidget(label8)

        layout.addLayout(v_layout1)
        layout.addLayout(v_layout2)
        layout.addLayout(v_layout3)
        layout.addLayout(v_layout4)

        self.setLayout(layout)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    widget = AddStretch()
    widget.resize(500, 500)
    widget.show()
    sys.exit(app.exec_())
