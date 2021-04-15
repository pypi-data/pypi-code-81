import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vk_types",
    version="0.2.2",
    author="kz159",
    description="vk_types for vk json answers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kz159/vk_types",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
