import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xtermutil", # Replace with your own username
    version="0.0.3",
    author="Marcelo Luciano",
    author_email="Marcelo.Perseus@gmail.com",
    description="A package to help customize xterm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Marcelo-Perseus/xterm-util",
    project_urls={
        "Bug Tracker": "https://github.com/Marcelo-Perseus/xterm-util/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
