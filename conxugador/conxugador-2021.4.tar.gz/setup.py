import setuptools
from importlib.metadata import entry_points

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="conxugador",
    version="2021.4",
    author="Andrés Vieites",
    author_email="andres@vieites.gal",
    description="This tool conjugates Galician verbs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GNU GPLv3",
    url="https://gitlab.com/avieites/conxugador",
    project_urls={
        "PyPI": "https://pypi.org/project/conxugador/",
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Console",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Natural Language :: Galician",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "console_scripts": [
            "conxugador=conxugador.__main__:main"
        ]
    },
    package_data={"": ["verbos.txt"]},
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
)
