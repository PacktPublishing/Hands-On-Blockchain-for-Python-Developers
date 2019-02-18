import ipfsapi


c = ipfsapi.connect()
c.pubsub_pub('bitcoin', 'To the moon!')
