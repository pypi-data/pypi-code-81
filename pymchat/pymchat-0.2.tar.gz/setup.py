import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymchat", # Replace with the pkg name
    version="0.2",
    author="Alexandre Silva // MrKelpy",
    author_email="alexandresilva.coding@gmail.com",
    description="A Simple and easy-to-use Python Library to read and interact with Minecraft's Chat in real time.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrKelpy/PyMChat",
    packages=setuptools.find_packages(),
    install_requires=["keyboard", "pygetwindow"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)