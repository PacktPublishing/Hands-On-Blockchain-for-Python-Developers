import pytest
import eth_tester
import time

def test_initialization(web3, chain):
    stable_coin, _ = chain.provider.get_or_deploy_contract('StableCoin')

    token_name = stable_coin.functions.name().call()
    token_symbol = stable_coin.functions.symbol().call()
    decimals = stable_coin.functions.decimals().call()
    total_supply = stable_coin.functions.totalSupply().call()
    owner = stable_coin.functions.owner().call()

    assert token_name == b"Haha Coin"
    assert token_symbol == b"HAH"
    assert decimals == 3
    assert total_supply == 1000000
    assert owner == web3.eth.coinbase

def test_freeze_balance(web3, chain):
    stable_coin, _ = chain.provider.get_or_deploy_contract('StableCoin')

    t = eth_tester.EthereumTester()
    account2 = t.get_accounts()[1]
    account3 = t.get_accounts()[2]

    set_txn_hash = stable_coin.functions.transfer(account2, 10).transact()
    chain.wait.for_receipt(set_txn_hash)

    set_txn_hash = stable_coin.functions.transfer(account3, 1).transact({'from': account2})
    chain.wait.for_receipt(set_txn_hash)

    set_txn_hash = stable_coin.functions.freezeBalance(account2, True).transact()
    chain.wait.for_receipt(set_txn_hash)

    with pytest.raises(eth_tester.exceptions.TransactionFailed):
        stable_coin.functions.transfer(account3, 1).transact({'from': account2})

    set_txn_hash = stable_coin.functions.freezeBalance(account2, False).transact()
    chain.wait.for_receipt(set_txn_hash)

    set_txn_hash = stable_coin.functions.transfer(account3, 1).transact({'from': account2})
    chain.wait.for_receipt(set_txn_hash)

def test_mint_token(web3, chain):
    stable_coin, _ = chain.provider.get_or_deploy_contract('StableCoin')

    set_txn_hash = stable_coin.functions.mintToken(100).transact()
    chain.wait.for_receipt(set_txn_hash)

    new_total_supply = stable_coin.functions.totalSupply().call()
    assert new_total_supply == 1000100

def test_burn_token(web3, chain):
    stable_coin, _ = chain.provider.get_or_deploy_contract('StableCoin')

    set_txn_hash = stable_coin.functions.burn(100).transact()
    chain.wait.for_receipt(set_txn_hash)

    new_total_supply = stable_coin.functions.totalSupply().call()
    assert new_total_supply == 999900
