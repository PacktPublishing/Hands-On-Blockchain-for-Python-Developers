from web3 import Web3, IPCProvider

w3 = Web3(IPCProvider(ipc_path='/tmp/geth.ipc'))

with open('address.txt', 'r') as f:
    content = f.read().rstrip("\n")

address = content


