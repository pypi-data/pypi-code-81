# Copyright 2021 Francesco Apruzzese <cescoap@gmail.com>
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl-3.0.html).

from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="marche",
    version="0.1.2",
    description="MaRChE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenCode/marche",
    author="Francesco Apruzzese",
    author_email="cescoap@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Software Development :: Version Control",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="github massive repository branch git vcs",
    license="GPLv3",
    packages=["marche"],
    install_requires=["click>=7.1.2", "pyyaml>=5.3.1", "PyGithub>=1.53"],
    entry_points={"console_scripts": ["marche=marche.core:entrypoint"]},
    zip_safe=False,
)
