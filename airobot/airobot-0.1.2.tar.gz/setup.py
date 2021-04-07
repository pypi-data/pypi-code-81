import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airobot",
    version="0.1.2",
    author="August",
    author_email="august@163.com",
    description="aichat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/August/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = ['requests']
)