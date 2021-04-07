""" Launch commands

These commands launch or build covfee and are supported for the typical use case.
"""
import os
from shutil import which
import sys
from colorama import init as colorama_init, Fore
import click

from flask import current_app as app
from flask.cli import FlaskGroup

from covfee.server.start import create_app
from ..covfee_folder import CovfeeFolder, ProjectExistsException
from halo.halo import Halo
from covfee.cli.validators.validation_errors import ValidationError
from covfee.cli.schemata import Schemata
from covfee.cli.utils import NPMPackage

colorama_init()


@click.group(cls=FlaskGroup, create_app=create_app, name='covfee')
def covfee_cli():
    pass


@covfee_cli.command()
def webpack():
    """
    Launches a webpack instance for use in dev mode
    """
    covfee_folder = CovfeeFolder(os.getcwd())
    if not covfee_folder.is_project():
        return print(Fore.RED+'Working directory is not a valid covfee project folder. '
                              'Did you run covfee-maker in the current folder?')

    covfee_folder.launch_webpack()


@covfee_cli.command()
@click.option('--unsafe', is_flag=True, help='Disables authentication.')
@click.option('--no-browser', is_flag=True, help='Disables launching of the web browser.')
def start(unsafe, no_browser):
    """
    Starts covfee in production (regular) mode
    """
    covfee_folder = CovfeeFolder(os.getcwd())
    if not covfee_folder.is_project():
        return print(Fore.RED+'Working directory is not a valid covfee project folder. Did you run'
                              ' covfee maker in the current folder?')

    covfee_folder.launch_prod(unsafe, launch_browser=not no_browser)


@covfee_cli.command(name='start-dev')
def start_dev():
    covfee_folder = CovfeeFolder(os.getcwd())
    if not covfee_folder.is_project():
        raise Exception('Working directory is not a valid covfee project folder.')

    covfee_folder.launch_dev()


@covfee_cli.command()
def build():
    """
    Builds the covfee bundle into the project folder
    """
    covfee_folder = CovfeeFolder(os.getcwd())
    if not covfee_folder.is_project():
        raise Exception(
            'Working directory is not a valid covfee project folder.')

    covfee_folder.build()


def print_admin_url():
    print(Fore.GREEN + f' * covfee is available at {app.config["ADMIN_URL"]}')


def open_covfee_admin():
    if which('xdg-open') is not None:
        os.system(f'xdg-open {app.config["ADMIN_URL"]}')
    elif sys.platform == 'darwin' and which('open') is not None:
        os.system(f'open {app.config["ADMIN_URL"]}')
    else:
        print_admin_url()


@covfee_cli.command(name="open")
def open_covfee():
    """
    Opens covfee (admin panel) in a browser window
    """
    open_covfee_admin()


def install_npm_packages_if_not_installed():
    cli_path = app.config['COVFEE_CLI_PATH']
    npm_package = NPMPackage(cli_path)
    if not npm_package.is_installed():
        npm_package.install()

    client_path = app.config['COVFEE_CLIENT_PATH']
    npm_package = NPMPackage(client_path)
    if not npm_package.is_installed():
        npm_package.install()


@covfee_cli.command()
@click.option("--force", is_flag=True, help="Specify to overwrite existing databases.")
@click.option("--unsafe", is_flag=True, help="Disables authentication for the covfee instance.")
@click.option("--rms", is_flag=True, help="Re-makes the schemata for validation.")
@click.option("--dev", is_flag=True, help="Start in dev mode.")
@click.option("--build", is_flag=True, help="Build the bundles (necessary for including custom tasks.)")
@click.option("--no-browser", is_flag=True, help="Do not launch in the browser")
@click.argument("file_or_folder")
def make(force, unsafe, rms, dev, build, no_browser, file_or_folder):
    install_npm_packages_if_not_installed()
    project_folder = CovfeeFolder(os.getcwd())

    # add the covfee files to the project
    with Halo(text='Adding .covfee.json files', spinner='dots') as spinner:
        covfee_files = project_folder.add_covfee_files(file_or_folder)

        if len(covfee_files) == 0:
            return spinner.fail(f'No valid covfee files found. Make sure that {file_or_folder}'
                                'points to a file or to a folder containing .covfee.json files.')

        spinner.succeed(f'{len(covfee_files)} covfee project files found.')

    # validate the covfee files
    if rms:
        Schemata().make()
    with Halo(text='Validating covfee project files', spinner='dots') as spinner:
        try:
            project_folder.validate(with_spinner=True)
        except ValidationError as err:
            err.print_friendly()
            return spinner.fail('Error validating covfee files. Covfee maker aborted.')
        spinner.succeed('all covfee project files are valid.')

    # init project folder if necessary
    if not project_folder.is_project():
        project_folder.init()
    try:
        project_folder.push_projects(force=force, interactive=True)
    except ProjectExistsException: 
        return print(' Add --force option to overwrite.')

    # open covfee
    if dev:
        project_folder.launch_dev()
    else:
        project_folder.launch_prod(unsafe=unsafe,
                                   build=build,
                                   launch_browser=not no_browser)


@covfee_cli.command()
def make_user():
    project_folder = CovfeeFolder(os.getcwd())
    if not project_folder.is_project():
        project_folder.init()

    # TODO: fix 
    # username = input('Please enter username: ')
    # password = input('Please enter password: ')
    # user = User(username, password, ['admin'])
    # db.session.add(user)
    # db.session.commit()
    # print('User has been created!')
