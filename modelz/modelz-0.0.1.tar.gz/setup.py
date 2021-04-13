from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="modelz",
    version='0.0.1',
    author="Nathan Raw",
    author_email="naterawdata@gmail.com",
    description="",
    install_requires=requirements,
    packages=find_packages(),
)
