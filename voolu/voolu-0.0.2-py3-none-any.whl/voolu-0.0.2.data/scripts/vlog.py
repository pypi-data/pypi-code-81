import asyncio
import os
import click

from modules.auth import AuthService


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    if debug:
        click.echo('Debug mode is on')


async def do_login():
    auth = AuthService()
    token = await auth.login('a@b.com', 'hi')
    p = os.path.expanduser('~/.voolu/')
    if not os.path.exists(p):
        os.mkdir(p)
    with open(p + 'token', 'w') as f:
        f.write(token)

    print('Logged in and saved token at ~/.voolu/token')


async def create_account():
    auth = AuthService()
    token = await auth.create_account('a@b.com', 'hi')
    p = os.path.expanduser('~/.voolu/')
    if not os.path.exists(p):
        os.mkdir(p)
    with open(p + 'token', 'w') as f:
        f.write(token)

    print('Logged in and saved token at ~/.voolu/token')


@cli.command()
def login():
    asyncio.get_event_loop().run_until_complete(do_login())


@cli.command()
def create():
    asyncio.get_event_loop().run_until_complete(create_account())


if __name__ == '__main__':
    cli()
