from setuptools import setup

with open("lin_alg_djl/README.md", "r") as fh:
    long_description = fh.read()

setup(name='lin_alg_djl',
      version='0.1',
      description='Linear Algebra Tools from Udacity',
      long_description=long_description,
      packages=['lin_alg_djl'],
      author='Derrick Lewis',
      zip_safe=False)
