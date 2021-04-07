import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as fr:
    requirements = fr.read().splitlines()

setuptools.setup(
    name="mc-downloader",
    version="0.0.2",
    license="MIT",

    author="Couapy",
    author_email="contact@marchand.cloud",

    description="A downloader tool for Minecraft servers from Mojang services.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/Couapy/mc-downloader",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
