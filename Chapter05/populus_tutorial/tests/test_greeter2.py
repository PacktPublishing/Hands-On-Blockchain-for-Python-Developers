import pytest

@pytest.fixture()
def greeter2_contract(chain):
    Greeter2Factory = chain.provider.get_contract_factory('Greeter2')
    deploy_txn_hash = Greeter2Factory.constructor(b'Hola').transact()
    contract_address = chain.wait.for_contract_address(deploy_txn_hash)
    return Greeter2Factory(address=contract_address)

def test_greeter2(greeter2_contract):
    greeting2 = greeter2_contract.functions.greet().call()
    assert greeting2 == b'Hola'
