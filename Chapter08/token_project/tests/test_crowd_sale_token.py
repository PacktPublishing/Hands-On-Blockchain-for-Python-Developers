import pytest
import eth_tester
import time

def test_initialization(web3, chain):
    crowd_sale_token, _ = chain.provider.get_or_deploy_contract('CrowdSaleToken')

    token_name = crowd_sale_token.functions.name().call()
    token_symbol = crowd_sale_token.functions.symbol().call()
    decimals = crowd_sale_token.functions.decimals().call()
    total_supply = crowd_sale_token.functions.totalSupply().call()
    beneficiary = crowd_sale_token.functions.beneficiary().call()
    minFundingGoal = crowd_sale_token.functions.minFundingGoal().call()
    maxFundingGoal = crowd_sale_token.functions.maxFundingGoal().call()
    amountRaised = crowd_sale_token.functions.amountRaised().call()
    deadline = crowd_sale_token.functions.deadline().call()
    price = crowd_sale_token.functions.price().call()
    fundingGoalReached = crowd_sale_token.functions.fundingGoalReached().call()
    crowdsaleClosed = crowd_sale_token.functions.crowdsaleClosed().call()

    assert token_name == b"Haha Coin"
    assert token_symbol == b"HAH"
    assert decimals == 2
    assert total_supply == 10000
    assert beneficiary == web3.eth.coinbase
    assert minFundingGoal == web3.toWei('30', 'ether')
    assert maxFundingGoal == web3.toWei('50', 'ether')
    assert amountRaised == 0
    assert (deadline - (int(time.time()) +  3600 * 24 * 100)) < 10
    assert price == web3.toWei('0.01', 'ether')
    assert fundingGoalReached == False
    assert crowdsaleClosed == False

def test_purchase_token(web3, chain):
    crowd_sale_token, _ = chain.provider.get_or_deploy_contract('CrowdSaleToken')

    t = eth_tester.EthereumTester()
    account2 = t.get_accounts()[1]
    account3 = t.get_accounts()[2]

    set_txn_hash = crowd_sale_token.functions.__default__().transact({'from': account2, 'value': web3.toWei('1', 'ether')})
    chain.wait.for_receipt(set_txn_hash)

    set_txn_hash = crowd_sale_token.functions.__default__().transact({'from': account3, 'value': web3.toWei('2', 'ether')})
    chain.wait.for_receipt(set_txn_hash)

    ethBalance_account2 = crowd_sale_token.functions.ethBalances(account2).call()
    balance_account2 = crowd_sale_token.functions.balanceOf(account2).call()
    amountRaised = crowd_sale_token.functions.amountRaised().call()
    balance_account1 = crowd_sale_token.functions.balanceOf(web3.eth.coinbase).call()
    assert ethBalance_account2 == web3.toWei('1', 'ether')
    assert balance_account2 == 100
    assert amountRaised == web3.toWei('3', 'ether')
    assert balance_account1 == (10000 - 100 - 200)

def test_close_crowdsale(web3, chain):
    crowd_sale_token, _ = chain.provider.get_or_deploy_contract('CrowdSaleToken')

    crowdsaleClosed = crowd_sale_token.functions.crowdsaleClosed().call()
    assert crowdsaleClosed == False

    with pytest.raises(eth_tester.exceptions.TransactionFailed):
        crowd_sale_token.functions.checkGoalReached().transact()

    # move forward 101 days
    web3.testing.timeTravel(int(time.time()) + 3600 * 24 * 101)
    web3.testing.mine(1)

    set_txn_hash = crowd_sale_token.functions.checkGoalReached().transact()
    chain.wait.for_receipt(set_txn_hash)

    crowdsaleClosed = crowd_sale_token.functions.crowdsaleClosed().call()
    fundingGoalReached = crowd_sale_token.functions.fundingGoalReached().call()
    assert crowdsaleClosed == True
    assert fundingGoalReached == False

def test_refund(web3, chain):
    crowd_sale_token, _ = chain.provider.get_or_deploy_contract('CrowdSaleToken')

    t = eth_tester.EthereumTester()
    account2 = t.get_accounts()[1]

    beforeCrowdsaleEthBalanceAccount2 = web3.eth.getBalance(account2)

    set_txn_hash = crowd_sale_token.functions.__default__().transact({'from': account2, 'value': web3.toWei('5', 'ether')})
    chain.wait.for_receipt(set_txn_hash)

    # move forward 101 days
    web3.testing.timeTravel(int(time.time()) + 3600 * 24 * 101)
    web3.testing.mine(1)

    set_txn_hash = crowd_sale_token.functions.checkGoalReached().transact()
    chain.wait.for_receipt(set_txn_hash)

    ethBalanceAccount2 = crowd_sale_token.functions.ethBalances(account2).call()
    assert ethBalanceAccount2 == web3.toWei('5', 'ether')

    set_txn_hash = crowd_sale_token.functions.safeWithdrawal().transact({'from': account2})
    chain.wait.for_receipt(set_txn_hash)

    afterCrowdsaleEthBalanceAccount2 = web3.eth.getBalance(account2)

    assert abs(beforeCrowdsaleEthBalanceAccount2 - web3.toWei('5', 'ether') - afterCrowdsaleEthBalanceAccount2) < web3.toWei('1', 'gwei')

    ethBalanceAccount2 = crowd_sale_token.functions.ethBalances(account2).call()
    assert ethBalanceAccount2 == 0

def test_withdrawal(web3, chain):
    crowd_sale_token, _ = chain.provider.get_or_deploy_contract('CrowdSaleToken')

    t = eth_tester.EthereumTester()
    account2 = t.get_accounts()[1]

    beforeCrowdsaleEthBalanceAccount2 = web3.eth.getBalance(account2)
    beforeCrowdsaleEthBalanceAccount1 = web3.eth.getBalance(web3.eth.coinbase)

    set_txn_hash = crowd_sale_token.functions.__default__().transact({'from': account2, 'value': web3.toWei('40', 'ether')})
    chain.wait.for_receipt(set_txn_hash)

    # move forward 101 days
    web3.testing.timeTravel(int(time.time()) + 3600 * 24 * 101)
    web3.testing.mine(1)

    set_txn_hash = crowd_sale_token.functions.checkGoalReached().transact()
    chain.wait.for_receipt(set_txn_hash)

    set_txn_hash = crowd_sale_token.functions.safeWithdrawal().transact()
    chain.wait.for_receipt(set_txn_hash)

    afterCrowdsaleEthBalanceAccount2 = web3.eth.getBalance(account2)
    afterCrowdsaleEthBalanceAccount1 = web3.eth.getBalance(web3.eth.coinbase)

    assert abs(beforeCrowdsaleEthBalanceAccount2 - afterCrowdsaleEthBalanceAccount2 - web3.toWei('40', 'ether')) < web3.toWei('1', 'gwei')
    assert abs(afterCrowdsaleEthBalanceAccount1 - beforeCrowdsaleEthBalanceAccount1 - web3.toWei('40', 'ether')) < web3.toWei('1', 'gwei')
