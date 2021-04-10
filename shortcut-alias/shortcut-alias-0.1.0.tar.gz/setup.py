import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    require = fh.readlines()

setuptools.setup(
    name="shortcut-alias", # Replace with your own username
    version="0.1.0",
    author="Matt Limb",
    author_email="matt.limb17@gmail.com",
    description="Powerful Configurable Aliases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        req.strip() 
        for req in require
    ],
    python_requires='>=3.6',
    entry_points={  
        'console_scripts': [
            'shortcut-alias=shortcut_alias.__main__:main',
            'shortcut=shortcut_alias.__main__:main',
            'sa=shortcut_alias.__main__:main',
        ],
    }
)