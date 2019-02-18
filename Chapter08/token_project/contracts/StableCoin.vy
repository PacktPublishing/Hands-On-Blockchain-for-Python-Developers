Transfer: event({_from: indexed(address), _to: indexed(address), _value: uint256})
Approval: event({_owner: indexed(address), _spender: indexed(address), _value: uint256})
Freeze: event({_account: indexed(address), _freeze: bool})

name: public(bytes[10])
symbol: public(bytes[3])
totalSupply: public(uint256)
decimals: public(uint256)
balances: map(address, uint256)
allowed: map(address, map(address, uint256))
frozenBalances: public(map(address, bool))
owner: public(address)

@public
def __init__():
    _initialSupply: uint256 = 1000
    _decimals: uint256 = 3
    self.totalSupply = _initialSupply * 10 ** _decimals
    self.balances[msg.sender] = self.totalSupply
    self.name = 'Haha Coin'
    self.symbol = 'HAH'
    self.decimals = _decimals
    self.owner = msg.sender
    log.Transfer(ZERO_ADDRESS, msg.sender, self.totalSupply)

@public
def freezeBalance(_target: address, _freeze: bool) -> bool:
    assert msg.sender == self.owner
    self.frozenBalances[_target] = _freeze
    log.Freeze(_target, _freeze)

    return True

@public
def mintToken(_mintedAmount: uint256) -> bool:
    assert msg.sender == self.owner
    self.totalSupply += _mintedAmount
    self.balances[msg.sender] += _mintedAmount
    log.Transfer(ZERO_ADDRESS, msg.sender, _mintedAmount)

    return True

@public
def burn(_burntAmount: uint256) -> bool:
    assert msg.sender == self.owner
    assert self.balances[msg.sender] >= _burntAmount
    self.totalSupply -= _burntAmount
    self.balances[msg.sender] -= _burntAmount
    log.Transfer(msg.sender, ZERO_ADDRESS, _burntAmount)

    return True

@public
@constant
def balanceOf(_owner: address) -> uint256:
    return self.balances[_owner]

@public
def transfer(_to: address, _amount: uint256) -> bool:
    assert self.balances[msg.sender] >= _amount
    assert self.frozenBalances[msg.sender] == False
    self.balances[msg.sender] -= _amount
    self.balances[_to] += _amount
    log.Transfer(msg.sender, _to, _amount)

    return True

@public
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    assert _value <= self.allowed[_from][msg.sender]
    assert _value <= self.balances[_from]
    assert self.frozenBalances[msg.sender] == False

    self.balances[_from] -= _value
    self.allowed[_from][msg.sender] -= _value
    self.balances[_to] += _value
    log.Transfer(_from, _to, _value)

    return True

@public
def approve(_spender: address, _amount: uint256) -> bool:
    self.allowed[msg.sender][_spender] = _amount
    log.Approval(msg.sender, _spender, _amount)

    return True

@public
@constant
def allowance(_owner: address, _spender: address) -> uint256:
    return self.allowed[_owner][_spender]
