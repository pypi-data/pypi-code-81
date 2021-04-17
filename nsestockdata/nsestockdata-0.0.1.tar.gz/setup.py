from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'NSE stock data'

# Setting up
setup(
    name="nsestockdata",
    version=VERSION,
    author="Vikram Ahuja",
    author_email="<vikramahuja1313@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['bs4', 'pandas', 'requests'],
    keywords=['python', 'NSE', 'stock','finance', 'data'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
