from setuptools import setup, find_packages

with open(file='README.md', mode='r') as fh:
    long_description = fh.read()

setup(
    name='crisper',
    version='0.0.1',
    author='JD',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=('docs', 'tests')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    python_requires='>=3.6'
)
