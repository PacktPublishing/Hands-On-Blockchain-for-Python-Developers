import pytest
import eth_tester


def test_balance(web3, chain):
    simple_token, _ = chain.provider.get_or_deploy_contract('SimpleToken')

    balance = simple_token.functions.balances(web3.eth.coinbase).call()
    assert balance == 10000

def test_transfer(web3, chain):
    simple_token, _ = chain.provider.get_or_deploy_contract('SimpleToken')

    t = eth_tester.EthereumTester()
    account2 = t.get_accounts()[1]

    old_balance = simple_token.functions.balances(account2).call()
    assert old_balance == 0

    set_txn_hash = simple_token.functions.transfer(account2, 10).transact({'from': web3.eth.coinbase})
    chain.wait.for_receipt(set_txn_hash)

    sender_new_balance = simple_token.functions.balances(web3.eth.coinbase).call()
    assert sender_new_balance == 9990
    destination_new_balance = simple_token.functions.balances(account2).call()
    assert destination_new_balance == 10

def test_fail_transfer(web3, chain):
    simple_token, _ = chain.provider.get_or_deploy_contract('SimpleToken')

    t = eth_tester.EthereumTester()
    account2 = t.get_accounts()[1]

    with pytest.raises(eth_tester.exceptions.TransactionFailed):
        simple_token.functions.transfer(web3.eth.coinbase, 10).transact({'from': account2})
