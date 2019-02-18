from PySide2.QtWidgets import (QWidget,
                               QGridLayout,
                               QVBoxLayout,
                               QHBoxLayout,
                               QPushButton,
                               QLabel,
                               QInputDialog,
                               QLineEdit,
                               QToolTip,
                               QComboBox,
                               QApplication,
                               QSlider,
                               QSizePolicy)
from PySide2.QtCore import Slot, SIGNAL, QSize, Qt
from PySide2.QtGui import QPixmap, QMovie, QPalette, QColor
from os.path import isdir, exists
from os import mkdir
from time import sleep
import json
from tools.util import render_avatar
from blockchain import blockchain, SendTransaction, TokenInformation


class TokenWidget(QWidget):

    tokens_file = 'tokens.json'

    def __init__(self, parent=None):
        super(TokenWidget, self).__init__(parent)

        self.watch_token_button = QPushButton("Watch Token")

        tokens = blockchain.get_tokens()

        self.tokens_layout = QVBoxLayout()

        for address, token_from_json in tokens.items():
            token_information = blockchain.get_token_named_tuple(token_from_json, address)
            self._addTokenToWindow(token_information)

        layout = QGridLayout()

        self.watch_token_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.connect(self.watch_token_button, SIGNAL('clicked()'), self.watchNewToken)

        layout.addWidget(self.watch_token_button, 0, 0)
        layout.addLayout(self.tokens_layout, 1, 0)

        self.setLayout(layout)

    def _addTokenToWindow(self, token_information, resize_parent=False):
        wrapper_layout = QVBoxLayout()
        token_layout = QHBoxLayout()
        rows_layout = QVBoxLayout()
        token_label = QLabel(token_information.name)
        token_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        symbol_label = QLabel(token_information.symbol)
        symbol_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        total_supply_label = QLabel('Total Supply: %d coins' % token_information.totalSupply)
        total_supply_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        rows_layout.addWidget(token_label)
        rows_layout.addWidget(symbol_label)
        rows_layout.addWidget(total_supply_label)
        avatar = QLabel()
        img_filename = render_avatar(token_information.address)
        pixmap = QPixmap(img_filename)
        avatar.setPixmap(pixmap)
        token_layout.addWidget(avatar)
        token_layout.addLayout(rows_layout)
        wrapper_layout.addLayout(token_layout)
        wrapper_layout.addSpacing(20)
        self.tokens_layout.addLayout(wrapper_layout)

        if resize_parent:
            sizeHint = self.size()
            self.parentWidget().parentWidget().resize(QSize(sizeHint.width(), sizeHint.height() + 100))

    @Slot()
    def watchNewToken(self):
        address, ok = QInputDialog.getText(self, "Watch A New Token",
                 "Token Smart Contract:", QLineEdit.Normal)
        if ok and address != '':
            token_information = blockchain.get_information_of_token(address)
            self._addTokenToWindow(token_information, resize_parent=True)
            token_data = {}
            if exists(self.tokens_file):
                with open(self.tokens_file) as json_data:
                    token_data = json.load(json_data)
            token_data[token_information.address] = {'name': token_information.name,
                                                     'symbol': token_information.symbol,
                                                     'total_supply': token_information.totalSupply}
            with open(self.tokens_file, 'w') as outfile:
                json.dump(token_data, outfile)
