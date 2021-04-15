from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()
    # allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
setup(
    name='RSTLib',
    version='0.0.12',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='RSTLib module',
    long_description=README,
    author='Prasad,Shikhar,Sumedh',
    author_email=' deepakmd17.extc@coep.ac.in, manojbm17.extc@coep.ac.in, sumedhms17.extc@coep.ac.in',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['pandas']
)