import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hp-tracker",
    version="0.0.2",
    author="Vojko Pribudić",
    author_email="dmanthing@gmail.com",
    description="Track posta.hr package status",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/vojko.pribudic/hp-tracker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["bs4", "requests"],
    python_requires=">=3.6",
)
