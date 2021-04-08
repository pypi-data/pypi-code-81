import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Adam_tanhx",
    version="0.0.3",
    author="junjunjun",
    author_email="996001302@qq.com",
    description="Optimizers with better performance than Adam in CIFAR-10.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/junjunjun-learner/Adam_tanhx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)