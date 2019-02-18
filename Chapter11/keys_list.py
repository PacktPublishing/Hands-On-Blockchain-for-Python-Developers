import ipfsapi


c = ipfsapi.connect()
print(c.key_list())
