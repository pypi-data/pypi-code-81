import setuptools

setuptools.setup(
    name='singular_report_builder',
    version='0.0.10',
    author='Singular Sistemas',
    author_email='ivan@singular.inf.br',
    description='Report builder',
    long_description='Report builder',
    url='https://lucas@bitbucket.org/singular-dev/singular_report_builder.git',
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[
        'django',
        'weasyprint'
    ]
)
