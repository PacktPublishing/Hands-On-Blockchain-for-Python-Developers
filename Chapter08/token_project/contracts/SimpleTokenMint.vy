balances: public(map(address, uint256))
owner: address


@public
def __init__():
    self.balances[msg.sender] = 10000
    self.owner = msg.sender


@public
def transfer(_to: address, _amount: uint256) -> bool:
    assert self.balances[msg.sender] >= _amount

    self.balances[msg.sender] -= _amount
    self.balances[_to] += _amount

    return True

@public
def mint(_new_supply: uint256):
    assert msg.sender == self.owner
    self.balances[msg.sender] = _new_supply
