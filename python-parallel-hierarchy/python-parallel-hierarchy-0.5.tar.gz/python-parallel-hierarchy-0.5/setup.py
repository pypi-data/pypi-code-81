#
#     Copyright 2021 Joël Larose
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
#
# type: ignore

"""Setup file for python-parallel-hierarchy."""

from setuptools import setup, find_packages

with open("README_pypi.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
        name='python-parallel-hierarchy',
        version='0.5',
        url='https://gitlab.com/joel.larose/python-parallel-hierarchy',
        license='Apache License 2.0',
        author='Joël Larose',
        author_email='joel.larose@gmail.com',
        description='A utility for creating a parallel class hierarchy based on a '
                    'primary set of classes.',
        long_description=long_description,
        long_description_content_type="text/x-rst",
        classifiers=[
                "Development Status :: 4 - Beta",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                "Programming Language :: Python :: 3.10",
                "License :: OSI Approved :: Apache Software License",
                "Operating System :: OS Independent",
                "Topic :: Software Development :: Code Generators",
                "Topic :: Software Development :: Libraries",
                "Topic :: Utilities",
                "Typing :: Typed",
                "Intended Audience :: Developers"
        ],
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        python_requires=">=3.8",
)
