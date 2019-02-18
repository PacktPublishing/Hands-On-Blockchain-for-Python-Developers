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

bytecode = compiled_code['hello']['bytecode']
abi = compiled_code['hello']['abi']

w3 = Web3(HTTPProvider('http://localhost:7545'))

HelloSmartContract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Change the account to your situation.
tx_hash = HelloSmartContract.constructor().transact({'from': '0xb105F01Ce341Ef9282dc2201BDfdA2c26903da77'})

tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)
