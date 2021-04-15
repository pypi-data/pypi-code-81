import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cpMatch",
    version="0.0.1",
    author="yangmiao",
    author_email="1446174581@qq.com",
    description="Python wrapper for kailp: natural language processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ]

)