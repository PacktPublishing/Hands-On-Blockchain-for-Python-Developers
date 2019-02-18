from web3 import Web3, IPCProvider

w3 = Web3(IPCProvider(ipc_path='/tmp/geth.ipc'))

with open('10_accounts.txt', 'w') as f:
    for i in range(10):
        f.write(w3.personal.newAccount('password123') + "\n")
