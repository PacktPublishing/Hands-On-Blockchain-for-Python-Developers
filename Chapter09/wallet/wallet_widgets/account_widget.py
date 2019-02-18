from PySide2.QtWidgets import (QWidget,
                               QGridLayout,
                               QVBoxLayout,
                               QHBoxLayout,
                               QPushButton,
                               QLabel,
                               QInputDialog,
                               QLineEdit,
                               QToolTip,
                               QApplication,
                               QSizePolicy)
from PySide2.QtCore import Slot, SIGNAL, QSize
from PySide2.QtGui import QPixmap, QIcon, QCursor, QClipboard
from time import sleep
from blockchain import blockchain
from tools.util import render_avatar
from wallet_threads.balance_thread import BalanceThread


class AccountWidget(QWidget):

    balance_widgets = {}

    def __init__(self, parent=None):
        super(AccountWidget, self).__init__(parent)

        self.create_account_button = QPushButton("Create Account")
        self.create_account_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.connect(self.create_account_button, SIGNAL('clicked()'), self.createNewAccount)

        self.accounts_layout = QVBoxLayout()

        accounts = blockchain.get_accounts()

        for account, balance in accounts:
            self._addAccountToWindow(account, balance)

        layout = QGridLayout()

        layout.addWidget(self.create_account_button, 0, 0)
        layout.addLayout(self.accounts_layout, 1, 0)

        self.setLayout(layout)

        self.balance_thread = BalanceThread()
        self.balance_thread.get_balance_transaction.connect(self._updateBalances)
        self.balance_thread.start()

    @Slot()
    def createNewAccount(self):
        password, ok = QInputDialog.getText(self, "Create A New Account",
                 "Password:", QLineEdit.Normal)
        if ok and password != '':
            new_account = blockchain.create_new_account(password)
            self._addAccountToWindow(new_account, 0, resize_parent=True)

    def copyAddress(self, address):
        QToolTip.showText(QCursor.pos(), "Address %s has been copied to clipboard!" % address)
        clipboard = QApplication.clipboard()
        clipboard.setText(address)

    def _addAccountToWindow(self, account, balance, resize_parent=False):
        wrapper_layout = QVBoxLayout()
        account_layout = QHBoxLayout()
        rows_layout = QVBoxLayout()
        address_layout = QHBoxLayout()
        account_label = QLabel(account)
        account_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        copy_button = QPushButton()
        copy_button.setAutoFillBackground(True)
        copy_button.setIcon(QIcon('icons/copy.svg'))
        self.connect(copy_button, SIGNAL('clicked()'), lambda: self.copyAddress(account))
        address_layout.addWidget(account_label)
        address_layout.addWidget(copy_button)
        balance_label = QLabel('Balance: %.5f ethers' % balance)
        balance_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.balance_widgets[account] = balance_label
        rows_layout.addLayout(address_layout)
        rows_layout.addWidget(balance_label)
        avatar = QLabel()
        img_filename = render_avatar(account)
        pixmap = QPixmap(img_filename)
        avatar.setPixmap(pixmap)
        account_layout.addWidget(avatar)
        account_layout.addLayout(rows_layout)
        wrapper_layout.addLayout(account_layout)
        wrapper_layout.addSpacing(20)
        self.accounts_layout.addLayout(wrapper_layout)

        if resize_parent:
            sizeHint = self.sizeHint()
            self.parentWidget().parentWidget().resize(QSize(sizeHint.width(), sizeHint.height() + 40))

    def kill(self):
        self.balance_thread.kill()
        sleep(2)

    @Slot()
    def _updateBalances(self, accounts):
        for account, balance in accounts:
            self.balance_widgets[account].setText('Balance: %.5f ethers' % balance)
