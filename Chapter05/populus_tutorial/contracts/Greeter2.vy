greeting: bytes[20]


@public
def __init__(greeting_param: bytes[20]):
    self.greeting = greeting_param


@public
def setGreeting(x: bytes[20]):
    self.greeting = x


@public
def greet() -> bytes[20]:
    return self.greeting
