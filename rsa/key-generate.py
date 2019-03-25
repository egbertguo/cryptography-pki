# _*_ coding=utf-8 _*_
'''https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/?highlight=public_key'''

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import datetime

# private key
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
print dir(private_key)
with open('rsa_private_key.pem', 'wb') as f:
    f.write(private_key.private_bytes(encoding=serialization.Encoding.PEM, \
   					format=serialization.PrivateFormat.TraditionalOpenSSL,\
					encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword'),))

# public key
public_key = private_key.public_key()
with open('rsa_public_key.pem', 'wb',) as f:
    f.write(public_key.public_bytes(\
	 	encoding=serialization.Encoding.PEM,\
    		format=serialization.PublicFormat.SubjectPublicKeyInfo))

# csr key, used to apply for the certificate
'''
Information about our public key (including a signature of the entire body).
Information about who we are.
Information about what domains this certificate is for.
'''
csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([\
                        x509.NameAttribute(NameOID.COUNTRY_NAME, u'CH'),\
                        x509.NameAttribute(NameOID.LOCALITY_NAME, u'SHENZHEN'),\
                        x509.NameAttribute(NameOID.COMMON_NAME, u'CAOBAOGUO'),\
                        ])).add_extension(\
                                x509.SubjectAlternativeName([\
                                        x509.DNSName(u'caobaoguo.com'),\
                                        x509.DNSName(u'baicells.com'),\
                                        ]),\
                                        critical=False,).sign(private_key, hashes.SHA256(), default_backend())
with open('rsa_csr.pem', 'wb') as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))

# certificate
one_day = datetime.timedelta(1, 0, 0)
public_key = private_key.public_key()
builder = x509.CertificateBuilder()
builder = builder.subject_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u'cryptography.io'),
]))
builder = builder.issuer_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u'cryptography.io'),
]))
builder = builder.not_valid_before(datetime.datetime.today() - one_day)
builder = builder.not_valid_after(datetime.datetime.today() + (one_day * 30))
builder = builder.serial_number(x509.random_serial_number())
builder = builder.public_key(public_key)
builder = builder.add_extension(
    x509.SubjectAlternativeName(
        [x509.DNSName(u'cryptography.io')]
    ),
    critical=False
)
builder = builder.add_extension(
    x509.BasicConstraints(ca=False, path_length=None), critical=True,
)
certificate = builder.sign(
    private_key=private_key, algorithm=hashes.SHA256(),
    backend=default_backend()
)

with open("certificate.pem", "wb") as f:
	f.write(certificate.public_bytes(serialization.Encoding.PEM))

