#! /usr/bin/python3
#

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
      long_description = fh.read()

setuptools.setup(name="dns_zone_builder",
      version="0.1.11",
      description="Build DNS zone files from python",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Martin Ibert",
      author_email="python@maribert.info",
      license="MIT",
      packages=["dns_zone_builder"],
      classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      python_requires=">=3.7",
      install_requires=["ipaddress"],
      zip_safe=True)