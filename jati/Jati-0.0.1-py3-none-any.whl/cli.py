import sys
import click

@click.group()
def main():
    click.echo('Debug mode is %s' % ('on' if True else 'off'))

@main.command('generate:controller')
def generate_ctrl():
    click.echo('Generating controller')

@main.command()
def start():
    click.echo('Starting')
# def main():
#     print(sys.argv)