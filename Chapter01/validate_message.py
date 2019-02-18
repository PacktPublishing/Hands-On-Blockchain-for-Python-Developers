from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def fetch_public_key(user):
    with open(user.decode('ascii') + "key.pub", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
           key_file.read(),
           backend=default_backend())
    return public_key

# Message coming from user
message = b"Nelson likes cat"

# Signature coming from user
signature = b'7\xe1\xbe\xff\xa8\xe5\'{\xe7\x97w\xfa\x87c\x19\xf0T\xca\xcd\x13\xe0\x80\xa3<\xed\x8b\x1f\x98\x19f\xe4\x00S\xe4\xed \x99Q\x15\x93\xb3\xf1\xe0\\\x03\xbe`\x9ab\xdc+\x9a\xb9\x00\x19\xf4\xe0\xa4a\x17i0HD\xe6~\\\x952\xec5\x18I\xd8k&\x13\xdcY"\xb9o\xa9\xe0\xf2\xa7\x8e\t\xa1PF\xd0\x8a\x10p\xe8\xcd\xc3\xe6f\x93\x9a\xe0\x7f\xbb\xe2\xd6HVM:\xd1\xcfG\xf6\x98gm$\xdf^\xf4\xae\xe4\xd5\xea\xb5\xb4'

user = message.split()[0].lower()
# fetch public key from Nelson
public_key = fetch_public_key(user)
# … verify the message like before
public_key.verify(
    signature,
    message,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256())
