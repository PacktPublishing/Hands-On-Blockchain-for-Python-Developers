import ipfsapi


c = ipfsapi.connect()
print(c.key_list())

c.key_gen('another_key', 'rsa')

print(c.key_list())
