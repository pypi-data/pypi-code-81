import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pysvgexport',
    version='1.0.3',
    scripts=[],
    author="vantrong291",
    author_email="vantrong291@gmail.com",
    description="A package for exporting svg format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vantrong291/pysvgexport",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pyppeteer', 'Pillow'
    ],
    include_package_data=True,
)