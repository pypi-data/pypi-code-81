import setuptools

setuptools.setup(
    name="appchance-redlink",
    version="0.0.3",
    author_email="backend@appchance.com",
    short_description="Appchance Redlink Extensions",
    description="Redlink extensions for Django projects.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/appchance/appchance-redlink/",
    packages=setuptools.find_packages(),
    install_requires=["django", "swapper"],
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
)
