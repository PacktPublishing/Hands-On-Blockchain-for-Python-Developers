from PySide2 import QtCore
import time

class SimpleThread(QtCore.QThread):

    def __init__(self, parent=None):
        super(SimpleThread, self).__init__(parent)

    def run(self):
        time.sleep(2) # simulating latency in network
        print("world")


simple_thread = SimpleThread()
simple_thread.start()

print("hello")
simple_thread.wait()
