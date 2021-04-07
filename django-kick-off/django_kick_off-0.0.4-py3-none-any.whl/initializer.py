import os
import subprocess

from .cprint import cprint

from .conf import requirements


def run(project_name, venv_name):
    '''Create a virtual envioremnt and a django project'''

    # Create requirements.txt
    cprint.info('\nCreate "requirements.txt"... ')
    with open(f'requirements.txt', 'w') as requirements_file:
        requirements_file.write(requirements.get_requirements_as_string())
        requirements_file.close()
    cprint.success('[Success]')

    # Create virtual enviorment
    venv_name = f'venv{venv_name}'
    cprint.info(f'\nCreate the virtual enviorment "{venv_name}"... ')
    command = f'python3 -m venv {venv_name}'
    start = subprocess.run(command.split())
    if start.returncode == 0:
        cprint.success('[Success]')

    # Install modules from conf.REQUIREMENTS 
    folder = '/'.join(__file__.split('/')[:-1])
    command = f'source {venv_name}/bin/activate &&\
              python3 {folder}/scripts/installers.py {project_name}'
    subprocess.run(command, shell=True)
