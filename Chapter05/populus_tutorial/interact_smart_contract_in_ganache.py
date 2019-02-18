from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider("http://localhost:7545"))

print(w3.eth.coinbase)
print(w3.eth.getBalance(w3.eth.coinbase))

# Change this address to your smart contract address
address = "0x9Dc44aa8d05c86388E647F954D00CaA858837804"
false = False
true = True
abi = [
            {
                "constant": false,
                "inputs": [],
                "name": "__init__",
                "outputs": [],
                "payable": false,
                "type": "constructor"
            },
            {
                "constant": false,
                "gas": 317989,
                "inputs": [
                    {
                        "name": "name",
                        "type": "bytes"
                    }
                ],
                "name": "donate",
                "outputs": [],
                "payable": true,
                "type": "function"
            },
            {
                "constant": false,
                "gas": 35996,
                "inputs": [],
                "name": "withdraw_donation",
                "outputs": [],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 793,
                "inputs": [
                    {
                        "name": "arg0",
                        "type": "address"
                    }
                ],
                "name": "donatur_details__sum",
                "outputs": [
                    {
                        "name": "out",
                        "type": "uint256"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 18462,
                "inputs": [
                    {
                        "name": "arg0",
                        "type": "address"
                    }
                ],
                "name": "donatur_details__name",
                "outputs": [
                    {
                        "name": "out",
                        "type": "bytes"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 853,
                "inputs": [
                    {
                        "name": "arg0",
                        "type": "address"
                    }
                ],
                "name": "donatur_details__time",
                "outputs": [
                    {
                        "name": "out",
                        "type": "uint256"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 850,
                "inputs": [
                    {
                        "name": "arg0",
                        "type": "int128"
                    }
                ],
                "name": "donaturs",
                "outputs": [
                    {
                        "name": "out",
                        "type": "address"
                    }
                ],
                "payable": false,
                "type": "function"
            },
            {
                "constant": true,
                "gas": 663,
                "inputs": [],
                "name": "donatee",
                "outputs": [
                    {
                        "name": "out",
                        "type": "address"
                    }
                ],
                "payable": false,
                "type": "function"
            }
        ]

donation = w3.eth.contract(address=address, abi=abi)
print(donation.functions.donatee().call())
