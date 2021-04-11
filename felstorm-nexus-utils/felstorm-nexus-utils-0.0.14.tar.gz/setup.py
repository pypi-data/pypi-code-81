import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="felstorm-nexus-utils",
    version="0.0.14",
    author="Felstorm",
    author_email="support@felstorm.com",
    description="Utility functions for Felstorm Nexus projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/felstorm-nexus-utils",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/felstorm-nexus-utils/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", exclude=[]),
    python_requires=">=3.6",
    install_requires=['flask', 'jinja2'],
    excluded = ['flask_app'],
    include_package_data = True
)
