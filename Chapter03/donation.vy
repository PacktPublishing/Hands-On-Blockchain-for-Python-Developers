struct DonaturDetail:
    sum: uint256(wei)
    name: bytes[100]
    time: timestamp

donatur_details: public(map(address, DonaturDetail))

donaturs: public(address[10])

donatee: public(address)

index: int128

@public
def __init__():
    self.donatee = msg.sender

@payable
@public
def donate(name: bytes[100]):
    assert msg.value >= as_wei_value(1, "ether")
    assert self.index < 10

    self.donatur_details[msg.sender] = DonaturDetail({
                                         sum: msg.value,
                                         name: name,
                                         time: block.timestamp
                                       })

    self.donaturs[self.index] = msg.sender
    self.index += 1

@public
def withdraw_donation():
    assert msg.sender == self.donatee

    send(self.donatee, self.balance)
