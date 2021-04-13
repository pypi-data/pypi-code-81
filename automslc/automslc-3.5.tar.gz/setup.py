import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='automslc',
    version='3.5',
    scripts=['automslc'] ,
    author="Thanh Hoa",
    author_email="getmoneykhmt3@gmail.com",
    description="A Des of AutoMSLC",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vtandroid/dokr",
    packages=setuptools.find_packages(),
    py_modules=['dzee_helper'],
    install_requires=[
        'requests', 'click', 'pycrypto'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )