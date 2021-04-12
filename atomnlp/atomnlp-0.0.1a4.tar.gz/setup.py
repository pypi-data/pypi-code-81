import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atomnlp",
    version="0.0.1a4",
    author="GaoangLau",
    author_email="byteleap@gmail.com",
    description="Atomic Natural Language Processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GaoangLiu/atomnlp",
    packages=setuptools.find_packages(),
    package_data={"atomnlp":["data/dict.txt", 'data/oov.txt']},
    install_requires=['colorlog>=4.6.1', 'tqdm>=4.56.0'],
    entry_points={
        'console_scripts': ['atom=atomnlp.entry:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
