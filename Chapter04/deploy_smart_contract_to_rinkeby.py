from web3 import Web3, IPCProvider
from vyper import compile_codes


contract_source_code = '''
name: public(bytes[24])

@public
def __init__():
    self.name = "Satoshi Nakamoto"

@public
def change_name(new_name: bytes[24]):
    self.name = new_name

@public
def say_hello() -> bytes[32]:
    return concat("Hello, ", self.name)
'''

smart_contract = {}
smart_contract['hello'] = contract_source_code

format = ['abi', 'bytecode']
compiled_code = compile_codes(smart_contract, format, 'dict')

bytecode = compiled_code['hello']['bytecode']
abi = compiled_code['hello']['abi']

# Change the path of geth.ipc according to your situation.
w3 = Web3(IPCProvider('/opt/data/ethereumdata/geth.ipc'))

HelloSmartContract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Change the account, the password, and the path to the keystore according to your situation,
from_account = "0x28f5b56b035da966afa609f65fd8f7d71ff68327"
password = 'password123'
with open('/opt/data/ethereumdata/keystore/UTC--2018-10-12T09-30-20.687898000Z--28f5b56b035da966afa609f65fd8f7d71ff68327') as keyfile:
    encrypted_key = keyfile.read()
    private_key = w3.eth.account.decrypt(encrypted_key, password)

nonce = w3.eth.getTransactionCount(Web3.toChecksumAddress(from_account))

transaction = HelloSmartContract.constructor().buildTransaction({'from': Web3.toChecksumAddress(from_account),
                                                                 'gas': 500000,
                                                                 'gasPrice': w3.toWei('30', 'gwei'),
                                                                 'nonce': nonce})

signed = w3.eth.account.signTransaction(transaction, private_key)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)
