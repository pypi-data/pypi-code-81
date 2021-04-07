import os
import re
# To use a consistent encoding
from codecs import open as copen

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with copen(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def read(*parts):
    with copen(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version("ros_configurator", "__version__.py")

test_deps =[
    "pytest",
    "pytest-cov",
]

extras = {
    'test': test_deps,
}

setup(
    name='ros_configurator',
    version=__version__,
    description="Ros Configurator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/micheleantonazzi/ros_configurator",
    author="Michele Antonazzi",
    author_email="micheleantonazzi@gmail.com",
    # Choose your license
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    tests_require=test_deps,
    # Add here the package dependencies
    install_requires=[
        "pathlib",
        "sockets",
        "termcolor",
        "regex"
    ],
    entry_points={
        'console_scripts': [
            'ros_config_set_ip = ros_configurator.functions:set_ip',
            'ros_config_set_ip_localhost = ros_configurator.functions:set_ip_localhost',
            'ros_config_set_ros_master_uri = ros_configurator.functions:set_ros_master_uri',
            'ros_config_list_source_files = ros_configurator.functions:list_source_files',
            'ros_config_add_source_file = ros_configurator.functions:add_source_file',
            'ros_config_remove_source_file = ros_configurator.functions:remove_source_file'
        ],
    },
    test_deps=test_deps,
    extras_require=extras,
)
