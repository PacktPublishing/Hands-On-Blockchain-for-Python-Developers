from web3 import Web3, IPCProvider

w3 = Web3(IPCProvider(ipc_path='/tmp/geth.ipc'))

false = False
true = True
abi = [
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "name": "_from",
                        "type": "address"
                    },
                    {
                        "indexed": false,
                        "name": "_proposal",
                        "type": "int128"
                    }
                ],
                "name": "Voting",
                "type": "event"
            },
            {
                "constant": false,
                "inputs": [
                    {
                        "name": "_proposalNames",
                        "type": "bytes32[2]"
                    }
                ],
                "name": "__init__",
                "outputs": [],
                "payable": false,
                "type": "constructor"
            },
            {
                "constant": false,
                "gas": 73421,
                "inputs": [
                    {
                        "name": "proposal",
                        "type": "int128"
                    }
                ],
                "name": "vote",
                "outputs": [],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 4006,
                "inputs": [],
                "name": "winner_name",
                "outputs": [
                    {
                        "name": "out",
                        "type": "bytes32"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 868,
                "inputs": [
                    {
                        "name": "arg0",
                        "type": "int128"
                    }
                ],
                "name": "proposals__name",
                "outputs": [
                    {
                        "name": "out",
                        "type": "bytes32"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 904,
                "inputs": [
                    {
                        "name": "arg0",
                        "type": "int128"
                    }
                ],
                "name": "proposals__vote_count",
                "outputs": [
                    {
                        "name": "out",
                        "type": "int128"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 633,
                "inputs": [],
                "name": "proposals_count",
                "outputs": [
                    {
                        "name": "out",
                        "type": "int128"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 835,
                "inputs": [
                    {
                        "name": "arg0",
                        "type": "address"
                    }
                ],
                "name": "voters_voted",
                "outputs": [
                    {
                        "name": "out",
                        "type": "int128"
                    }
                ],
                "payable": false,
                "type": "function"
            }
        ]

with open('address.txt', 'r') as f:
    content = f.read().rstrip("\n")

address = content

SimpleVoting = w3.eth.contract(address=address, abi=abi)

event_filter = SimpleVoting.events.Voting.createFilter(fromBlock=1)

import time
while True:
    print(event_filter.get_new_entries())
    time.sleep(2)
