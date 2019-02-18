import ipfsapi


c = ipfsapi.connect()

result = c.add('milada-vigerova-1284157-unsplash.jpg')
print(result)
