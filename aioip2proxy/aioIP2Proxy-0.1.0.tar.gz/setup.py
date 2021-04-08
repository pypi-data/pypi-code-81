import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as rq:
    requirements = [r.strip() for r in rq.readlines()]

setuptools.setup(
    name="aioIP2Proxy",
    version="0.1.0",
    author="sunset-developer",
    author_email="aidanstewart@sunsetdeveloper.com",
    description="Python API for IP2Proxy database. It can be used to query an IP address if it was being used as open proxy, web proxy, VPN anonymizer and TOR exits.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['IP2Proxy'],
    url="https://github.com/ip2location/ip2proxy-python",
    packages=setuptools.find_packages(),
    tests_require=['pytest>=3.0.6', 'pytest-asyncio==0.14.0'],
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    requirements=requirements
)
