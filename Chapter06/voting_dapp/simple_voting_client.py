from web3 import Web3, IPCProvider
from populus.utils.wait import wait_for_transaction_receipt
import glob

w3 = Web3(IPCProvider(ipc_path='/tmp/geth.ipc'))

with open('client_address.txt', 'r') as f:
    content = f.read().rstrip("\n")

address = content.lower()

encrypted_private_key_file = glob.glob('../voting_project/chains/localblock/chain_data/keystore/*' + address)[0]
with open(encrypted_private_key_file) as f:
    password = 'password123'
    private_key = w3.eth.account.decrypt(f.read(), password)
    w3.eth.defaultAccount = '0x' + address


false = False
true = True
abi = [
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "name": "_from",
                        "type": "address"
                    },
                    {
                        "indexed": false,
                        "name": "_proposal",
                        "type": "int128"
                    }
                ],
                "name": "Voting",
                "type": "event"
            },
            {
                "constant": false,
                "inputs": [
                    {
                        "name": "_proposalNames",
                        "type": "bytes32[2]"
                    }
                ],
                "name": "__init__",
                "outputs": [],
                "payable": false,
                "type": "constructor"
            },
            {
                "constant": false,
                "gas": 73421,
                "inputs": [
                    {
                        "name": "proposal",
                        "type": "int128"
                    }
                ],
                "name": "vote",
                "outputs": [],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 4006,
                "inputs": [],
                "name": "winner_name",
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
                "gas": 868,
                "inputs": [
                    {
                        "name": "arg0",
                        "type": "int128"
                    }
                ],
                "name": "proposals__name",
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
                "gas": 904,
                "inputs": [
                    {
                        "name": "arg0",
                        "type": "int128"
                    }
                ],
                "name": "proposals__vote_count",
                "outputs": [
                    {
                        "name": "out",
                        "type": "int128"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 633,
                "inputs": [],
                "name": "proposals_count",
                "outputs": [
                    {
                        "name": "out",
                        "type": "int128"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 835,
                "inputs": [
                    {
                        "name": "arg0",
                        "type": "address"
                    }
                ],
                "name": "voters_voted",
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
    content = f.read().rstrip("\n")

smart_contract_address = content

SimpleVoting = w3.eth.contract(address=smart_contract_address, abi=abi)

nonce = w3.eth.getTransactionCount(Web3.toChecksumAddress(w3.eth.defaultAccount))

txn = SimpleVoting.functions.vote(0).buildTransaction({
        'gas': 70000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
      })

signed = w3.eth.account.signTransaction(txn, private_key=private_key)
w3.eth.sendRawTransaction(signed.rawTransaction)
