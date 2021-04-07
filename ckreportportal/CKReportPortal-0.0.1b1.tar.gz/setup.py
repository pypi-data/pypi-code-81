from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='CKReportPortal',
    version='0.0.1b1',
    description='ChokChaisak',
    long_description=readme(),
    url='https://github.com/ChokChaisak/ChokChaisak',
    author='ChokChaisak',
    author_email='ChokChaisak@gmail.com',
    license='ChokChaisak',
    install_requires=[
        'matplotlib',
        'numpy',
        'reportportal-client>=5.0.9',
    ],
    keywords='CKReportPortal',
    packages=['CKReportPortal'],
    package_dir={
    'CKReportPortal': 'src/CKReportPortal',
    },
    package_data={
    'CKReportPortal': ['*'],
    },
)