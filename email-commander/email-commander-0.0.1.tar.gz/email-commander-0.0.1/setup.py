from setuptools import setup, find_packages

requirements = [
    'fileperms',
    'structlog>=21.1.0',
    'toml',
]


with open('README.md') as f:
    readme = f.read()

setup(
    name='email-commander',
    version='0.0.1',
    description='Email Commander allows you to manage any host just by sending emails.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/msztolcman/email-commander',
    project_urls={
        'GitHub: issues': 'https://github.com/msztolcman/email-commander/issues',
        'GitHub: repo': 'https://github.com/msztolcman/email-commander',
    },
    download_url='https://github.com/msztolcman/email-commander',
    author='Marcin Sztolcman',
    author_email='marcin@urzenia.net',
    license='MIT',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'email-commander = email_commander.cli:main',
            'ec = email_commander.cli:main',
        ],
    },
    install_requires=requirements,
    # see: https://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Communications :: Email',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
        'Topic :: Utilities',
        'Framework :: AsyncIO',
    ]
)
