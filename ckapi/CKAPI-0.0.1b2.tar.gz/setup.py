from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='CKAPI',
    version='0.0.1b2',
    description='ChokChaisak',
    long_description=readme(),
    url='https://github.com/ChokChaisak/ChokChaisak',
    author='ChokChaisak',
    author_email='ChokChaisak@gmail.com',
    license='ChokChaisak',
    install_requires=[
        'matplotlib',
        'numpy',
        'requests>=2.25.1',
    ],
    keywords='CKAPI',
    packages=['CKAPI'],
    package_dir={
    'CKAPI': 'src/CKAPI',
    },
    package_data={
    'CKAPI': ['*'],
    },
)