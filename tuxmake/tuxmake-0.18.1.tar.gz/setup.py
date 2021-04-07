#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['tuxmake']

package_data = \
{'': ['*'],
 'tuxmake': ['arch/*',
             'metadata/*',
             'runtime/*',
             'target/*',
             'toolchain/*',
             'wrapper/*']}

entry_points = \
{'console_scripts': ['tuxmake = tuxmake.cli:main']}

setup(name='tuxmake',
      version='0.18.1',
      description='Thin wrapper to build Linux kernels',
      author='Antonio Terceiro',
      author_email='antonio.terceiro@linaro.org',
      url='https://tuxmake.org/',
      packages=packages,
      package_data=package_data,
      entry_points=entry_points,
      python_requires='>=3.6',
     )
