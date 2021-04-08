from distutils.core import setup
version_string = "0.1.4"
setup(
    name='awsome',
    packages=['awsome'],
    version=version_string,
    license='MIT',
    description='aws utilities to make my life easier',
    author='zdunker',
    author_email='robinli.forwork@gmail.com',
    url='https://github.com/zdunker/awsome',
    download_url='https://github.com/zdunker/awsome/archive/refs/tags/'+version_string+'.tar.gz',
    keywords=['aws', 'utility'],
    install_requires=[
        'boto3',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
