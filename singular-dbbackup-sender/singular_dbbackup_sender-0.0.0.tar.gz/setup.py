import setuptools

setuptools.setup(
    name='singular_dbbackup_sender',
    version='0.0.0',
    author='Singular Sistemas',
    author_email='ivan@singular.inf.br',
    description='Server updater',
    long_description='Server updater',
    url='https://lucas@bitbucket.org/singular-dev/dbbackup_sender.git',
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        'django',
        'django-crontab',
        'dbbackup'
    ]
)
