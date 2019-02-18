from web3 import Web3, HTTPProvider
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

abi = compiled_code['hello']['abi']

w3 = Web3(HTTPProvider('http://localhost:7545'))

# Change the address of the smart contract, the private key, and the account according to your situation
address = "0x9Dc44aa8d05c86388E647F954D00CaA858837804"
private_key = '0x1a369cedacf0bf2f5fd16b5215527e8c8767cbd761ebefa28d9df0d389c60b6e'
w3.eth.defaultAccount = '0xb105F01Ce341Ef9282dc2201BDfdA2c26903da77'

Hello = w3.eth.contract(address=address, abi=abi)

print(Hello.functions.name().call())

print(Hello.functions.say_hello().call())

nonce = w3.eth.getTransactionCount(w3.eth.defaultAccount)

txn = Hello.functions.change_name(b"Lionel Messi").buildTransaction({
        'gas': 70000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
      })

signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key)

signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

w3.eth.waitForTransactionReceipt(signed_txn_hash)

print(Hello.functions.say_hello().call())
