from PySide2 import QtCore, QtWidgets
import web3
from web3 import Web3, HTTPProvider
from populus.utils.wait import wait_for_transaction_receipt

w3 = Web3(HTTPProvider('http://localhost:7545'))

false = False
true = True
abi = [
            {
                "constant": false,
                "gas": 71987,
                "inputs": [
                    {
                        "name": "tweet",
                        "type": "bytes32"
                    }
                ],
                "name": "write_a_tweet",
                "outputs": [],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 968,
                "inputs": [
                    {
                        "name": "arg0",
                        "type": "address"
                    },
                    {
                        "name": "arg1",
                        "type": "int128"
                    }
                ],
                "name": "tweets__messages",
                "outputs": [
                    {
                        "name": "out",
                        "type": "bytes32"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 787,
                "inputs": [
                    {
                        "name": "arg0",
                        "type": "address"
                    }
                ],
                "name": "tweets__index",
                "outputs": [
                    {
                        "name": "out",
                        "type": "int128"
                    }
                ],
                "payable": false,
                "type": "function"
            }
        ]

with open('address.txt', 'r') as f:
    address = f.read().rstrip("\n")

TwitterOnBlockchain = w3.eth.contract(address=address, abi=abi)

def strip_x00_from_tweet(tweet):
    null_index = tweet.find(b'\x00')
    return tweet[:null_index]


class Web3ReadTweetsThread(QtCore.QThread):

    fetched_posts = QtCore.Signal(list)
    account = ''

    def __init__(self, parent=None):
        super(Web3ReadTweetsThread, self).__init__(parent)

    def setAccount(self, account):
        self.account = account

    def run(self):
        try:
            index = TwitterOnBlockchain.functions.tweets__index(Web3.toChecksumAddress(self.account)).call()
        except web3.exceptions.ValidationError:
            return
        tweets = []
        for i in range(index):
            tweet = TwitterOnBlockchain.functions.tweets__messages(Web3.toChecksumAddress(self.account), i).call()
            tweets.append(tweet.decode('utf-8'))
        self.fetched_posts.emit(tweets)


class Web3WriteATweetThread(QtCore.QThread):

    write_a_tweet = QtCore.Signal()
    private_key = ''
    tweet = ''

    def __init__(self, parent=None):
        super(Web3WriteATweetThread, self).__init__(parent)

    def setPrivateKey(self, private_key):
        self.private_key = private_key

    def setTweet(self, tweet):
        self.tweet = tweet

    def run(self):
        try:
            account = w3.eth.account.privateKeyToAccount('0x'+self.private_key)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Private key is invalid.')
            return
        nonce = w3.eth.getTransactionCount(Web3.toChecksumAddress(account.address))
        txn = TwitterOnBlockchain.functions.write_a_tweet(self.tweet.encode('utf-8')).buildTransaction({
                  'from': account.address,
                  'gas': 70000,
                  'gasPrice': w3.toWei('1', 'gwei'),
                  'nonce': nonce
              })
        signed = w3.eth.account.signTransaction(txn, private_key=self.private_key)
        txhash = w3.eth.sendRawTransaction(signed.rawTransaction)
        wait_for_transaction_receipt(w3, txhash)
        self.write_a_tweet.emit()


class TwitterDapp(QtWidgets.QWidget):

    private_key = '0x0'
    account = ''
    bookmark_file = 'bookmark.txt'
    addresses = []

    def __init__(self):
        super(TwitterDapp, self).__init__()

        self.createPrivateKeyGroupBox()
        self.createWritingTweetGroupBox()
        self.createTweetsGroupBox()
        self.createBookmarkGroupBox()

        self.setWindowTitle("Twitter-Like Blockchain Dapp")

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.private_key_group_box)
        mainLayout.addLayout(self.write_button_layout)
        mainLayout.addWidget(self.tweets_group_box)
        mainLayout.addWidget(self.bookmark_group_box)

        self.setLayout(mainLayout)

        self.web3_read_tweets_thread = Web3ReadTweetsThread()
        self.web3_read_tweets_thread.fetched_posts.connect(self.fillPosts)
        self.web3_write_a_tweet_thread = Web3WriteATweetThread()
        self.web3_write_a_tweet_thread.write_a_tweet.connect(self.successfullyWriteATweet)

    def createPrivateKeyGroupBox(self):
        self.private_key_group_box = QtWidgets.QGroupBox("Account")
        self.private_key_field = QtWidgets.QLineEdit()
        self.welcome_message = QtWidgets.QLabel()

        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Private key:"), self.private_key_field)
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        button_box.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.checkPrivateKey)
        layout.addRow(button_box)
        layout.addRow(self.welcome_message)

        self.private_key_group_box.setLayout(layout)

    def createWritingTweetGroupBox(self):
        self.tweet_button = QtWidgets.QPushButton("Write a new tweet")
        self.tweet_button.setMaximumSize(200,40)
        self.write_button_layout = QtWidgets.QHBoxLayout()
        self.write_button_layout.addWidget(self.tweet_button)
        self.connect(self.tweet_button, QtCore.SIGNAL('clicked()'), self.writeANewTweet)

    def createTweetsGroupBox(self):
        self.tweets_group_box = QtWidgets.QGroupBox("Tweets")
        self.account_address = QtWidgets.QLineEdit()
        self.fetch_button = QtWidgets.QPushButton("Fetch")
        self.add_to_bookmark_button = QtWidgets.QPushButton("Bookmark it!")

        self.connect(self.fetch_button, QtCore.SIGNAL('clicked()'), self.fetchTweets)
        self.connect(self.add_to_bookmark_button, QtCore.SIGNAL('clicked()'), self.bookmarkAddress)

        account_address_layout = QtWidgets.QHBoxLayout()
        account_address_layout.addWidget(self.account_address)
        account_address_layout.addWidget(self.fetch_button)
        account_address_layout.addWidget(self.add_to_bookmark_button)

        self.tweets_layout = QtWidgets.QVBoxLayout()

        self.tweets_main_layout = QtWidgets.QVBoxLayout()
        self.tweets_main_layout.addWidget(QtWidgets.QLabel("Address:"))
        self.tweets_main_layout.addLayout(account_address_layout)
        self.tweets_main_layout.addSpacing(20)
        self.tweets_main_layout.addLayout(self.tweets_layout)
        self.tweets_group_box.setLayout(self.tweets_main_layout)

    def createBookmarkGroupBox(self):
        self.bookmark_group_box = QtWidgets.QGroupBox("Bookmark")

        self.bookmark_layout = QtWidgets.QVBoxLayout()

        self.bookmark_group_box.setLayout(self.bookmark_layout)

        with open(self.bookmark_file) as f:
            addresses = f.readlines()
        self.addresses = list(map(lambda x: x.rstrip(), filter(lambda x: len(x) > 1, addresses)))
        self.fillBookmark()

    @QtCore.Slot()
    def fetchTweets(self):
        account = self.account_address.displayText()
        self.web3_read_tweets_thread.setAccount(account)
        self.web3_read_tweets_thread.start()

    @QtCore.Slot()
    def bookmarkAddress(self):
        account = self.account_address.displayText()
        if account:
            self.addresses.append(account)
            self.addresses = list(set(self.addresses))
        with open(self.bookmark_file, 'w') as f:
            for address in self.addresses:
                f.write(address + "\n")
        self.fillBookmark()

    @QtCore.Slot()
    def writeANewTweet(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Write a new tweet",
                 "Tweet:", QtWidgets.QLineEdit.Normal, "")
        if ok and text != '':
            self.web3_write_a_tweet_thread.setPrivateKey(self.private_key)
            self.web3_write_a_tweet_thread.setTweet(text)
            self.web3_write_a_tweet_thread.start()

    def checkPrivateKey(self):
        self.private_key = self.private_key_field.displayText()
        try:
            self.account = w3.eth.account.privateKeyToAccount('0x'+self.private_key)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Private key is invalid.')
            return
        self.welcome_message.setText('Welcome, ' + self.account.address + '!')
        self.private_key_field.clear()

    def clearTweetsField(self):
        while True:
            label_item = self.tweets_layout.takeAt(0)
            if label_item is None:
                break
            else:
                label_item.widget().close()

    def fillPosts(self, posts):
        self.clearTweetsField()
        for post in posts:
            label_field = QtWidgets.QLabel(post)
            self.tweets_layout.addWidget(label_field)

    def clearBookmarkField(self):
        while True:
            label_item = self.bookmark_layout.takeAt(0)
            if label_item is None:
                break
            else:
                label_item.widget().close()

    def fillBookmark(self):
        self.clearBookmarkField()
        for address in self.addresses:
            label_field = QtWidgets.QLabel(address)
            label_field.setTextInteractionFlags(label_field.textInteractionFlags() | QtCore.Qt.TextSelectableByMouse)
            self.bookmark_layout.addWidget(label_field)

    def successfullyWriteATweet(self):
        self.welcome_message.setText('You have successfully written a new tweet!')


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    twitter_dapp = TwitterDapp()
    twitter_dapp.show()
    sys.exit(app.exec_())
