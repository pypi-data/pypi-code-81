import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='D1scordX',
    version='0.0.9',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='D1scordX AIO Module',
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        'aiohttp',
        'discord',
        'unidecode',
        'numpy',
        'colorama',
        'discord_webhooks'
    ],
    author='хıи"RCΛ#7777',
    author_email='xingodcontact@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)