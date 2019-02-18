from web3 import Web3, IPCProvider
from populus.utils.wait import wait_for_transaction_receipt
import glob

w3 = Web3(IPCProvider(ipc_path='/tmp/geth.ipc'))

address = 'fa146d7af4b92eb1751c3c9c644fa436a60f7b75'

with open('chains/localblock/password') as f:
    password = f.read().rstrip("\n")

    encrypted_private_key_file = glob.glob('chains/localblock/chain_data/keystore/*' + address)[0]
    with open(encrypted_private_key_file) as f2:
        private_key = w3.eth.account.decrypt(f2.read(), password)

w3.eth.defaultAccount = w3.eth.coinbase

with open('10_accounts.txt', 'r') as f:
    accounts = f.readlines()
    for account in accounts:
        nonce = w3.eth.getTransactionCount(Web3.toChecksumAddress(w3.eth.defaultAccount))
        transaction = {
          'to': Web3.toChecksumAddress(account.rstrip("\n")),
          'value': w3.toWei('10', 'ether'),
          'gas': 1000000,
          'gasPrice': w3.toWei('20', 'gwei'),
          'nonce': nonce
        }

        signed = w3.eth.account.signTransaction(transaction, private_key)
        txhash = w3.eth.sendRawTransaction(signed.rawTransaction)
        wait_for_transaction_receipt(w3, txhash)

