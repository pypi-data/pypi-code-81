# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
from setuptools import setup

version='0.0.4'

setup(
    name='dnull',
    version='{}'.format(version),
    description='UES Lib python helpers',
    license='MIT',
    packages=['dnull'],
    author='Bohdan Sukhomlinov',
    author_email='shellshock.dnull@gmail.com',
    keywords=['google', 'calendar', 'ues'],
    url='https://gitlab.com/ues/lib/python/dnull',
    download_url = 'https://gitlab.com/ues/lib/python/dnull/-/archive/{}/dnull-{}.tar.gz'.format(version, version),
    install_requires=[
        'google-api-core',
        'google-api-python-client',
        'google-auth',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'googleapis-common-protos',
        'PyYAML'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

