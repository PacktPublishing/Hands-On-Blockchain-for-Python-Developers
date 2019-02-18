import hashlib

payload_string = '{"history": "Sky loves turtle", "parent_id": 3, "id": 4}'
payload_bytes = bytes(payload_string, 'utf-8')
for i in range(1000000):
    nonce = str(i).encode('utf-8')
    result = hashlib.sha256(payload_bytes + nonce).hexdigest()
    if result[0:5] == '00000':
        print("The answer to puzzle: " + str(i))
        print("Input to hash is: " + payload_string + str(i))
        print("Output hash which has 5 leading zeros: " + result)
        break

