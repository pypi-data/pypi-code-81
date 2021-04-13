import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="mdcompiler",
    version="2021.04.01",
    author="TechGeeks",
    author_email="MDCompiler@tgeeks.cf",
    maintainer="Rajdeep Malakar",
    maintainer_email="Rajdeep@tgeeks.cf",
    description="a free & OpenSource Markdown Compiler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TechGeeks-Dev/MDC",
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
        console_scripts=['mdc=MDC.__init__:cli']
    )
)