import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="2.5D",
    version="0.0.2",
    author="K6nE",
    author_email="maknix@k6nesoftware.com",
    description="With this module you can create kind of 3D games easily. Documentation will be created soon.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://k6nesoftware.com",
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires=">=3.7",
)
