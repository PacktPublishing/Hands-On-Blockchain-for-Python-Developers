import sys
from PySide2.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.resize(400, 400)

window.show()
sys.exit(app.exec_())
