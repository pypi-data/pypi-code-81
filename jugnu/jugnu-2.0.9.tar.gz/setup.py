"""Setup for the jugnu package."""

import setuptools
import os


setuptools.setup(
    author="Ajay Kulal",
    author_email="hackerhero@bugcrowdninja.com",
    name='jugnu',
    license="MIT",
    description='jugnu is a amazing package for data handling',
    version='v2.0.9',
    long_description="no long decsription given",
    url='https://github.com/bountyrecon/',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    dependency_links=['https://github.com/bountyrecon/pydep/releases/tag/0.0.7'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers'
    ],
)
