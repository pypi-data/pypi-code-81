from setuptools import setup
import sys

is_py_3 = sys.version_info[0] == 3

setup(
    name='aalam-common',
    license="MIT",
    version="0.1.53",
    author="Babu Shanmugam",
    author_email="babu@aalam.io",
    description="Aalam Common module",
    platforms='any',
    keywords=['aalam', 'web framework'],
    packages=['aalam_common'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
    entry_points={
        'console_scripts': [
            'app_launcher_python=aalam_common.main:main'
        ]
    },
    install_requires=['requests==2.11.1',
                      'eventlet==0.21.0' if is_py_3 else 'eventlet==0.20.1',
                      'PasteDeploy', 'webob', 'python-dateutil',
                      'PyYAML==3.11', 'Routes==2.2.0', 'pycrypto',
                      'sqlalchemy', 'mysqlclient', 'redis==2.10.6',
                      'htmlmin==0.1.6', 'Paste', 'PasteDeploy', 'ecdsa',
                      'pystache', 'requests-unixsocket'],
)
