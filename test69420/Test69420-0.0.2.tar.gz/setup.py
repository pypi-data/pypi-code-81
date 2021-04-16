from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Test Package for PyPi'
LONG_DESCRIPTION = 'Test Package for PyPi Long Desc'

# Setting up
setup(
    name="Test69420",
    version=VERSION,
    author="Incognito Under",
    author_email="<test@test.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'Test69420'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)