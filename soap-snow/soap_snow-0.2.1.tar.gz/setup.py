from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="soap_snow",
    version="0.2.1",
    author="Ezequiel M. Iglesias",
    author_email="ezequiel.m.iglesias@gmail.com",
    description="Python client for interacting with the ServiceNow SOAP web service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xthehatterx/soap_snow",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
        'requests',
    ]
)