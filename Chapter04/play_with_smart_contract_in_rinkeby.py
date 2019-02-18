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

abi = compiled_code['hello']['abi']

# Change the path of geth.ipc according to your situation.
w3 = Web3(IPCProvider('/opt/data/ethereumdata/geth.ipc'))

from web3.middleware import geth_poa_middleware
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

# Change the address of the smart contract, the account, the password, and the path to the keystore according to your situation,
address = "0x58705EBBc791DB917c7771FdA6175b2D9F59D51A"
password = 'password123'
w3.eth.defaultAccount = '0x28f5b56b035da966afa609f65fd8f7d71ff68327'
with open('/opt/data/ethereumdata/keystore/UTC--2018-10-12T09-30-20.687898000Z--28f5b56b035da966afa609f65fd8f7d71ff68327') as keyfile:
    encrypted_key = keyfile.read()
    private_key = w3.eth.account.decrypt(encrypted_key, password)

Hello = w3.eth.contract(address=address, abi=abi)

print(Hello.functions.name().call())

print(Hello.functions.say_hello().call())

nonce = w3.eth.getTransactionCount(w3.eth.defaultAccount)

txn = Hello.functions.change_name(b"Lionel Messi").buildTransaction({
        'gas': 500000,
        'gasPrice': w3.toWei('30', 'gwei'),
        'nonce': nonce
      })

signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key)

signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

w3.eth.waitForTransactionReceipt(signed_txn_hash)

print(Hello.functions.say_hello().call())
