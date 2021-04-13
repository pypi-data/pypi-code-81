import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="tgcc",
    version="1.0.0",
    author="TechGeeks",
    author_email="TGCompilers@tgeeks.cf",
    maintainer="Rajdeep Malakar",
    maintainer_email="Rajdeep@tgeeks.cf",
    description="TechGeeks Compiler Collections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TechGeeks-Dev/tgcc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'markdown'
    ],
    entry_points=dict(
        console_scripts=['tgcc=tgcc.cli:cli']
    )
)