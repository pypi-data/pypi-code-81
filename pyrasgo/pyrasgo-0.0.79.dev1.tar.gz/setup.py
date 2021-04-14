from setuptools import setup
import os

_here = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(_here, 'pyrasgo', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='pyrasgo',
    version=version['__version__'],
    description=('Alpha version of the Rasgo Python interface.'),
    long_description='Alpha version of the Rasgo Python interface.',
    author='Patrick Dougherty',
    author_email='patrick@rasgoml.com',
    url='https://www.rasgoml.com/',
    license='MPL 2.0',
    packages=['pyrasgo',
              'pyrasgo.api',
              'pyrasgo.primitives',
              'pyrasgo.schemas',
              'pyrasgo.schemas.feature_set',
              'pyrasgo.storage',
              'pyrasgo.utils'],
    install_requires=[
        # Note these are duplicated in requirements.txt
        "idna>=2.5,<3",
        "more-itertools",
        "pandas",
        "pyarrow>=3.0.0",
        "pydantic",
        "pyyaml",
        "requests",
        "snowflake-connector-python>=2.4.0",
        "snowflake-connector-python[pandas]",
        "tqdm"
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.7'],
)
