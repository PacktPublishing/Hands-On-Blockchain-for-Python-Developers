import pytest
import eth_tester


def test_balance(web3, chain):
    erc20_token, _ = chain.provider.get_or_deploy_contract('ERC20Token')

    token_name = erc20_token.functions.name().call()
    token_symbol = erc20_token.functions.symbol().call()
    decimals = erc20_token.functions.decimals().call()
    total_supply = erc20_token.functions.totalSupply().call()
    balance = erc20_token.functions.balanceOf(web3.eth.coinbase).call()

    assert token_name == b"Haha Coin"
    assert token_symbol == b"HAH"
    assert decimals == 3
    assert total_supply == 1000000
    assert balance == 1000000

def test_transfer(web3, chain):
    erc20_token, _ = chain.provider.get_or_deploy_contract('ERC20Token')

    t = eth_tester.EthereumTester()
    account2 = t.get_accounts()[1]

    old_balance = erc20_token.functions.balanceOf(account2).call()
    assert old_balance == 0

    set_txn_hash = erc20_token.functions.transfer(account2, 10).transact({'from': web3.eth.coinbase})
    chain.wait.for_receipt(set_txn_hash)

    sender_new_balance = erc20_token.functions.balanceOf(web3.eth.coinbase).call()
    assert sender_new_balance == 999990
    destination_new_balance = erc20_token.functions.balanceOf(account2).call()
    assert destination_new_balance == 10

def test_fail_transfer(web3, chain):
    erc20_token, _ = chain.provider.get_or_deploy_contract('ERC20Token')

    t = eth_tester.EthereumTester()
    account2 = t.get_accounts()[1]

    with pytest.raises(eth_tester.exceptions.TransactionFailed):
        erc20_token.functions.transfer(web3.eth.coinbase, 10).transact({'from': account2})

def test_approve(web3, chain):
    erc20_token, _ = chain.provider.get_or_deploy_contract('ERC20Token')

    t = eth_tester.EthereumTester()
    account2 = t.get_accounts()[1]

    allowance = erc20_token.functions.allowance(web3.eth.coinbase, account2).call()
    assert allowance == 0

    set_txn_hash = erc20_token.functions.approve(account2, 100).transact({'from': web3.eth.coinbase})
    chain.wait.for_receipt(set_txn_hash)

    allowance = erc20_token.functions.allowance(web3.eth.coinbase, account2).call()
    assert allowance == 100

def test_transferFrom(web3, chain):
    erc20_token, _ = chain.provider.get_or_deploy_contract('ERC20Token')

    t = eth_tester.EthereumTester()
    account2 = t.get_accounts()[1]
    account3 = t.get_accounts()[2]

    with pytest.raises(eth_tester.exceptions.TransactionFailed):
        erc20_token.functions.transferFrom(web3.eth.coinbase, account3, 10).transact({'from': account2})

    set_txn_hash = erc20_token.functions.approve(account2, 100).transact({'from': web3.eth.coinbase})
    chain.wait.for_receipt(set_txn_hash)

    set_txn_hash = erc20_token.functions.transferFrom(web3.eth.coinbase, account3, 10).transact({'from': account2})
    chain.wait.for_receipt(set_txn_hash)

    balance_account1 = erc20_token.functions.balanceOf(web3.eth.coinbase).call()
    balance_account2 = erc20_token.functions.balanceOf(account2).call()
    balance_account3 = erc20_token.functions.balanceOf(account3).call()
    allowance = erc20_token.functions.allowance(web3.eth.coinbase, account2).call()

    assert balance_account1 == 999990
    assert balance_account2 == 0
    assert balance_account3 == 10
    assert allowance == 90
