from setuptools import setup

setup(name='index_of_refraction',
      version='1.0',
      description='A package to generate the index of refraction from Vector Network Analyzer data or densities.',
      url='http://github.com/phys201/index_of_refraction',
      author='spacemir',
      author_email='miranda.eiben@cfa.harvard.edu',
      license='GPLv3',
      packages=['index_of_refraction'],
      install_requires=['numpy', 'matplotlib'])
