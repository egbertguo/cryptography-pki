# _*_ coding=utf-8 _*_
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


with open("rsa_private_key.pem", "rb") as key_file:
     private_key = serialization.load_pem_private_key(
         key_file.read(),
         password='mypassword',
         backend=default_backend()
     )

'''
# encryption private key
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
 )
print  pem

# noEncryption key
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
 )
print pem
'''

with open('data.txt', 'r') as f:
    ciphertext = f.read()

plaintext = private_key.decrypt(
     ciphertext,
     padding.OAEP(
         mgf=padding.MGF1(algorithm=hashes.SHA256()),
         algorithm=hashes.SHA256(),
         label=None
     )
 )

print plaintext
