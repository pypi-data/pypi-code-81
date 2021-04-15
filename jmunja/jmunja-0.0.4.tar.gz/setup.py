import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jmunja", # Replace with your own username
    version="0.0.4",
    author="Jaesang Jo",
    author_email="oralol@naver.com",
    description="Jmunja message send package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nicecoding1/jmunja",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
