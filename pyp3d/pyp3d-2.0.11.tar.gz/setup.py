import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyp3d",
    version="2.0.11",
    author="Copyright (C), 2020, Beijing GLory PKPM Technology. Co., Ltd. All rights reserved.",
    author_email="youqi@cabrtech.com",
    url="",
    description="Python interface of P3D.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free For Educational Use",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
        'pywin32',
        'numpy == 1.19.3',
    ],
    python_requires='>=3.6',
)
