import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wispyjim",
    version="1.3.8",
    author="JimTheScientist",
    author_email="aidannpratt@gmail.com",
    description="A tiny Python package to interect with the WISP.gg API, modified by JimTheScientist",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JimTheScientist/wisp.py",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    keywords = ['wisp', 'api-wrapper', 'api', 'gaming', 'wrapper'],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent",
    ],
    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
)