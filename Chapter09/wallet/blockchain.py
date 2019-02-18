from web3 import Web3, IPCProvider
from web3.exceptions import ValidationError
from populus.utils.wait import wait_for_transaction_receipt
from collections import namedtuple
from os.path import exists
import json


SendTransaction = namedtuple("SendTransaction", "sender password destination amount fee")
TokenInformation = namedtuple("TokenInformation", "name symbol totalSupply address")

true = True
false = False
erc20_token_interface = [
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "name": "_from",
                        "type": "address"
                    },
                    {
                        "indexed": true,
                        "name": "_to",
                        "type": "address"
                    },
                    {
                        "indexed": false,
                        "name": "_value",
                        "type": "uint256"
                    }
                ],
                "name": "Transfer",
                "type": "event"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "name": "_owner",
                        "type": "address"
                    },
                    {
                        "indexed": true,
                        "name": "_spender",
                        "type": "address"
                    },
                    {
                        "indexed": false,
                        "name": "_value",
                        "type": "uint256"
                    }
                ],
                "name": "Approval",
                "type": "event"
            },
            {
                "constant": false,
                "inputs": [],
                "name": "__init__",
                "outputs": [],
                "payable": false,
                "type": "constructor"
            },
            {
                "constant": true,
                "gas": 655,
                "inputs": [
                    {
                        "name": "_owner",
                        "type": "address"
                    }
                ],
                "name": "balanceOf",
                "outputs": [
                    {
                        "name": "out",
                        "type": "uint256"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": false,
                "gas": 74459,
                "inputs": [
                    {
                        "name": "_to",
                        "type": "address"
                    },
                    {
                        "name": "_amount",
                        "type": "uint256"
                    }
                ],
                "name": "transfer",
                "outputs": [
                    {
                        "name": "out",
                        "type": "bool"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": false,
                "gas": 110866,
                "inputs": [
                    {
                        "name": "_from",
                        "type": "address"
                    },
                    {
                        "name": "_to",
                        "type": "address"
                    },
                    {
                        "name": "_value",
                        "type": "uint256"
                    }
                ],
                "name": "transferFrom",
                "outputs": [
                    {
                        "name": "out",
                        "type": "bool"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": false,
                "gas": 37779,
                "inputs": [
                    {
                        "name": "_spender",
                        "type": "address"
                    },
                    {
                        "name": "_amount",
                        "type": "uint256"
                    }
                ],
                "name": "approve",
                "outputs": [
                    {
                        "name": "out",
                        "type": "bool"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 935,
                "inputs": [
                    {
                        "name": "_owner",
                        "type": "address"
                    },
                    {
                        "name": "_spender",
                        "type": "address"
                    }
                ],
                "name": "allowance",
                "outputs": [
                    {
                        "name": "out",
                        "type": "uint256"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 3116,
                "inputs": [],
                "name": "name",
                "outputs": [
                    {
                        "name": "out",
                        "type": "bytes"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 2103,
                "inputs": [],
                "name": "symbol",
                "outputs": [
                    {
                        "name": "out",
                        "type": "bytes"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 693,
                "inputs": [],
                "name": "totalSupply",
                "outputs": [
                    {
                        "name": "out",
                        "type": "uint256"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 723,
                "inputs": [],
                "name": "decimals",
                "outputs": [
                    {
                        "name": "out",
                        "type": "uint256"
                    }
                ],
                "payable": false,
                "type": "function"
            }
        ]


class Blockchain:

    tokens_file = 'tokens.json'

    def __init__(self):
        self.w3 = Web3(IPCProvider('/tmp/geth.ipc'))

    def get_accounts(self):
        return map(lambda account: (account, self.w3.fromWei(self.w3.eth.getBalance(account), 'ether')), self.w3.eth.accounts)

    def create_new_account(self, password):
        return self.w3.personal.newAccount(password)

    def get_balance(self, address):
        return self.w3.fromWei(self.w3.eth.getBalance(address), 'ether')

    def get_token_balance(self, account_address, token_information):
        try:
            token_contract = self.w3.eth.contract(address=token_information.address, abi=erc20_token_interface)
            balance = token_contract.functions.balanceOf(account_address).call()
        except ValidationError:
            return None
        return balance

    def create_send_transaction(self, tx):
        nonce = self.w3.eth.getTransactionCount(tx.sender)
        transaction = {
          'from': tx.sender,
          'to': Web3.toChecksumAddress(tx.destination),
          'value': self.w3.toWei(str(tx.amount), 'ether'),
          'gas': 21000,
          'gasPrice': self.w3.toWei(str(tx.fee), 'gwei'),
          'nonce': nonce
        }

        tx_hash = self.w3.personal.sendTransaction(transaction, tx.password)
        wait_for_transaction_receipt(self.w3, tx_hash)

    def create_send_token_transaction(self, tx, token_information):
        nonce = self.w3.eth.getTransactionCount(tx.sender)
        token_contract = self.w3.eth.contract(address=token_information.address, abi=erc20_token_interface)
        transaction = token_contract.functions.transfer(tx.destination, int(tx.amount)).buildTransaction({
                  'from': tx.sender,
                  'gas': 70000,
                  'gasPrice': self.w3.toWei(str(tx.fee), 'gwei'),
                  'nonce': nonce
              })

        tx_hash = self.w3.personal.sendTransaction(transaction, tx.password)
        wait_for_transaction_receipt(self.w3, tx_hash)

    def get_information_of_token(self, address):
        try:
            token_contract = self.w3.eth.contract(address=address, abi=erc20_token_interface)
            name = token_contract.functions.name().call()
            symbol = token_contract.functions.symbol().call()
            total_supply = token_contract.functions.totalSupply().call()
        except ValidationError:
            return None
        token_information = TokenInformation(name=name.decode('utf-8'),
                                             symbol=symbol.decode('utf-8'),
                                             totalSupply=total_supply,
                                             address=address)
        return token_information

    def get_token_named_tuple(self, token_dict, address):
        return TokenInformation(name=token_dict['name'],
                                totalSupply=token_dict['total_supply'],
                                symbol=token_dict['symbol'],
                                address=address)

    def get_tokens(self):
        tokens = {}
        if exists(self.tokens_file):
            with open(self.tokens_file) as json_data:
                tokens = json.load(json_data)
        return tokens


blockchain = Blockchain()
