from setuptools import setup, find_packages
import os

#with open("README.md", "r") as f:
#    long_description = f.read()

setup(
    name='sync-mpv',
    version='0.25',
    description='Host a server and watch any youtube-dl compatible video in synchronization with your peers.',
    author='midnightman',
    author_email='midnightman@protonmail.com',
    license='Apache-2.0',
    url="https://github.com/mdnghtman/sync-mpv",
    py_modules=[
        "sync_mpv_client",
        "sync_mpv_server"],
    package_dir={'': 'sync-mpv'},
    scripts =[
        'bin/sync-mpv-client',
        'bin/sync-mpv-server',
    ]
    ,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        'Operating System :: POSIX :: Linux',
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires='>=3.6',
    install_requires=['pycryptodome',
    'python-mpv-jsonipc',
    ]
)
