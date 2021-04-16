import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="luckyrandom", # Replace with your own username
    version="0.0.3",
    author="Maximilian Wu",
    author_email="me@maxesisn.online",
    description="Encourage users with bad luck",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxesisn/luckyrandom",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)