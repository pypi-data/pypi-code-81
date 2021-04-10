import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="windlib",
    version="1.4.2",
    author="SNWCreations",
    author_email="windcheng233@gmail.com",
    description="A useful functions library for everyone.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SNWCreations/windlib",
    packages=setuptools.find_packages(),
    project_urls={
        "Bug Tracker": "https://github.com/SNWCreations/windlib/issues",
    },
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
