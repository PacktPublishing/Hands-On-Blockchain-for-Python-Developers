import ipfsapi


c = ipfsapi.connect()
peer_id = c.key_list()['Keys'][0]['Id']

c.name_publish('Qme1FUeEhA1myqQ8C1sCSXo4dDJzZApGD6StE26S72ZqyU')

result = c.cat('/ipns/' + peer_id)
print(result)
