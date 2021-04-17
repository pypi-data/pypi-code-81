import setuptools


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dj-optimizely',
    version='0.0.8',
    author='Gene Sluder',
    author_email='gene@gobiko.com',
    description='Store Optimizely datafile in a Django model',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/genesluder/dj-optimizely',
    project_urls={
        'Bug Tracker': 'https://github.com/genesluder/dj-optimizely/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=[
        'django',
        'requests',
        'optimizely-sdk',
    ]
)
