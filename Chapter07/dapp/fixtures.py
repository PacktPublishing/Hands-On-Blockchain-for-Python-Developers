from web3 import Web3, HTTPProvider
from populus.utils.wait import wait_for_transaction_receipt

w3 = Web3(HTTPProvider('http://localhost:7545'))

private_keys = ['dummy',
                '59e31694256f71b8d181f47fc67914798c4b96990e835fc1407bf4673ead30e2',
                'ac1e6abbe002699fbef756a2cbc2bf8c03cfac97adee84ce32f198219be94788']

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

for i in range(1, 3):
    for j in range(1, 11):
        nonce = w3.eth.getTransactionCount(Web3.toChecksumAddress(w3.eth.accounts[i]))
        txn = TwitterOnBlockchain.functions.write_a_tweet(b'Tweet ' + str(j).encode('utf-8')).buildTransaction({
                'gas': 70000,
                'gasPrice': w3.toWei('1', 'gwei'),
                'nonce': nonce
              })

        signed = w3.eth.account.signTransaction(txn, private_key=private_keys[i])
        txhash = w3.eth.sendRawTransaction(signed.rawTransaction)
        wait_for_transaction_receipt(w3, txhash)
