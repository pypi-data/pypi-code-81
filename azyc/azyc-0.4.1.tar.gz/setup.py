from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='azyc',
    version='0.4.1',
    packages=['azyc'],
    url='https://github.com/claasd/azyc',
    license='MIT',
    author='Claas Diederichs',
    author_email='',
    description='Helper to create large large deployment-parameters.json files from small yaml files',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "PyYaml",
    ]
)
