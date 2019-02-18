from web3 import Web3, IPCProvider
from web3.middleware import geth_poa_middleware

# Change the path of geth.ipc according to your situation.
w3 = Web3(IPCProvider('/opt/data/ethereumdata/geth.ipc'))

w3.middleware_stack.inject(geth_poa_middleware, layer=0)

# Change the destination account, the sender account, the password, and the path to the keystore according to your situation,
password = 'password123'
from_account = "0x28f5b56b035da966afa609f65fd8f7d71ff68327"
to_account = '0x99fb2eee85acbf878d4154de73d5fb1b7e88c328'
with open('/opt/data/ethereumdata/keystore/UTC--2018-10-12T09-30-20.687898000Z--28f5b56b035da966afa609f65fd8f7d71ff68327') as keyfile:
    encrypted_key = keyfile.read()
    private_key = w3.eth.account.decrypt(encrypted_key, password)

nonce = w3.eth.getTransactionCount(Web3.toChecksumAddress(from_account))

transaction = {
  'to': Web3.toChecksumAddress(to_account),
  'value': w3.toWei('1', 'ether'),
  'gas': 21000,
  'gasPrice': w3.toWei('2', 'gwei'),
  'nonce': nonce
}

signed = w3.eth.account.signTransaction(transaction, private_key)
w3.eth.sendRawTransaction(signed.rawTransaction)
