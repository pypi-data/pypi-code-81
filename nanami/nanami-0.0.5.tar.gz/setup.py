import os
from setuptools import setup, find_packages

project_name = "nanami"
version = os.environ.get('COMMIT_VERSION', '0.0.0')

with open('requirements.txt') as f:
    required = f.read().splitlines()

if __name__ == "__main__":

    with open('README.md', 'r') as t:
        README = t.read()

    setup(
        name=project_name,
        version=version,
        long_description=README,
        long_description_content_type='text/markdown',
        license="",
        author="nanami-ci",
        author_email="gray@nanami.io",
        description="",
        url="https://github.com/nanami-ci/client",
        python_requires=">=3.6",
        platforms=["any"],
        project_urls={
            "Source Code": "https://github.com/nanami-ci/client",
        },
        install_requires=required,
        entry_points={
            'console_scripts': [
                'nanami=nanami.main:cli'
            ],
        },
        packages=find_packages(),
    )