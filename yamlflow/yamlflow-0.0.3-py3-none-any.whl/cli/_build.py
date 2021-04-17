import click
import docker

from yamlflow.manifest import Manifest

client = docker.from_env()


@click.command()
@click.option('-f', '--file', 'f', required=True)
def build(f):
    """Given a manifest file, create docker image"""
    manifest = Manifest(f)
    build_info = manifest.build_info()
    click.echo(
        click.style(
            f"""
            Building image ....
            Name:    {build_info["tag"]}
            Backend: {build_info["buildargs"]["backend"]}
            """,
            fg="blue"
        )
    )
    client.images.build(**build_info)
