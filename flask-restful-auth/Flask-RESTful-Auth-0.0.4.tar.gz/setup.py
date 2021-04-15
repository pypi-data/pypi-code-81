
import sys
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

__title__       = 'Flask-RESTful-Auth'
__description__ = 'Customizable RESTful Authentication & User Management: Register, Confirm, Login, Change username/password, Forgot password and more.'
__version__     = '0.0.4'
__url__         = 'https://github.com/mcqueen256/Flask-RESTful-Auth'
__author__      = ['Nicholas Buckeridge', 'Sarah Heading', 'Prateek Kr. Gupta', 'Prarthana Jayanna']
__author_email__= 'bucknich@gmail.com'
__maintainer__  = 'Nicholas Buckeridge'
__license__     = 'MIT'
__copyright__   = '(c) 2021 The Flask-RESTful-Auth Team'

setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=README,
    long_description_content_type="text/markdown",
    keywords='Flask User Authorization Account Management Registration Username Email Confirmation Forgot Reset Password Invitation',
    url=__url__,
    author=__author__,
    author_email=__author_email__,
    license=__license__,

    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Security',
    ],

    packages=['flask_restful_auth'],
    include_package_data=True,    # Tells setup to use MANIFEST.in
    zip_safe=False,    # Do not zip as it will make debugging harder

    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',   # Python 3.6+
    # setup_requires=['Flask-Login',] + pytest_runner,
    install_requires=[],
    #     'bcrypt>=2.0',
    #     'cryptography>=1.6',
    #     'Flask>=0.9',
    #     'Flask-Login>=0.2',
    #     'Flask-Mail>=0.9',
    #     'Flask-SQLAlchemy>=1.0',
    #     'Flask-WTF>=0.9',
    #     'passlib>=1.7',
    # ],
    # tests_require=['pytest'],
    entry_points={
        "console_scripts": [
            "flask-restful-auth-example=flask_restful_auth.__main__:main",
        ]
    },

)