"""
Module Description.


"""
import logging
import shutil
from pathlib import Path

from .figlet import figletise

DIR = Path(__file__).parent.absolute()
CWD = Path.cwd()
logger = logging.getLogger(__name__)


def creatReadMe(projectname: str) -> None:
    """
    Create a template readme file.

    Args:
        projectname (str): The project name.
    """
    with open(DIR / 'templates/readme.md', 'r') as f:
        template = f.read()

    logger.debug('Hello')

    template = template.replace('FIGLET_PROJECT_NAME', figletise(projectname))
    template = template.replace(r'PROJECT_NAME', projectname.capitalize())

    target = CWD / projectname
    target.mkdir(exist_ok=True, parents=True)

    with open(target / 'README.md', 'w') as f:
        f.write(template)


def copyTemplates(projectname):
    for file in (DIR / 'templates').iterdir():
        if file.suffix == '.tmpl':
            target = CWD / projectname / file.stem
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(file, target)
        if file.stem == 'src':
            shutil.copytree(file, CWD / projectname / file.stem)
