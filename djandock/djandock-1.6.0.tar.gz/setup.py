import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="djandock",
    version="1.6.0",
    author="marxygen",
    author_email="marxygen@gmail.com",
    description="A simple utility to create Django projects with virtual environment, Git and Docker all set up",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marxygen/djandock",
    project_urls={
        "Bug Tracker": "https://github.com/marxygen/djandock/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    package_data={'djandock': ['Dockerfile', 'docker-compose.yml']},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)