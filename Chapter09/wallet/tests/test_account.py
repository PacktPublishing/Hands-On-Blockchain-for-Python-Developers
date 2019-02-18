import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

from wallet import WalletWidget
from PySide2.QtWidgets import QInputDialog
from PySide2 import QtCore


def test_account(qtbot, monkeypatch):
    wallet = WalletWidget()
    qtbot.addWidget(wallet)

    old_accounts_amount = wallet.account_widget.accounts_layout.count()

    monkeypatch.setattr(QInputDialog, 'getText', lambda *args: ("password", True))
    qtbot.mouseClick(wallet.account_widget.create_account_button, QtCore.Qt.LeftButton)

    accounts_amount = wallet.account_widget.accounts_layout.count()
    assert accounts_amount == old_accounts_amount + 1

    wallet.killThreads()
