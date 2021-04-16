import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mdx_spanner", # Replace with your own username
    version="0.0.5",
    author="Marc Schleeweiß",
    author_email="mschleeweiss@gmail.com",
    description="Span table cols and rows in MkDocs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mschleeweiss/mdx_spanner",
    project_urls={
        "Bug Tracker": "https://gitlab.com/mschleeweiss/mdx_spanner/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
