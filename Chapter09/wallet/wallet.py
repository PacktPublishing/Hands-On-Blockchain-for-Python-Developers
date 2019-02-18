from PySide2.QtWidgets import QTabWidget, QApplication
import sys

from wallet_widgets.account_widget import AccountWidget
from wallet_widgets.send_widget import SendWidget
from wallet_widgets.token_widget import TokenWidget


class WalletWidget(QTabWidget):

    def __init__(self, parent=None):
        super(WalletWidget, self).__init__(parent)
        self.account_widget = AccountWidget()
        self.send_widget = SendWidget()
        self.token_widget = TokenWidget()
        self.addTab(self.account_widget, "Account")
        self.addTab(self.send_widget, "Send")
        self.addTab(self.token_widget, "Token")

    def killThreads(self):
        self.account_widget.kill()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    wallet_widget = WalletWidget()
    wallet_widget.show()
    return_app = app.exec_()
    wallet_widget.killThreads()
    sys.exit(return_app)
