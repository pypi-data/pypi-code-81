import setuptools

setuptools.setup(
    name='singular_server_management',
    version='0.0.11',
    author='Singular Sistemas',
    author_email='ivan@singular.inf.br',
    description='Server management',
    long_description='Server management',
    url='https://lucas@bitbucket.org/singular-dev/singular_server_management.git',
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[
        'django',
        'fabric',
        'invoke',
        'django-crontab',
    ]
)
