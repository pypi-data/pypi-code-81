from setuptools import setup, find_packages
from distutils.core import setup, Extension

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='skyway',
    version='0.0.2',
    description='Use Your Imagination',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Yigido',
    author_email='yigitgulay11@outlook.com',
    license='MIT',
    classifiers=classifiers,
    keywords='skyway',
    packages=find_packages(),
    install_requires=['']
)
