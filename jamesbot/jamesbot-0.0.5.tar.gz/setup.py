import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jamesbot", 
    version="0.0.5",
    author="Faruk Hammoud, Felipe Freire Pinto",
    author_email="farukhammoud@student-cs.fr, felipe.fp@student-cs.fr",
    description="Download and Store financial data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felipe-fp/JamesBot",
    packages=setuptools.find_packages(),
	install_requires=[
   'pandas',
   'datetime',
   'yfinance'
	],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
