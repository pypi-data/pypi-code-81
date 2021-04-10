from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='metaunit',
    version='0.0.6',
    description='Metaunit is python package for unit conversion.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Bathiya Seneviratne',
    author_email='seneviratne.bathiya@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keyword='conversion units area metric length volume weight liquid',
    packages=find_packages(),
    install_requires=[]
)