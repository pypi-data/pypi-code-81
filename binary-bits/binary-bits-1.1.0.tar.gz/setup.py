import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="binary-bits",
    version="1.1.0",
    author="S Groesz",
    description="Provide additional methods for working with binary data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wolfpackmars2/bits",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['bits'],
    package_dir={'': 'src'},
    test_suite='tests',
    extras_require={
        'test': ['coverage'],
    },
    project_urls={
        'Source': 'http://git.groesz.org/wp/bits/',
    },
)
