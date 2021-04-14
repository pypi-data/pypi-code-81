from setuptools import setup
import json
with open("/home/treebeard/Projects/lischon-vipextract/pypi_upload/config.json","r") as config:
    version = json.load(config)["version"]

setup(
    name = "wengmack_project",
    version = version,
    packages=['wengmack_project']
)