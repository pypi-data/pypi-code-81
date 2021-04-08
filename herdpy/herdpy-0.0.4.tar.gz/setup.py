import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="herdpy", # Replace with your own username
    version="0.0.4",
    author="Steffen Park",
    author_email="dev@istherepie.com",
    description="Building a project herd client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/istherepie/herd-python-client",
    project_urls={
        "Bug Tracker": "https://github.com/istherepie/herd-python-client/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "requests==2.25.1"
    ],
    tests_require=[
        "pytest==6.2.3"
    ]
)
