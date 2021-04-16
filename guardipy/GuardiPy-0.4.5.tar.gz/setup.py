import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="GuardiPy",
    version="0.4.5",
    author="cmcghee",
    author_email="devops@idealintegrations.net",
    description="Unofficial Python 3.x library for Guardicore Centra (based on API 3.0).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BlueBastion/GuardiPy",
    packages=setuptools.find_packages(),
    install_requires=required,
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
