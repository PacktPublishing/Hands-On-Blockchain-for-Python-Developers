from web3 import Web3, HTTPProvider


w3 = Web3(HTTPProvider('http://localhost:7545'))

private_key = '59e31694256f71b8d181f47fc67914798c4b96990e835fc1407bf4673ead30e2'

transaction = {
  'to': Web3.toChecksumAddress('0x9049386D4d5808e0Cd9e294F2aA3d70F01Fbf0C5'),
  'value': w3.toWei('1', 'ether'),
  'gas': 100000,
  'gasPrice': w3.toWei('1', 'gwei'),
  'nonce': 0
}

signed = w3.eth.account.signTransaction(transaction, private_key)
tx = w3.eth.sendRawTransaction(signed.rawTransaction)
