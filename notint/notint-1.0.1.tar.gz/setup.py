from setuptools import setup,find_packages
setup(
    name='notint',
    version='1.0.1',
    description='This is not an integer',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/donno2048/notint',
    packages=find_packages(),
    license='MIT',
    author='Elisha Hollander',
    classifiers=['Programming Language :: Python :: 3']
)
