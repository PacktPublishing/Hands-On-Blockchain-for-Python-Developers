import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from time import sleep

from wallet import WalletWidget
from PySide2.QtWidgets import QInputDialog
from PySide2 import QtCore


def test_send(qtbot, monkeypatch):
    wallet = WalletWidget()
    qtbot.addWidget(wallet)

    monkeypatch.setattr(QInputDialog, 'getText', lambda *args: ("this-is-not-a-secure-password", True))

    first_account = wallet.send_widget.sender_items[0]
    second_account = wallet.send_widget.sender_items[1]

    qtbot.keyClicks(wallet.send_widget.sender_combo_box, second_account)
    old_balance_of_second_account = int(float(wallet.send_widget.balance_label.text().split()[1]))
    sleep(1)

    qtbot.keyClicks(wallet.send_widget.destination_line_edit, second_account)
    sleep(1)

    qtbot.keyClicks(wallet.send_widget.sender_combo_box, first_account)
    sleep(1)

    qtbot.keyClicks(wallet.send_widget.amount_line_edit, "10")
    sleep(1)

    qtbot.mouseClick(wallet.send_widget.send_button, QtCore.Qt.LeftButton)

    sleep(20)

    qtbot.keyClicks(wallet.send_widget.sender_combo_box, second_account)
    balance_of_second_account = int(float(wallet.send_widget.balance_label.text().split()[1]))

    assert balance_of_second_account - old_balance_of_second_account == 10

    wallet.killThreads()
