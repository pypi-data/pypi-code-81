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

# with open('requirements.txt') as f:
#     required = f.read().splitlines()

setuptools.setup(
    name="deployz",
    version="0.0.0.6",
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
    install_requires=[
        'aniso8601==9.0.1',
        'artifactz==0.0.2.0',
        'cachetools==4.2.1',
        'certifi==2020.12.5',
        'cffi==1.14.5',
        'chardet==4.0.0',
        'click==7.1.2',
        'coverage==5.5',
        'fastapi==0.63.0',
        'Flask==1.1.2',
        'Flask-RESTful==0.3.8',
        'google-api-core==1.26.3',
        'google-auth==1.28.0',
        'google-cloud-core==1.6.0',
        'google-cloud-storage==1.37.1',
        'google-crc32c==1.1.2',
        'google-resumable-media==1.2.0',
        'googleapis-common-protos==1.53.0',
        'h11==0.12.0',
        'idna==2.10',
        'itsdangerous==1.1.0',
        'Jinja2==2.11.3',
        'MarkupSafe==1.1.1',
        'nose==1.3.7',
        'nose2==0.10.0',
        'packaging==20.9',
        'protobuf==3.15.7',
        'providah==0.1.15.0',
        'pyasn1==0.4.8',
        'pyasn1-modules==0.2.8',
        'pycparser==2.20',
        'pydantic==1.8.1',
        'pyparsing==2.4.7',
        'pytz==2021.1',
        'PyYAML==5.4.1',
        'requests==2.25.1',
        'rsa==4.7.2',
        'six==1.15.0',
        'starlette==0.13.6',
        'typing-extensions==3.7.4.3',
        'urllib3==1.26.4',
        'uvicorn==0.13.4',
        'Werkzeug==1.0.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.8',
)
