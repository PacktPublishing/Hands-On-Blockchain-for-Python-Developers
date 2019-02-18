import ipfsapi


c = ipfsapi.connect()
peer_id = c.key_list()['Keys'][0]['Id']

c.name_publish('QmYjYGKXqo36GDt6f6qvp9qKAsrc72R9y88mQSLvogu8Ub', key='another_list')

result = c.cat('/ipns/' + peer_id)
print(result)
