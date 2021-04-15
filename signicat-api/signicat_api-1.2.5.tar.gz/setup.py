from distutils.core import setup

setup(
    name='signicat_api',
    packages=['signicat_api'],
    version='1.2.5',
    description='Rabobank Signicat API wrapper',
    author='Theo Bouwman',
    author_email='theo.bouwman@swishfund.nl',
    package_dir={'': 'src'},
    install_requires=[
        'requests==2.21.0'
    ],
)