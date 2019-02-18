from web3 import Web3, HTTPProvider

w3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
print(w3.eth.getCode('0x891dfe5Dbf551E090805CEee41b94bB2205Bdd17'))
