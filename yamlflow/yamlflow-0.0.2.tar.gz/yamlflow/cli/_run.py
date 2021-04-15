


@click.command()
@click.option('-f', '--file', 'f', required=True)
def apply(f):
    manifest = Manifest(f)
    data = manifest.data