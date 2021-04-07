import os
import pathlib
from setuptools import setup,find_packages
def parse_requirements(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir) for ir in install_reqs]

here = pathlib.Path(__file__).parent #os.path.abspath(os.path.dirname(__file__))
README = (here/"README.md").read_text() #open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-doclib',
    version='1.2.0',
    packages=find_packages(),
    description='A Document library',
    long_description=README,
    long_description_content_type="text/markdown",
    authors='Dharmesh Singh, Pratyush Jaiswal',
    classifiers =[
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.7"
    ],
    authors_email='dharmeshsinghpaliwal.7@gmail.com, jaiswalpratyush2015@gmail.com',
    url='https://github.com/Pratyush1606/doclib',
    license='MIT',
    install_requires=reqs,
    include_package_data=True
)
