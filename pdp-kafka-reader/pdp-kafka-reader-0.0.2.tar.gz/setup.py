import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pdp-kafka-reader",
    version="0.0.2",
    author="Filip Beć",
    author_email="filip.bec@porsche.digital",
    description="PDP Kafka package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    scripts=[
        "bin/kafka-csv-export",
        "bin/export-avro-jar",
    ],
    python_requires=">=3.6",
    package_data={
        "pdp_kafka_reader": ["jars/*"],
    },
    zip_safe=False,
    install_requires=[
        "pandas>=1.1.5",
        "importlib_resources",
    ],
)
