from PySide2.QtCore import QThread, Signal
from time import sleep
from blockchain import blockchain


class BalanceThread(QThread):

    get_balance_transaction = Signal(map)

    def __init__(self, parent=None):
        super(BalanceThread, self).__init__(parent)
        self.quit = False

    def kill(self):
        self.quit = True

    def run(self):
        while True:
            sleep(2)
            if self.quit:
                break
            accounts = blockchain.get_accounts()
            self.get_balance_transaction.emit(accounts)
