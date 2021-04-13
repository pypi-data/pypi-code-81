from setuptools import setup, find_packages

ld="""# Example
```python
from univoucher import models, local
from getpass import getpass
import math

netloc = input("Netloc: ") # <host>:<port>
username = input("Username: ")
password = getpass("Password: ")

client:models.Client = local.Client(netloc, username, password)
client.verify = False

# Create one voucher
# A guest can use it for 1000 minutes when redeemed
# The voucher can be redeemed an unlimited amount of times
vouchers = client.fetch(amount=1, duration=1000, uses=math.inf)

unlimited_uses_voucher:models.Voucher = next(vouchers)

print(unlimited_uses_voucher.code)
```"""

setup(
    name="univoucher",
    packages=find_packages(),
    version="2.0.1",
    description="Programmatically create UniFi Guest vouchers",
    long_description=ld,
    long_description_content_type="text/markdown",
    author="Perzan",
    author_email="PerzanDevelopment@gmail.com",
    url="https://github.com/Perzan/univoucher",
    install_requires=[
        "requests>=2.25,<3.0"
    ]
)
