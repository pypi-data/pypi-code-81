# -*- coding: utf-8 -*
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stocktop50",
    version="0.0.1",
    author="geejuan",
    author_email="geejuanxu@gmail.com",
    description="Stock_Clawer.",
    long_description='爬取A股每日前五十资金流入个股的数据，并生成csv格式文件保存在本地',
    long_description_content_type="text/markdown",
    url="https://github.com/geejuan/DailyStockTop50",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

