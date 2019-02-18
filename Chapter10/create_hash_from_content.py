from os import listdir
from hashlib import sha256


files = [f for f in listdir('.') if 'hello' in f]

hashes = {}

for file in files:
    with open(file) as f:
        content = f.read().encode('utf-8')
        hash_of_content = sha256(content).hexdigest()
        hashes[hash_of_content] = content

content = hashes['20c38a7a55fc8a8e7f45fde7247a0436d97826c20c5e7f8c978e6d59fa895fd2']
print(content.decode('utf-8'))

print(len(hashes))
