import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="headpy",
    version="0.0.1",
    author="Petr Martynenko",
    author_email="petr.martynenko@gmail.com",
    description="A tiny wrapper of app auth and vacancy search on hh.ru API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/retardigrade/headpy",
    project_urls={
        "Bug Tracker": "https://github.com/retardigrade/headpy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
    install_requires=["requests", "tqdm"]
)