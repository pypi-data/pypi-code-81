from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3'
]

setup(
    name='unofficialmailpoof',
    version='0.0.1',
    description='unofficial mailpoof module',
    long_description=open('README.md').read(),
    url='https://github.com/Retch/unofficial-mailpoof-python',
    author='Retch',
    author_email='retch@mailpoof.com',
    license='GPL-3',
    classifiers=classifiers,
    keywords='mailpoof',
    packages=find_packages(),
    install_requires=['selenium>=3.141.0', 'urllib3>=1.26.4']
)