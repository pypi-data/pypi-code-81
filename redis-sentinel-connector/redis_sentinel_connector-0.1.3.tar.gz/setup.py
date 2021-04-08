import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redis_sentinel_connector",
    version="0.1.3",
    author="Ronaldo Duarte",
    author_email="ronaldoduarte@globo.com",
    description="A package that works with Redis Sentinel.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ronaldodduarte/redis_sentinel_connector",
    install_requires=["redis", "fakeredis"],
    packages=["redis_sentinel_connector"],
    license="GNU",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
