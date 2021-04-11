import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-jjy37777", # Replace with your own username
    version="0.0.1",
    author="jjy37777",
    author_email="jjy37777@naver.com",
    description="jjy ai framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/woduq1414/deep-learning-without-framework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)