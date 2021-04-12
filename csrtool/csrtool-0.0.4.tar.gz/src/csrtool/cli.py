import argparse
import time
from pathlib import Path

from . import csrutils
from cryptography.hazmat.primitives import serialization

default_path = Path.home() / "csr"

def gencsr():
    """
    CLI-command `csr` to generate CSR with DNS-names
    """
    parser = argparse.ArgumentParser(description='Generate CSRs')
    parser.add_argument('names', metavar='FQDN', type=str, nargs='+', help='DNS-names for CSR (first will be used for CN)')
    parser.add_argument('--ou', type=str, default="IT", help="Organizational Unit (default: IT)")
    parser.add_argument('--country', type=str, default='NO', help='Two-letter country-code (default: NO)')
    parser.add_argument('--org', type=str, required=True, help='Organization Name')
    parser.add_argument('-w', metavar='PATH', dest='path', type=str, default=default_path, help=f'Output directory (default: {default_path})')
    args = parser.parse_args()

    # sanity checks
    output_dir = Path(args.path)
    output_dir.mkdir(mode=750, exist_ok=True)
    output_dir.chmod(mode=750)

    key = csrutils.generate_private_key()
    csr = csrutils.generate_csr(org=args.org, ou=args.ou, c=args.country,
                            dns_names=args.names, private_key=key)

    # name
    base_name = f'{args.names[0]}-{int(time.time())}'

    # write key
    with open(output_dir / f'{base_name}.key', 'wb') as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print(f'Wrote key: {output_dir / base_name}.key')

    # write csr
    with open(output_dir / f'{base_name}.csr', 'wb') as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))
    print(f'Wrote csr: {output_dir / base_name}.csr')
