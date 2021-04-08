from setuptools import setup

requires = [
    "requests>=2.25.1",
]
test_requirements = []

about = {
    "name": "source_aggregation",
    "description": "An API wrapper for the Source Aggregation Service.",
    "url": "https://github.com/wepublic-nl",
    "version": "0.1.2",
    "author": "Wepublic",
    "email": "stakeholderintel@wepublic.nl",
    "license": "Other/Proprietary License",
    "copyright": "All rights reserved",
}

setup(
    name=about["name"],
    version=about["version"],
    description=about["description"],
    author=about["author"],
    author_email=about["email"],
    url=about["url"],
    packages=["source_aggregation"],
    package_dir={"source_aggregation": "source_aggregation"},
    include_package_data=True,
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*",
    install_requires=requires,
    license=about["license"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    project_urls={
        "Source": "https://github.com/wepublic-nl",
    },
)
