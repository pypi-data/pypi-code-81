import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ic_slide",
    packages=['ic_slide'],
    package_dir={'': 'src'},
    version="0.2.8",
    author="rwecho",
    author_email="rwecho@live.com",
    description="api of coriander slides, communicate with private cloud slides. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests>=2.22.0",
        "Pillow>=6.2.0",
        "numpy>=1.16.5",
    ],
    python_requires='>=3.6',
)
