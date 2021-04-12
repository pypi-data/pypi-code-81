import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    use_incremental=True,
    install_requires=["incremental"],
    name="modularRobotics",  # How you named your package folder (MyLib)
    packages=["modularRobotics"],  # Chose the same as "name"
    # version=__version__,  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="A package to controll products of Modular robotics",  # Give a short description about your library
    author="Fischchen",  # Type in your name
    author_email="tipp.klever@gmail.com",  # Type in your E-Mail
    url="https://github.com/Fischchen/modular-robotics",  # Provide either the link to your github or to your website
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/Fischchen/modular-robotics/archive/v0.1-alpha.tar.gz",  # I explain this later on
    keywords=[
        "SOME",
        "MEANINGFULL",
        "KEYWORDS",
    ],  # Keywords that define your package best
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)