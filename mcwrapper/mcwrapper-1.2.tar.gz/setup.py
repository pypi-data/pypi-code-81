import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mcwrapper",
    version="1.02",
    author="Zidane Karim",
    author_email="zkarim7676@gmail.com",
    description="A Minecraft API Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThePotatoPowers/mcapiwrapper",
    project_urls={
        "Bug Tracker": "https://github.com/ThePotatoPowers/mcapiwrapper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    license='MIT',
    package_dir={"": "src"},
    install_requires = ['requests'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)       