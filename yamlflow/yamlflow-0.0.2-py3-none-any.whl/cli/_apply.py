import sys

import yaml
import click
import docker

from yamlflow.core.manifest import Manifest


@click.command()
@click.option('-f', '--file', 'f', required=True)
def apply(f):
    manifest = Manifest(f)
    data = manifest.data
