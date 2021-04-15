import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent


def parse_requirements(file):
    required = []
    with open(file) as f:
        for req in f.read().splitlines():
            if not req.strip().startswith("#"):
                required.append(req)
    return required


version = "0.4.3"
requires = parse_requirements("requirements.txt")
tests_requires = parse_requirements("requirements.tests.txt")
README = (HERE / "README.md").read_text()

setup(
    name="docker-volume-dump",
    version=version,
    description="Create your backups based on docker labels",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[],
    author="Pierre Verkest",
    author_email="pierreverkest84@gmail.com",
    url="https://gitlab.com/micro-entreprise/docker-volume-dump",
    license="GPLv3+",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    namespace_packages=["archiver"],
    install_requires=requires,
    tests_require=requires + tests_requires,
    entry_points="""
    [console_scripts]
    archive=archiver.archive:backup
    """,
)
