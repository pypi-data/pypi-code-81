from setuptools import setup, find_packages
 

setup(
    name="facevision", # Replace with your own username
    version="0.0.4",
    author="Felipe Oliveira",
    author_email="gavb@gavb.com",
    description='The computer vision library focused on facial recognition pipeline.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url="",
    packages=find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ]
)