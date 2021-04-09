import setuptools

setuptools.setup(
    name="data-in-tools",
    version="0.0.1",
    author="Data-in Admins",
    author_email="data-in-admins@funnel.io",
    description="A small example package",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
