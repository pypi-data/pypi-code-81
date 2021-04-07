from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'API for Kafka Python'

setup(
    name="KafkaUnity",
    version=VERSION,
    author="Jake Fogden",
    author_email="jake.fogden@vodafone.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['kafka-python'],
    keywords=['Kafka', 'Python', 'Unity'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)