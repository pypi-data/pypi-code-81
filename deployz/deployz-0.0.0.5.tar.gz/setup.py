# Copyright © 2021 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="deployz",
    version="0.0.0.5",
    author="Hashmap, Inc",
    author_email="accelerators@hashmapinc.com",
    description="DO NOT USE - This is a sample program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hashmapinc/deployz",
    packages=setuptools.find_packages(),
    package_data={
    },
    entry_points={
        'console_scripts': [
            'deployz=deployz.deployer:run'
        ]
    },
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.8',
)
