import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="dataoutsider",
    version="1.0.2",
    description="Data visualization toolbox.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/dataoutsider/",
    author="Nick Gerend",
    author_email="nickgerend@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['dataoutsider'],
    install_requires=["pandas", "numpy"],
)