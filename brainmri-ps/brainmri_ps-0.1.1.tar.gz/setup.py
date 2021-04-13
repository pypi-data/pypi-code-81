import os
from pkg_resources import parse_requirements
from setuptools import setup
install_requires = []
requirements = 'requirements.txt'
if os.path.isfile(requirements):
    with open(requirements) as f:
        install_requires = f.read().splitlines()

setup(
    name='brainmri_ps',
    version='0.1.1',
    packages=['brainmri_ps'],
    url='',
    license='LICENSE.txt',
    author='lhkhiem, tuantran',
    author_email='',
    description='Automatically classify Brain MRI series by pulse sequence types: DWI, FLAIR, T1, T2, and Others',
    install_requires=install_requires,
    package_data={'checkpoints': ['checkpoints/*.pt']}
)
