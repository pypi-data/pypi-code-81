import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydopi", # Replace with your own username
    version="0.0.1",
    author="cijliu",
    author_email="cijliu@qq.com",
    description="dopi opensource library for IoT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cijliu/pydopi-iot",
    project_urls={
        "Bug Tracker": "https://github.com/cijliu/pydopi-iot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.6",
)