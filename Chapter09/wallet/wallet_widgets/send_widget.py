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
from tools.util import render_avatar
from blockchain import blockchain, SendTransaction
from wallet_threads.send_thread import SendThread
from wallet_threads.send_token_thread import SendTokenThread


class SendWidget(QWidget):

    tokens_file = 'tokens.json'

    def __init__(self, parent=None):
        super(SendWidget, self).__init__(parent)

        self.token_name = 'Ethereum'

        self.setupSenderSection()
        self.setupDestinationSection()
        self.setupTokenSection()
        self.setupProgressSection()
        self.setupSendButtonSection()
        self.setupFeeSection()

        self.send_thread = SendThread()
        self.send_thread.send_transaction.connect(self.sendTransactionFinished)
        self.send_token_thread = SendTokenThread()
        self.send_token_thread.send_token_transaction.connect(self.sendTransactionFinished)

        layout = QGridLayout()

        layout.addLayout(self.sender_layout, 0, 0)
        layout.addLayout(self.destination_layout, 0, 1)
        layout.addLayout(self.progress_layout, 1, 0, 1, 2, Qt.AlignCenter)
        layout.addLayout(self.token_layout, 2, 0)
        layout.addLayout(self.send_layout, 2, 1)
        layout.addLayout(self.slider_layout, 3, 0)

        self.setLayout(layout)

    def setupSenderSection(self):
        accounts = blockchain.get_accounts()

        sender_label = QLabel("Sender")
        sender_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.balance_label = QLabel("Balance: ")
        self.balance_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.avatar = QLabel()

        self.sender_combo_box = QComboBox()
        self.sender_items = []
        for account, balance in accounts:
            self.sender_items.append(account)
        self.sender_combo_box.addItems(self.sender_items)
        self.sender_combo_box.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.sender_combo_box.currentTextChanged.connect(self.filterSender)

        first_account = self.sender_items[0]
        self.filterSender(first_account)
        self.setAvatar(first_account, self.avatar)

        self.sender_layout = QVBoxLayout()
        sender_wrapper_layout = QHBoxLayout()
        sender_right_layout = QVBoxLayout()
        sender_right_layout.addWidget(sender_label)
        sender_right_layout.addWidget(self.sender_combo_box)
        sender_right_layout.addWidget(self.balance_label)
        sender_wrapper_layout.addWidget(self.avatar)
        sender_wrapper_layout.addLayout(sender_right_layout)
        sender_wrapper_layout.addStretch()

        self.sender_layout.addLayout(sender_wrapper_layout)
        self.sender_layout.addStretch()

    def setupDestinationSection(self):
        self.destination_layout = QVBoxLayout()

        destination_label = QLabel("Destination")
        destination_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.destination_line_edit = QLineEdit()
        self.destination_line_edit.setFixedWidth(380);
        self.destination_line_edit.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.destination_layout.addWidget(destination_label)
        self.destination_layout.addWidget(self.destination_line_edit)
        self.destination_layout.addStretch()

    def setupTokenSection(self):
        token_label = QLabel("Token")
        token_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        token_combo_box = QComboBox()

        tokens = blockchain.get_tokens()
        first_token = 'Ethereum'
        items = [first_token]
        self.token_address = {'Ethereum': '0xcccccccccccccccccccccccccccccccccccccccc'}
        self.token_informations = {}

        for address, token_from_json in tokens.items():
            token_information = blockchain.get_token_named_tuple(token_from_json, address)
            self.token_informations[token_information.name] = token_information
            self.token_address[token_information.name] = token_information.address
            items.append(token_information.name)

        self.amount_label = QLabel("Amount (in ethers)")

        token_combo_box.addItems(items)
        token_combo_box.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        token_combo_box.currentTextChanged.connect(self.filterToken)

        self.token_avatar = QLabel()

        self.filterToken(first_token)
        token_address = self.token_address[first_token]
        self.setAvatar(token_address, self.token_avatar)

        self.token_layout = QVBoxLayout()
        token_wrapper_layout = QHBoxLayout()
        token_right_layout = QVBoxLayout()
        token_right_layout.addWidget(token_label)
        token_right_layout.addWidget(token_combo_box)
        token_wrapper_layout.addWidget(self.token_avatar)
        token_wrapper_layout.addLayout(token_right_layout)
        token_wrapper_layout.addStretch()
        self.token_layout.addLayout(token_wrapper_layout)

    def setupProgressSection(self):
        self.progress_layout = QHBoxLayout()
        progress_vertical_layout = QVBoxLayout()
        progress_wrapper_layout = QHBoxLayout()
        self.progress_label = QLabel()
        movie = QMovie('icons/ajax-loader.gif')
        self.progress_label.setMovie(movie)
        movie.start()
        self.progress_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.progress_description_label = QLabel()
        self.progress_description_label.setText("Transaction is being confirmed. Please wait!")
        self.progress_description_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        progress_wrapper_layout.addWidget(self.progress_label)
        progress_wrapper_layout.addWidget(self.progress_description_label)
        progress_vertical_layout.addLayout(progress_wrapper_layout, 1)
        self.progress_layout.addLayout(progress_vertical_layout)
        self.sendTransactionFinished()

    def setupSendButtonSection(self):
        self.send_layout = QVBoxLayout()
        self.amount_line_edit = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.send_button.clicked.connect(self.sendButtonClicked)
        pal = self.send_button.palette()
        pal.setColor(QPalette.Button, QColor(Qt.green))
        self.send_button.setAutoFillBackground(True)
        self.send_button.setPalette(pal)
        self.send_button.update()
        self.send_layout.addWidget(self.amount_label)
        self.send_layout.addWidget(self.amount_line_edit)
        self.send_layout.addWidget(self.send_button)

    def setupFeeSection(self):
        self.slider_layout = QVBoxLayout()
        fee_label = QLabel("Fee")
        self.fee_slider = QSlider(Qt.Horizontal)
        self.fee_slider.setRange(1, 10)
        self.fee_slider.setValue(3)
        self.fee_slider.valueChanged.connect(self.feeSliderChanged)
        self.gwei_label = QLabel()
        self.feeSliderChanged(3)
        self.slider_layout.addWidget(fee_label)
        self.slider_layout.addWidget(self.fee_slider)
        self.slider_layout.addWidget(self.gwei_label)

    def filterToken(self, token_name):
        address = self.token_address[token_name]
        token_information = None
        if token_name != 'Ethereum':
            token_information = self.token_informations[token_name]
            self.amount_label.setText("Amount")
        else:
            self.amount_label.setText("Amount (in ethers)")
        self.updateBalanceLabel(token_name, self.sender_account, token_information)
        self.setAvatar(address, self.token_avatar)
        self.token_name = token_name

    def filterSender(self, account_address):
        self.sender_account = account_address
        token_information = None
        if self.token_name != 'Ethereum':
            token_information = self.token_informations[self.token_name]
        self.updateBalanceLabel(self.token_name, account_address, token_information)
        self.setAvatar(account_address, self.avatar)

    def updateBalanceLabel(self, token_name, account_address, token_information=None):
        if token_name == 'Ethereum':
            self.balance_label.setText("Balance: %.5f ethers" % blockchain.get_balance(account_address))
        else:
            self.balance_label.setText("Balance: %d coins" % blockchain.get_token_balance(account_address, token_information))

    def setAvatar(self, code, avatar):
        img_filename = render_avatar(code)
        pixmap = QPixmap(img_filename)
        avatar.setPixmap(pixmap)

    def feeSliderChanged(self, value):
        self.gwei_label.setText("%d GWei" % value)
        self.fee = value

    def sendButtonClicked(self):
        password, ok = QInputDialog.getText(self, "Create A New Transaction",
                 "Password:", QLineEdit.Password)
        if ok and password != '':
            self.progress_label.setVisible(True)
            self.progress_description_label.setVisible(True)
            tx = SendTransaction(sender=self.sender_account,
                                 password=password,
                                 destination=self.destination_line_edit.text(),
                                 amount=self.amount_line_edit.text(),
                                 fee=self.fee)
            token_information = None
            if self.token_name != 'Ethereum':
                token_information = self.token_informations[self.token_name]
                self.send_token_thread.prepareTransaction(tx, token_information)
                self.send_token_thread.start()
            else:
                self.send_thread.prepareTransaction(tx)
                self.send_thread.start()

    def sendTransactionFinished(self):
        self.progress_label.setVisible(False)
        self.progress_description_label.setVisible(False)
