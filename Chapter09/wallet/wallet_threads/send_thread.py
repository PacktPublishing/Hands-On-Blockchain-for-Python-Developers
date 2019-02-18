from PySide2.QtCore import QThread, Signal
from blockchain import blockchain


class SendThread(QThread):

    send_transaction = Signal()

    def __init__(self, parent=None):
        super(SendThread, self).__init__(parent)

    def prepareTransaction(self, tx):
        self.tx = tx

    def run(self):
        blockchain.create_send_transaction(self.tx)
        self.send_transaction.emit()
