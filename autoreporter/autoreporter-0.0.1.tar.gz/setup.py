import setuptools

setuptools.setup(
    name="autoreporter", # Replace with your own username
    version="0.0.1",
    author="David Huang",
    author_email="dhuang26@gmail.com",
    description="To easily format, design, and automatically generate reports",
    long_description="Autoreporter generates beautiful reports laid out using a customizable PowerPoint template. It interfaces with matplotlib for producing figures, and it does text variable substitution as well.",
    url="https://github.com/davidzqhuang/autoreporter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
