# coding: --utf-8--
import os

from setuptools import setup, find_packages

# install requirements
with open('requirements.txt') as f:
    requirements = [x.strip() for x in f.readlines()]

name = "web_frame"


def gen_data_files(*dirs):
    results = ["requirements.txt"]

    for src_dir in dirs:
        for root, dirs, files in os.walk(name + os.path.sep + src_dir):
            results.append((root, map(lambda f: root + os.path.sep + f, files)))
    print(results)
    return results


setup(
    name=name,
    version='0.0.1',
    description=u'基于tornado封装简易开发框架',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: C',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Scientific/Engineering :: GIS'],
    keywords='coordinate vector china',
    author='jinchengzhen',
    author_email='13555746358@163.com',
    url='https://github.com/jinchengzhen',
    include_package_data=True,
    data_files=gen_data_files("templates"),
    packages=find_packages(),
    install_requires=requirements,
)
