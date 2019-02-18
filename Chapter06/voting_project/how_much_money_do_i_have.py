from web3 import Web3, IPCProvider

w3 = Web3(IPCProvider(ipc_path='/tmp/geth.ipc'))

print(w3.fromWei(w3.eth.getBalance(w3.eth.coinbase), 'ether'))
