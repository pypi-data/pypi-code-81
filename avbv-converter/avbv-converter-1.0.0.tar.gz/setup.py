import setuptools
with open("README.md", "r") as rm:
    long_description = rm.read()

setuptools.setup(
    name="avbv-converter",
    version="1.0.0",
    author="lenovo",
    author_email="2276316223@qq.com",
    description="a simple av bv converter",
    long_description=long_description,
    long_desciption_content_type="text/markdown",
    url="https://github.com/xiaohuangren1001/Bilibili-av-bv-converter",
    packages=setuptools.find_packages(),
    classifers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
