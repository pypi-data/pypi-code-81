import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='pymom',
      version='1.0.0',
      description='Kafka framework for Python.',
      long_description=README,
      long_description_content_type="text/markdown",
      url='https://github.com/patrickmay/pymom/src/master/',
      author='Patrick May',
      author_email="patrick.may@mac.com",
      license="Apache 2.0",
      packages=['pymom'],
      include_package_data=True,
      install_requires=['pykafka'])
