# cryptography-pki

1, use the key-generate.py to generate the private_key and the public_key and the self-signed certificate
2, the encryption-test.py encrypt the message
3, the decryption-test.py decrypt the message(using public or use the certificate)

steps:
actually, we can apply for the certificate from the third part using the csr.pm 
after the third part confirm the applicant's infomation, they release the certificate,
a. our users can get the certificate, and verify it is trusty.
b. the users get the public_key from the certificate 
c. encrypt the message with the public_key.
d. send the ciphertext throught the http(others can't decrypt the ciphertext because they dont have the private_key).
e. the server receive the ciphertext and decrypt it with the private_key.

the only problem is that: others can get the server's message because it is encrypted using the public_key
