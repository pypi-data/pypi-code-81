from setuptools import setup


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version(path):
    with open(path, "r") as fp:
        lines = fp.read()
    for line in lines.split("\n"):
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(name='scipy-quadopt',
      version=get_version("scipy_quadopt/__init__.py"),
      description=(
          "Wrapper and utility functions to apply scipy's SLSQP algorithm "
          "to quadratic optimization problems with resource constraints and "
          "upper boundaries."),
      # long_description=read('README.md'),
      # long_description_content_type='text/markdown',
      url='http://github.com/satzbeleg/scipy-quadopt',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='Apache License 2.0',
      packages=['scipy_quadopt'],
      install_requires=[
          'setuptools>=40.0.0',
          'numpy>=1.19.5',
          'scipy>=1.5.0,<2'],
      python_requires='>=3.6',
      zip_safe=True)
