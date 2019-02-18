import pytest
import eth_tester


def test_donatee(web3, chain):
    donation, _ = chain.provider.get_or_deploy_contract('Donation')

    donatee = donation.functions.donatee().call()
    assert donatee == web3.eth.coinbase

def test_donate_less_than_1_eth(web3, chain):
    donation, _ = chain.provider.get_or_deploy_contract('Donation')

    with pytest.raises(eth_tester.exceptions.TransactionFailed):
        donation.functions.donate(b'Taylor Swift').transact({'value': web3.toWei('0.8', 'ether')})

def test_donate_1_eth(web3, chain):
    import time

    donation, _ = chain.provider.get_or_deploy_contract('Donation')

    t = eth_tester.EthereumTester()
    account2 = t.get_accounts()[1]

    donatur_name = b'Taylor Swift'
    set_txn_hash = donation.functions.donate(donatur_name).transact({'from': account2, 'value': web3.toWei('1', 'ether')})
    chain.wait.for_receipt(set_txn_hash)

    donatur = donation.functions.donaturs(0).call()
    donation_sum = donation.functions.donatur_details__sum(donatur).call()
    donation_name = donation.functions.donatur_details__name(donatur).call()
    donation_time = donation.functions.donatur_details__time(donatur).call()

    assert donatur == account2
    assert donation_sum == web3.toWei('1', 'ether')
    assert donation_name == donatur_name
    assert (int(time.time()) - donation_time) < 600 # could be flaky

    assert web3.eth.getBalance(donation.address) == web3.toWei('1', 'ether')

def test_other_account_could_not_withdraw_money(web3, chain):
    donation, _ = chain.provider.get_or_deploy_contract('Donation')

    t = eth_tester.EthereumTester()
    account2 = t.get_accounts()[1]

    donatur_name = b'Taylor Swift'
    set_txn_hash = donation.functions.donate(donatur_name).transact({'from': account2, 'value': web3.toWei('1', 'ether')})
    chain.wait.for_receipt(set_txn_hash)

    with pytest.raises(eth_tester.exceptions.TransactionFailed):
        donation.functions.withdraw_donation().transact({'from': account2})

def test_manager_account_could_withdraw_money(web3, chain):
    donation, _ = chain.provider.get_or_deploy_contract('Donation')

    t = eth_tester.EthereumTester()
    account2 = t.get_accounts()[1]

    donatur_name = b'Taylor Swift'
    set_txn_hash = donation.functions.donate(donatur_name).transact({'from': account2, 'value': web3.toWei('1', 'ether')})
    chain.wait.for_receipt(set_txn_hash)

    initial_balance = web3.eth.getBalance(web3.eth.coinbase)
    set_txn_hash = donation.functions.withdraw_donation().transact({'from': web3.eth.coinbase})
    chain.wait.for_receipt(set_txn_hash)

    after_withdraw_balance = web3.eth.getBalance(web3.eth.coinbase)

    assert abs((after_withdraw_balance - initial_balance) - web3.toWei('1', 'ether')) < web3.toWei('10', 'gwei')
