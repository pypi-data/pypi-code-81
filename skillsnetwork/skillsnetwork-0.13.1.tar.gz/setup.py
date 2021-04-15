from setuptools import setup

setup(
    name='skillsnetwork',
    version='0.13.1',
    license='MIT',
    author='Bradley Steinfeld',
    author_email='bs@ibm.com',
    url='http://vision.skills.network',
    long_description="README.md",
    packages=['skillsnetwork'],
    scripts=['bin/cvstudio','bin/cvstudio_report','bin/cvstudio_ping','bin/cvstudio_download_all','bin/cvstudio_upload_model','bin/cvstudio_download_model'],
    install_requires=['requests','ibm-cos-sdk==2.0.1','tqdm'],
    description="Skills Network",
)
