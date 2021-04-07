# Module imports
from .normalizer import project_to_venv
from .initializer import run


def main(args):
    argv_length = len(args)
    if argv_length == 2:
        project_name = args[1]
        venv_name = project_to_venv(project_name)
    elif argv_length > 2:
        project_name = args[1]
        venv_name = args[2]
    else:
        project_name = 'mysite'
        venv_name = 'MySite'
    run(project_name, venv_name)
