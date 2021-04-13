# @Time     : 2021/3/27
# @Project  : w8_auto_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from setuptools import setup, find_packages

_name = "w8_auto_py"
_author = "angel"
_author_email = "376355670@qq.com"
_description = "auto_tool"


def get_long_description():
    long_description = ""
    with open("README.md", mode="r", encoding="utf-8") as rd:
        long_description += rd.read()

    return long_description


setup(
    name=_name,
    version="0.2.5",
    author=_author,
    author_email=_author_email,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7"
)
