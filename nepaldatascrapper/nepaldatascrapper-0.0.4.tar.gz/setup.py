import setuptools

long_description = ""
with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nepaldatascrapper", # Replace with your own username
    version="0.0.4",
    author="Sujit Maharjan",
    author_email="shubhajeet.per@gmail.com",
    description="Package that scraps data related to Nepal for further analysis through panda or spreadsheet.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shubhajeet/nepaldatascrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
