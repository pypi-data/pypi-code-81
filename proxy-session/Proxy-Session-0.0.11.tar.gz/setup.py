from setuptools import setup
from proxy_session import __module__
from proxy_session import __version__


def readme():
    with open('./README.md') as readme_fp:
        README = readme_fp.read()
    return README


setup(
    name=__module__,
    version=__version__,
    description='''
        {0} is a python module, helps to make a reliable proxy request to a HTTP server.
        Current version of this module is {1}
    '''.format(__module__, __version__),
    long_description=readme(),
    long_description_content_type='text/markdown',
    url="https://github.com/antaripchatterjee/Proxy-Session",
    author="Antarip Chatterjee",
    author_email="antarip.chatterjee22@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Environment :: Console",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Software Development"
    ],
    packages=["proxy_session"],
    install_requires=[
        "beautifulsoup4==" + "4.9.3",
        "html5lib==" + "1.1",
        "requests==" + "2.25.1"
    ],
    include_package_data=True
)