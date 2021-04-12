"""Installation script for BASEmesh.

This is used to set up the module after installation via PIP, as well
as to build local versions for testing and development.
"""

from setuptools import Extension, find_packages, setup

from basemesh import __version__

# Load the project README
with open('README.md') as readme:
    long_description = readme.read()

# Define the algorithm acceleration module
algorithms_c = Extension(name='basemesh.algorithms.algorithms_c',
                         sources=['src/algorithms_c.c'],
                         optional=True)

# Non-Python files to include
package_data = {
    'basemesh': ['metadata.txt', 'packages/**'],
    'basemesh.plugin': ['resources.qrc', 'icons/**'],
    'basemesh.plugin.gui': ['templates/**'],
    'basemesh.triangle': ['bin/**']
}

setup(name='BASEmesh',
      version=__version__,
      description='Pre-processing and mesh generation toolkit for BASEMENT.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='ETH Zürich',
      maintainer_email='seidelmann@vaw.ethz.ch',
      url='https://git.ee.ethz.ch/basemesh/basemesh-v2/',
      license='GNU General Public License v3 (GPLv3)',
      packages=find_packages(),
      package_data=package_data,
      ext_modules=[
          algorithms_c
      ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.7',
          'Typing :: Typed'
      ],
      install_requires=[
          'numpy'
      ],
      scripts=['scripts/basechange.py'])
