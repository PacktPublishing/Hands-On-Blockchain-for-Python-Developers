struct DonaturDetail:
    sum: uint256(wei)
    name: bytes[100]
    time: timestamp

contract Hello():
    def say_hello() -> bytes[32]: constant

donatur_details: public(map(address, DonaturDetail))

infinite_array_of_strings: map(uint256, bytes[100])

mapping_of_mapping_of_mapping: map(uint256, map(uint256, map(uint256, bytes[10])))

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

@public
@constant
def donation_smart_contract_call_hello_smart_contract_method(smart_contract_address: address) -> bytes[32]:
    return Hello(smart_contract_address).say_hello()
