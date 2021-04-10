import asyncio
import os
import click

from modules.auth import AuthService


async def main():
    auth = AuthService()
    token = await auth.login('a@b.com', 'hi')
    p = os.path.expanduser('~/.voolu/')
    if not os.path.exists(p):
        os.mkdir(p)
    with open(p + 'token', 'w') as f:
        f.write(token)

    print('Logged in and saved token at ~/.voolu/token')


@click.command()
def cli():
    asyncio.get_event_loop().run_until_complete(main())


if __name__ == '__main__':
    cli()
