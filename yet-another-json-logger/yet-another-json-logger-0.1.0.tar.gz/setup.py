from setuptools import find_packages, setup


with open('README.md') as f:
    long_description = f.read()

setup(
    name='yet-another-json-logger',
    version='0.1.0',
    packages=find_packages(),
    author='Alen Buhanec <alen.buhanec@gmail.com>',
    license='MIT',
    description='A simple JSON logger, used for structured logging',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/buhanec/yet-another-json-logger',
    classifiers=[
        'Topic :: System :: Logging',  # doesn't seem quite right, does it?
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Typing :: Typed',
    ],
)
