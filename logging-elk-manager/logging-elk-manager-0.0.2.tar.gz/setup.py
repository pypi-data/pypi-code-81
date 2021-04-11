from setuptools import setup, find_packages

VERSION = '0.0.2'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="logging-elk-manager",
    version=VERSION,
    author="Marco Aleixo",
    author_email="marco.aleixo@misterturing.com",
    description="Facilitate the insertion of logs in our ELK.",
    long_description="Facilitate the insertion of logs in our ELK using this package as a handler for the standard python logging library as a base.",
    packages=find_packages(),
    install_requires=["requests==2.25.1", "pytz==2020.5"],  # add any additional packages that
    keywords=['logging', 'python', 'elk', 'elasticsearch'],
    classifiers=[
        "Development Status :: 3 - Alpha",
    ]
)
