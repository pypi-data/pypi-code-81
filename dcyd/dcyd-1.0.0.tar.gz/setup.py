'''
# DCYD Model Performance Monitoring Client

Visit https://www.dcyd.io/ for more details.

## Install

Requires Python 3 before start

### Using pip

```
pip3 install dcyd -U
```

### Using pipenv

```
pipenv install dcyd
```


## Configure

Generate the **dcyd.json** configuration file

```bash
dcyd-config $DCYD_PROJECT_ID $DCYD_PROJECT_ACCESS_TOKEN
```

Point the **DCYD_CONFIG_FILE** environment variable to the above file location

```bash
export DCYD_CONFIG_FILE=/path/to/project/dcyd.json
```

## Usage

### Simple monitoring

```python
from dcyd import dcyd

@dcyd.monitor
def my_predict_function(features):
    result = None
    # run my model(s) logic
    return result
```

### Transform function arguments before sending out

```python
from dcyd import dcyd

@dcyd.monitor(transformers={
    'arg1': lambda value: value + 1,
    'arg2': lambda value: value - 1,
    'arg3': lambda value: value * -1,
})
def my_predict_function(arg1, arg2=2, arg3=10):
    result = None
    # run my model(s) logic
    return result
```

### Transform function return value before sending out

```python
from dcyd import dcyd

@dcyd.dcyd.monitor(return_transformer=lambda value: value + 1)
def my_predict_function():
    return 0
```


### Turn on writing data to a local file

Set the environment variable `DCYD_CLIENT_FILE_LOGGER` with the file path you want to write to.

An example is:

```
export DCYD_CLIENT_FILE_LOGGER=/tmp/dcyd-client.log
```

### Disable sending data to DCYD

Make sure the `dcyd.json` file is *absent* from your project directory.

And make sure these environment variables are *absent* from the process. You can unset them by running the following:

```
unset DCYD_CONFIG_FILE
unset DCYD_PROJECT_ID
unset DCYD_PROJECT_ACCESS_TOKEN
```


'''

from setuptools import setup, find_packages

import dcyd

setup(
    name="dcyd",
    version=dcyd.__version__,
    author="dcyd, inc.",
    author_email="info@dcyd.io",
    description="dcyd model performance monitoring client",
    long_description=__doc__,
    long_description_content_type="text/markdown",
    url="https://github.com/dcyd-inc/dcyd-mpm-client-python",
    entry_points={
        'console_scripts': [
            'dcyd-config = dcyd.config:main',
        ],
    },
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'google-cloud-logging==2.2.0',
        'requests',
    ],
    tests_require=[
        'pytest',
    ],
    python_requires='>=3.5',
    package_data={
        'dcyd': ['static/*.txt']
    }
)
