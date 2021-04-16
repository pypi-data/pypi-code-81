import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dirba",
    version="0.1.0",
    author="Mansur Izert",
    author_email="izertmi@uriit.ru",
    description="Small ML boilerplate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://git2.uriit.local/CIAS/dirba.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["requests",
                      "fastapi>=0.63.0",
                      "pydantic==1.8.1",
                      "python-multipart>=0.0.5",
                      "uvicorn>=0.11.3",
                      "aiokafka>=0.7.0,<0.8.0",
                      "pandas>=1.0.1",
                      "scikit-learn>=0.21.0.1,<0.24",
                      "aiomisc==12.1.0",
                      "aiohttp>3.7.0,<4.0.0",
                      "aiohttp-asgi>=0.3.1",
                      "orjson>=3.5.1",
                      "sentry-sdk>=0.19.0",
                      "cachetools>=4.2.1",
                      "asyncache>=0.1.1",
                      "prometheus_client>=0.10.1,<0.11.0",
                      ],
)
