from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='nlpa',
    version='0.1.0',
    description='A very basic nlp automation',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/nerds-coding/nlpa',
    author='Anup Prakash',
    author_email='2000.anupprakash@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='nlp automation',
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'nltk', 'contractions','emoji'],
    python_requires='>=3',
)
