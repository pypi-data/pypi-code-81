import os

from setuptools import find_packages, setup

project_name = "django-nofloc"

if os.path.exists("README.rst"):
    long_description = open("README.rst").read()
else:
    long_description = (
        "See https://hg.code.netlandish.com/~netlandish/django-nofloc"
    )


setup(
    name=project_name,
    version=__import__("nofloc").get_version(),
    package_dir={project_name: project_name},
    packages=find_packages(),
    description=("Opt out of the privacy invading Google FLoC program."),
    author="Netlandish Inc.",
    author_email="hello@netlandish.com",
    license="BSD License",
    url="https://hg.code.netlandish.com/~netlandish/django-nofloc",
    long_description=long_description,
    platforms=["any"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
