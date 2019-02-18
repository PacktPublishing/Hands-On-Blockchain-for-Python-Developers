balances: public(map(address, uint256))


@public
def __init__():
    self.balances[msg.sender] = 10000


@public
def transfer(_to: address, _amount: uint256) -> bool:
    assert self.balances[msg.sender] >= _amount

    self.balances[msg.sender] -= _amount
    self.balances[_to] += _amount

    return True
