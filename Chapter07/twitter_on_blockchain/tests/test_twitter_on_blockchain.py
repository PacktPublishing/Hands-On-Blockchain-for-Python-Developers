import pytest
import eth_tester


def test_initial_condition(web3, chain):
    twitter_on_blockchain, _ = chain.provider.get_or_deploy_contract('TwitterOnBlockchain')

    assert twitter_on_blockchain.functions.tweets__index(web3.eth.coinbase).call() == 0

def test_write_a_tweet(web3, chain):
    twitter_on_blockchain, _ = chain.provider.get_or_deploy_contract('TwitterOnBlockchain')

    tweet = b'My first tweet ever!'
    set_txn_hash = twitter_on_blockchain.functions.write_a_tweet(tweet).transact()
    chain.wait.for_receipt(set_txn_hash)
    assert twitter_on_blockchain.functions.tweets__index(web3.eth.coinbase).call() == 1
    assert twitter_on_blockchain.functions.tweets__messages(web3.eth.coinbase,0).call()[:len(tweet)] == tweet

    tweet2 = b'I feel sad today.'
    set_txn_hash = twitter_on_blockchain.functions.write_a_tweet(tweet2).transact()
    chain.wait.for_receipt(set_txn_hash)
    assert twitter_on_blockchain.functions.tweets__index(web3.eth.coinbase).call() == 2
    assert twitter_on_blockchain.functions.tweets__messages(web3.eth.coinbase,0).call()[:len(tweet)] == tweet
    assert twitter_on_blockchain.functions.tweets__messages(web3.eth.coinbase,1).call()[:len(tweet2)] == tweet2
