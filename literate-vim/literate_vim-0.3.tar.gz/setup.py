from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="literate_vim",
    description="Literate vim configuration.",
    version="0.3",
    author="Joao Freitas",
    author_email="joaj.freitas@gmail.com",
    license="GPLv3",
    url="https://gitlab.com/joajfreitas/literate-vim",
    packages=find_packages(),
    entry_points={"console_scripts": ["literate_vim = literate_vim.__main__:main",],},
    install_requires=["markdown", "loguru"],
    long_description=long_description,
    long_description_content_type="text/markdown"
)
