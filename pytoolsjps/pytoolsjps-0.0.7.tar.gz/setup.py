from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pytoolsjps',
    version='0.0.7',
    description='Collection of helper tools',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    #include_package_data=True,  # Checks MANIFEST.in for explicit rules
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning"
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "greenlet >= 1.0.0",
        "numpy >= 1.20.2",
        "pandas >= 1.2.3",
        "psycopg2-binary >= 2.8.6",
        "python-dateutil >= 2.8.1",
        "python-dotenv >= 0.16.0",
        "pytz >= 2021.1",
        "six >= 1.15.0",
        "SQLAlchemy >= 1.4.4",
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
    author='Jan Schüler',
    author_email='janpschueler@gmail.com',
    url='https://github.com/jan-schueler/pytools',
)
