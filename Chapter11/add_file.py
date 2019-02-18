import ipfsapi


c = ipfsapi.connect()
result = c.add('hello.txt')

print(result)
