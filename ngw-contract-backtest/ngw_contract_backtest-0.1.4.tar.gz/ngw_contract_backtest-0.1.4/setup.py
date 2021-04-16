import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ngw_contract_backtest", # Replace with your own username
    version="0.1.4",
    author="Wang Jian",
    author_email="296348304@qq.com",
    description="contract framework 014",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/296348304/ngw_contract_backtest",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)