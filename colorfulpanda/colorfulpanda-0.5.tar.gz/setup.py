import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colorfulpanda",
    version="0.5",
    author="LeePanda",
    author_email="leepandapia@gmail.com",
    description="a colorful printer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PandaTea/colorfulPanda",
    packages=setuptools.find_packages(),
    install_requires=['sty', 'tqdm'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
