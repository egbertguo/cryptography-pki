# _*_ coding=utf-8 _*_
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate, ocsp 
 
# 公匙导入
with open('rsa_public_key.pem', 'rb') as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )
 
 
message = b'test data'
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
 
with open('data.txt', 'wb') as f:
    f.write(ciphertext)


#----------------------------------
# encryption with certificate

with open('certificate.pem', 'r') as f:
    cert = load_pem_x509_certificate(f.read(), default_backend())

print dir(cert)
print cert.issuer
public_key = cert.public_key()

message = b'me'
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print ciphertext
print len(ciphertext)
with open('data.txt', 'wb') as f:
    f.write(ciphertext)

