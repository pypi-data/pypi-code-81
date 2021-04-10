from setuptools import setup

url = "https://github.com/jic-dtool/dtool-create"
version = "0.23.3"
readme = open('README.rst').read()

setup(
    name="dtool-create",
    packages=["dtool_create"],
    package_data={"dtool_create": ["templates/*"]},
    version=version,
    description="Dtool plugin for creating datasets",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@jic.ac.uk",
    url=url,
    install_requires=[
        "click",
        "dtoolcore>=3.6",
        "dtool_cli>=0.6.0",
        "dtool_symlink>=0.2.0",
        "dtool_http",
        "ruamel.yaml",
    ],
    entry_points={
        "dtool.cli": [
            "create=dtool_create.dataset:create",
            "name=dtool_create.dataset:name",
            "readme=dtool_create.dataset:readme",
            "add=dtool_create.dataset:add",
            "freeze=dtool_create.dataset:freeze",
            "copy=dtool_create.dataset:copy",
            "cp=dtool_create.dataset:cp",
            "publish=dtool_create.publish:publish",
        ],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
