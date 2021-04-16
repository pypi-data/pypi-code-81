import setuptools


setuptools.setup(
    name='bmaquet-tap-pagerduty',
    version='1.0.1',
    url='https://github.com/BenjMaq/bmaquet-tap-pagerduty',
    description='Singer.io tap for extracting data from Pagerduty v2 API',
    long_description='',
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Topic :: Software Development',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords="singer tap python pagerduty",
    license='GPLv3',
    packages=setuptools.find_packages(exclude=['tests']),
    package_data={
        'tap_pagerduty': ['schemas/*.json']
    },
    install_requires=[
        'requests==2.22.0',
        'singer-python==5.7.0'
    ],
    extras_require={
        'dev': [
            'pylint',
            'ipdb'
        ]
    },
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['tap-pagerduty = tap_pagerduty:main']
    }
)
