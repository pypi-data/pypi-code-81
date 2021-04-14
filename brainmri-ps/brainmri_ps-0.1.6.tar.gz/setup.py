from pkg_resources import parse_requirements
from setuptools import setup

setup(
    name='brainmri_ps',
    version='0.1.6',
    packages=['brainmri_ps'],
    url='',
    license='LICENSE.txt',
    author='lhkhiem, tuantran',
    author_email='',
    description='Automatically classify Brain MRI series by pulse sequence types: DWI, FLAIR, T1, T2, and Others',
    install_reqs=parse_requirements('requirements.txt'),
)