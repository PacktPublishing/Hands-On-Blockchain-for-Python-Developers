from populus import Project
from populus.utils.wait import wait_for_transaction_receipt


def main():

    project = Project()

    chain_name = "ganache"

    with project.get_chain(chain_name) as chain:

        SimpleVoting = chain.provider.get_contract_factory('SimpleVoting')

        txhash = SimpleVoting.deploy(transaction={"from": chain.web3.eth.coinbase}, args=[[b'Messi', b'Ronaldo']])
        receipt = wait_for_transaction_receipt(chain.web3, txhash)
        simple_voting_address = receipt["contractAddress"]
        print("SimpleVoting contract address is", simple_voting_address)


if __name__ == "__main__":
    main()

