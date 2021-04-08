from distutils.core import setup
import setuptools

setup(
    name='mesa-solutions-utils',
    packages=['MesaSoapManager', 'ODCHelperFunctions'],
    version='1.0.7',
    license='MIT',
    description='Various utilities functions and classes',
    author='Mesa Natural Gas Solutions, LLC',
    author_email='support@mesangs.com',
    url='https://dev.azure.com/mesa-ngs/_git/mesa-solutions-utils',
    download_url='https://dev.azure.com/mesa-ngs/_git/mesa-solutions-utils',
    keywords=['Microsoft Dynamics NAV', 'SOAP'],
    install_requires=[
        'zeep <= 3.4.0',
    ]
)
