from setuptools import setup, find_packages

import compileall

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

compileall.compile_dir("datarangers")

setup(
    name='datarangers-sdk-python',
    version='1.0.2',
    packages=['datarangers',
              'datarangers.collector',
              'datarangers.collector.config',
              'datarangers.collector.writer',
              'datarangers.collector.model',
              'datarangers.collector.util'],
    url='https://github.com/volcengine/datarangers-sdk-py',
    license='Apache 2.0',
    author='DataRangers',
    author_email='datarangers-opensource@bytedance.com',
    description='datarangers-sdk-py是 [DataRangers](https://datarangers.com.cn/) 的用户行为采集服务端SDK',
    keywords='datarangers, server',
    python_requires='>=3.4, <4',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests']
)
