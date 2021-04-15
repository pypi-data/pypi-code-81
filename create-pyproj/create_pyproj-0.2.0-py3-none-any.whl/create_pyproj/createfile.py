"""
Module Description.


"""
import logging
import shutil
from pathlib import Path

from .figlet import figletise
from .templater import writeTemplate

DIR = Path(__file__).parent.absolute()
logger = logging.getLogger(__name__)


def copyTemplates(projectname: str, package: bool = False, cli: bool = False):
    """
    [summary]

    [extended_summary]

    Args:
        projectname (str): [description]
        package (bool, optional): [description]. Defaults to False.
        cli (bool, optional): [description]. Defaults to False.
    """
    # Set the path for the main code repo
    PROJECT_ROOT = Path.cwd() / projectname
    PROJECT_PATH = PROJECT_ROOT / (projectname.replace('-', '_') if package else 'src')
    PROJECT_PATH.mkdir(exist_ok=True, parents=True)
    for file in (DIR / 'code').iterdir():
        if file.stem == '_config':
            shutil.copytree(file, PROJECT_PATH / file.stem)
        elif file.stem == 'test':
            shutil.copytree(file, PROJECT_ROOT / file.stem)
        elif file.stem == 'main.py':
            data = {'projectname': projectname, 'cli': cli, 'package': package}
            writeTemplate('main.py', PROJECT_PATH, data=data, templatepath=DIR / 'code')
        else:
            if not file.is_dir():
                shutil.copy(file, PROJECT_PATH / file.name)


def createFiles(projectname: str, package: bool = False, cli: bool = False):
    PROJECT_ROOT = Path.cwd() / projectname
    data = {
        'projectname': projectname,
        'figleted': figletise(projectname),
        'cli': cli,
        'package': package,
        'author': None,
        'author_email': None,
        'description': None,
        'hashes': '##'
    }

    standard = [
        '.env',
        '.flake8',
        '.gitignore',
        '.gitlab-ci.yml',
        '.style.yapf',
        'deploy.sh',
        'Pipfile',
        'README.md',
        'VERSION',
    ]

    for tmpl in standard:
        writeTemplate(tmpl, PROJECT_ROOT, data=data)

    pkg_tmpl = ['LICENSE', 'setup.cfg', 'pyproject.toml', 'MANIFEST.in']
    if package:
        for tmpl in pkg_tmpl:
            writeTemplate(tmpl, PROJECT_ROOT, data=data)
