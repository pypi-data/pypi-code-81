from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='asterism',
      version='0.7',
      description='Helpers for Project Electron infrastructure',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/RockefellerArchiveCenter/asterism',
      author='Rockefeller Archive Center',
      author_email='archive@rockarch.org',
      install_requires=[
          'bagit',
          'django',
          'djangorestframework',
          'psycopg2-binary',
          'odin'],
      license='MIT',
      packages=find_packages(),
      test_suite='nose.collector',
      tests_require=[
          'bagit',
          'django',
          'djangorestframework',
          'psycopg2-binary',
          'nose',
          'odin'],
      zip_safe=False)
