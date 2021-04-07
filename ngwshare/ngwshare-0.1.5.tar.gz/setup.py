import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ngwshare", # Replace with your own username
    version="0.1.5",
    author="Wang Jian",
    author_email="296348304@qq.com",
    description="data api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/296348304/ngwshare",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)