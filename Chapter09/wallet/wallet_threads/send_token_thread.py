from PySide2.QtCore import QThread, Signal
from blockchain import blockchain


class SendTokenThread(QThread):

    send_token_transaction = Signal()

    def __init__(self, parent=None):
        super(SendTokenThread, self).__init__(parent)

    def prepareTransaction(self, tx, token_information):
        self.tx = tx
        self.token_information = token_information

    def run(self):
        blockchain.create_send_token_transaction(self.tx, self.token_information)
        self.send_token_transaction.emit()
