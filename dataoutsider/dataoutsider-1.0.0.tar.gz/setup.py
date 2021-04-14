import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="dataoutsider",
    version="1.0.0",
    description="Data visualization toolbox.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nickgerend/dataoutsider",
    author="Nick Gerend",
    author_email="nickgerend@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandas", "numpy"],
    entry_points={
        "console_scripts": [
            "outsider=dataoutsider.__main__:main",
        ]
    },
)