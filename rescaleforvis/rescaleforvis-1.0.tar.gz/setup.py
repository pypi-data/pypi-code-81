
from setuptools import setup


setup(name='rescaleforvis',
      version='1.0',
      description='Maps each number of a short list to a whole number, such that the order of the magnitudes of the differences between any two numbers is preserved.',
      url='https://github.com/garryFromGermany/rescale_for_vis',
      author='Garrett May',
      author_email='garrettmay@live.de',
      license='MIT',
      install_requires=['numpy'],
      packages=['rescaleforvis'],
      zip_safe=False)
