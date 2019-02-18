import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

from wallet import WalletWidget
from PySide2.QtWidgets import QInputDialog
from PySide2 import QtCore


def test_token(qtbot, monkeypatch):
    wallet = WalletWidget()
    qtbot.addWidget(wallet)

    old_tokens_amount = wallet.token_widget.tokens_layout.count()

    address = None
    with open('address.txt') as f:
        address = f.readline().rstrip()

    monkeypatch.setattr(QInputDialog, 'getText', lambda *args: (address, True))
    qtbot.mouseClick(wallet.token_widget.watch_token_button, QtCore.Qt.LeftButton)

    tokens_amount = wallet.token_widget.tokens_layout.count()
    assert tokens_amount == old_tokens_amount + 1

    wallet.killThreads()
