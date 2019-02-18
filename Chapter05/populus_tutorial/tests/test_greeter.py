def test_greeter(chain):
    greeter, _ = chain.provider.get_or_deploy_contract('Greeter')

    greeting = greeter.functions.greet().call()
    assert greeting == b'Hello'


def test_custom_greeting(chain):
    greeter, _ = chain.provider.get_or_deploy_contract('Greeter')

    set_txn_hash = greeter.functions.setGreeting(b'Guten Tag').transact()
    chain.wait.for_receipt(set_txn_hash)

    greeting = greeter.functions.greet().call()
    assert greeting == b'Guten Tag'
