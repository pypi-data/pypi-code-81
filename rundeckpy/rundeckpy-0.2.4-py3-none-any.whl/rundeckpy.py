'''Rundeckpy CLI.'''

import click

@click.group()
def cli():
    '''Command group for cli'''

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--all', 'all_plugins', is_flag=True,
    help='Path is a folder with multiple plugin folders. Validate all.'
    )
def validate(path, all_plugins):
    '''Validate given plugin'''
    if all_plugins:
        click.echo(f'Need to iterate path {path} for plugins')
    else:
        click.echo('Need to validate plugin')
        print(f"Need to install {path}!")


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--all', 'all_plugins', is_flag=True,
    help='Path is a folder with multiple plugin folders. Install all.'
    )
def install(path, all_plugins):
    '''Install given plugin'''
    if all_plugins:
        click.echo(f'Need to iterate path {path}for plugins')
    else:
        click.echo('Need to install plugin')
        print(f"Need to install {path}!")


cli.add_command(validate)
cli.add_command(install)
