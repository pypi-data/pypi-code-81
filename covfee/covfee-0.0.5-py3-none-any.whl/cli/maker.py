import os
import sys
import json

import click
from halo import Halo
from colorama import init as colorama_init, Fore
from flask import current_app as app

from covfee.server.orm import Project, User
from ..commands import start_dev, start_prod, open_covfee_admin, print_admin_url
from .covfee_folder import CovfeeFolder
from .utils import NPMPackage
from covfee.cli.validators.validation_errors import ValidationError
colorama_init()


def install_npm_packages_if_not_installed():
    cli_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cli')
    npm_package = NPMPackage(cli_path)
    if not npm_package.is_installed():
        npm_package.install()

    client_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'client')
    npm_package = NPMPackage(client_path)
    if not npm_package.is_installed():
        npm_package.install()


@click.command()
@click.option("--force", is_flag=True, help="Specify to overwrite existing databases.")
@click.option("--unsafe", is_flag=True, help="Disables authentication for the covfee instance.")
@click.option("--rms", is_flag=True, help="Re-makes the schemata for validation.")
@click.option("--dev", is_flag=True, help="Do not launch the browser.")
@click.argument("file_or_folder")
def make_db(force, unsafe, rms, dev, file_or_folder):
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
    with Halo(text='Validating covfee project files', spinner='dots') as spinner:
        try:
            project_folder.validate()
        except ValidationError as err:
            err.print_friendly()
            return spinner.fail('Error validating covfee files. Covfee maker aborted.')
        spinner.succeed('covfee project files are valid.')

    # ask user what to do if the database file exists
    if not project_folder.is_project():
        project_folder.init()
    project_folder.push_projects(interactive=True)

    # open covfee
    if dev:
        print_admin_url()
        start_dev()
    else:
        project_folder.link_bundles()
        open_covfee_admin()
        start_prod(unsafe=unsafe)


@click.command()
def make_user():
    if not os.path.exists(app.config['DATABASE_PATH']):
        cli_create_tables()
    username = input('Please enter username: ')
    password = input('Please enter password: ')
    user = User(username, password, ['admin'])
    db.session.add(user)
    db.session.commit()
    print('User has been created!')
