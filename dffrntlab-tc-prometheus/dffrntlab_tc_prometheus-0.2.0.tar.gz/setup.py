# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='dffrntlab_tc_prometheus',
    version="0.2.0",
    description='Thumbor Prometheus metrics extension (DffrntLab fork)',
    author='DffrntLab',
    author_email='info@dffrntlab.co',
    url='https://github.com/dffrntmedia/tc-prometheus',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'dffrntlab_thumbor',
        'prometheus_client',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
    ],
    long_description="""
Prometheus metrics extension enables thumbor to expose a scrape endpoint prometheus can scrape from.
"""
)
