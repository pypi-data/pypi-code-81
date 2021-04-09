from setuptools import setup
import pypandoc


def get_version(path):
    with open(path, "r") as fp:
        lines = fp.read()
    for line in lines.split("\n"):
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(name='pad-sequences',
      version=get_version("pad_sequences/__init__.py"),
      description='pad variable length sequences with multiples features',
      long_description=pypandoc.convert('README.md', 'rst'),
      url='http://github.com/ulf1/pad-sequences-multi',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['pad_sequences'],
      install_requires=[
          'setuptools>=40.0.0'],
      python_requires='>=3.6',
      zip_safe=True)
