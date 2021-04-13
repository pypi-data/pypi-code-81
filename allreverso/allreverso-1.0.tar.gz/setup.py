from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="allreverso",
      version="1.0",
      description="A simple package to handle allreverso.net services (translation, voice, dictionary etc.).",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="PetitPotiron",
      author_email="malocollet@hotmail.com",
      packages=["allreverso"],
      install_requires=["requests", "bs4"],
      license="Apache 2.0",
      classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
            "Environment :: Console",
            "Environment :: Web Environment",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
      ]
      )
