import setuptools

from beancountswedbank import VERSION


with open('LICENSE', encoding='utf-8') as fd:
    licensetext = fd.read()


setuptools.setup(name='beancountswedbank',
      version=VERSION,
      description="CSV importer script from Swedbank online banking for beancount",
      url="https://github.com/vonshednob/beancount-swedbank-importer",
      author="R",
      author_email="devel+beancount-swedbank-this-is-spam@kakaomilchkuh.de",
      license=licensetext,
      py_modules=['beancountswedbank'],
      data_files=[],
      requires=['beancount'],
      python_requires='>=3.5',
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3',
                   ])
