from typing import List

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import AttributeOID, NameOID

# typing hint
StrArr = List[str]

def generate_private_key(key_size=2048, public_exponent=65537) -> rsa.RSAPrivateKey:
    """
        public_exponent should be 65537 for almost everyone, only in some cases 3 for legacy reasons,
        see: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey
    """
    return rsa.generate_private_key( public_exponent, key_size )

def generate_csr(org: str, ou: str, c: str, dns_names: StrArr, private_key) -> x509.CertificateSigningRequest:
    """
    Returns CSR-object based on input. Private key is from method `generate_private_key`
    """
    builder = x509.CertificateSigningRequestBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, dns_names[0]),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, ou),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
        x509.NameAttribute(NameOID.COUNTRY_NAME, c)
    ]))

    # add DNSname(s)
    builder = builder.add_extension(
        x509.SubjectAlternativeName(
            list(map(lambda x: x509.DNSName(x), dns_names))
        ),
        critical=False
    )

    builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True
    )

    # return CSR
    return builder.sign( private_key, hashes.SHA256() )