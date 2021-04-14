import setuptools

setuptools.setup(
    name="koti-basic-math", # Replace with your own username
    version="0.0.1",
    author="Koteswararao Gummadidala",
    author_email="gkrkoti3@gmail.com",
    description="A small math package",
    long_description="long_description",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
