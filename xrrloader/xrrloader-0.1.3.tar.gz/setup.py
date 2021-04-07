from setuptools import setup, find_packages

with open('requirements.txt') as file:
    requirements = file.readlines()

setup(
    name='xrrloader',
    version='0.1.3',
    author='Alessandro Greco',
    author_email='alessandro.greco@uni-tuebingen.de',
    licence='GPL3',
    packages=find_packages(),
    zip_safe=False,
    install_requires=requirements,
    python_requires='>=3.6'
)
