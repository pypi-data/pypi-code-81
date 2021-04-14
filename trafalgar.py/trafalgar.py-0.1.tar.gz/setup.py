from setuptools import setup

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='trafalgar.py',
    version='0.1',
    description='Trafalgar makes quantitative finance and portfolio analysis faster and easier',
    py_modules=['trafalgar'],
    package_dir={'':'src'},
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url='https://github.com/ssantoshp/trafalgar',
    author = "Santosh Passoubady",
    author_email = "santoshpassoubady@gmail.com",
    license='MIT',
    install_requires=[
          'numpy',
          'matplotlib',
          'pykalman',
          'seaborn',
          'scipy',
          'pandas_datareader',
          'datetime',
          'statsmodels',
          'sklearn'
      ],
)
