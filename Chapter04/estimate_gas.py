from web3 import Web3, HTTPProvider


w3 = Web3(HTTPProvider('http://localhost:7545'))

transaction = {
  'to': Web3.toChecksumAddress('0x9049386D4d5808e0Cd9e294F2aA3d70F01Fbf0C5'),
  'value': w3.toWei('1', 'ether'),
  'gas': 100000,
  'gasPrice': w3.toWei('1', 'gwei'),
  'nonce': 0
}

print("Estimating gas usage: " + str(w3.eth.estimateGas(transaction)))
print("Gas price: " + str(w3.eth.gasPrice))
