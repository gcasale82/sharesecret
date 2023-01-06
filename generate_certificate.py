#Generate certificate
from os import environ
from cryptography.hazmat.primitives import serialization , hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime , timedelta

try : hosturl = environ['hosturl']
except : hosturl = '127.0.0.1'
# Generate RSA key
key = rsa.generate_private_key(public_exponent=65537,key_size=2048,)

with open("./certificates/key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))
# Generate a CSR
csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
    # Provide various details about who we are.
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"No Company"),
    x509.NameAttribute(NameOID.COMMON_NAME, hosturl),
])).add_extension(
    x509.SubjectAlternativeName([
        # Describe what sites we want this certificate for.
        x509.DNSName(hosturl),
    ]),
    critical=False,
# Sign the CSR with our private key.
).sign(key, hashes.SHA256())
# Write our CSR out to disk.
with open("./certificates/csr.pem", "wb") as f:
    f.write(csr.public_bytes(serialization.Encoding.PEM))
# Generate certificate
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"No Company"),
    x509.NameAttribute(NameOID.COMMON_NAME, hosturl),
])
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.utcnow()
).not_valid_after(
    # Our certificate will be valid for 1000 days
    datetime.utcnow() + timedelta(days=1000)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName(hosturl)]),
    critical=False,
# Sign our certificate with our private key
).sign(key, hashes.SHA256())
# Write our certificate out to disk.
with open("./certificates/certificate.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))