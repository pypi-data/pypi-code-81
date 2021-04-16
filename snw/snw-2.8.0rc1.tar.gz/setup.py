from setuptools import setup

setup(
    name='snw',
    version='2.8.0rc1',
    description='snw client tool',
    author='Jean Senellart',
    author_email='jean.senellart@systrangroup.com',
    url='http://www.systransoft.com',
    scripts=['client/snw'],
    package_dir={'client': 'nmt-wizard/client', 'lib': 'client/lib'},
    packages=['client', 'lib', 'lib.commands'],
    install_requires=[
        'configparser',
        'prettytable',
        'requests',
        'six>=1.14.0',
        'setuptools',
        'jsonschema',
        'packaging>=17.0'
    ]
)
