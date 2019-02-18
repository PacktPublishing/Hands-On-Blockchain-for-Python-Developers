Transfer: event({_from: indexed(address), _to: indexed(address), _value: uint256})
Approval: event({_owner: indexed(address), _spender: indexed(address), _value: uint256})
Payment: event({_buyer: indexed(address), _value: uint256(wei)})

name: public(bytes[10])
symbol: public(bytes[3])
totalSupply: public(uint256)
decimals: public(uint256)
balances: map(address, uint256)
ethBalances: public(map(address, uint256(wei)))
allowed: map(address, map(address, uint256))

beneficiary: public(address)
minFundingGoal: public(uint256(wei))
maxFundingGoal: public(uint256(wei))
amountRaised: public(uint256(wei))
deadline: public(timestamp)
price: public(uint256(wei))
fundingGoalReached: public(bool)
crowdsaleClosed: public(bool)

@public
def __init__():
    _initialSupply: uint256 = 100
    _decimals: uint256 = 2
    self.totalSupply = _initialSupply * 10 ** _decimals
    self.name = 'Haha Coin'
    self.symbol = 'HAH'
    self.decimals = _decimals
    self.beneficiary = msg.sender
    self.balances[msg.sender] = self.totalSupply
    self.minFundingGoal = as_wei_value(30, "ether")
    self.maxFundingGoal = as_wei_value(50, "ether")
    self.amountRaised = 0
    self.deadline = block.timestamp + 3600 * 24 * 100 # 100 days
    self.price = as_wei_value(1, "ether") / 100
    self.fundingGoalReached = False
    self.crowdsaleClosed = False

@public
@payable
def __default__():
    assert msg.sender != self.beneficiary
    assert self.crowdsaleClosed == False
    assert self.amountRaised + msg.value < self.maxFundingGoal
    assert msg.value >= as_wei_value(0.01, "ether")
    self.ethBalances[msg.sender] += msg.value
    self.amountRaised += msg.value
    tokenAmount: uint256 = msg.value / self.price
    self.balances[msg.sender] += tokenAmount
    self.balances[self.beneficiary] -= tokenAmount
    log.Payment(msg.sender, msg.value)

@public
def checkGoalReached():
    assert block.timestamp > self.deadline
    if self.amountRaised >= self.minFundingGoal:
        self.fundingGoalReached = True
    self.crowdsaleClosed = True

@public
def safeWithdrawal():
    assert self.crowdsaleClosed == True
    if self.fundingGoalReached == False:
        if msg.sender != self.beneficiary:
            if self.ethBalances[msg.sender] > 0:
                self.ethBalances[msg.sender] = 0
                self.balances[self.beneficiary] += self.balances[msg.sender]
                self.balances[msg.sender] = 0
                send(msg.sender, self.ethBalances[msg.sender])
    if self.fundingGoalReached == True:
        if msg.sender == self.beneficiary:
            if self.balance > 0:
                send(msg.sender, self.balance)

@public
@constant
def balanceOf(_owner: address) -> uint256:
    return self.balances[_owner]

@public
def transfer(_to: address, _amount: uint256) -> bool:
    assert self.crowdsaleClosed == True
    assert self.balances[msg.sender] >= _amount
    self.balances[msg.sender] -= _amount
    self.balances[_to] += _amount
    log.Transfer(msg.sender, _to, _amount)

    return True

@public
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    assert self.crowdsaleClosed == True
    assert _value <= self.allowed[_from][msg.sender]
    assert _value <= self.balances[_from]

    self.balances[_from] -= _value
    self.allowed[_from][msg.sender] -= _value
    self.balances[_to] += _value
    log.Transfer(_from, _to, _value)

    return True

@public
def approve(_spender: address, _amount: uint256) -> bool:
    assert self.crowdsaleClosed == True
    self.allowed[msg.sender][_spender] = _amount
    log.Approval(msg.sender, _spender, _amount)

    return True

@public
@constant
def allowance(_owner: address, _spender: address) -> uint256:
    return self.allowed[_owner][_spender]
