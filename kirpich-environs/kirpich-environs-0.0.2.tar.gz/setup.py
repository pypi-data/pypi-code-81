import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["environs<=5.2.1"]

setuptools.setup(
    name="kirpich-environs",
    version="0.0.2",
    author="LLC Kirpich",
    author_email="support@kirpich.it",
    description="Пакет с оберткой над environ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/kirpich-environs/",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
