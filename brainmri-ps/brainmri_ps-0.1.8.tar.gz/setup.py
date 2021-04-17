from setuptools import setup

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name='brainmri_ps',
    version='0.1.8',
    packages=['brainmri_ps'],
    url='',
    license='LICENSE.txt',
    author='lhkhiem, tuantran',
    author_email='',
    description='Automatically classify Brain MRI series by pulse sequence types: DWI, FLAIR, T1, T2, and Others',
    install_requires=install_requires,
)