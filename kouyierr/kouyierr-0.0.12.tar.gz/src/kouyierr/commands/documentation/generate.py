from shutil import which
import logging
import os
import time

import click
import pypandoc
import texlivemetadata
from rich import print as rprint

from kouyierr.commands import global_options
from kouyierr.utils.helper import Helper


class Generator:
    def __init__(self, helper: Helper, markdown: str, output_file: str, template: str, output_dir: str):
        logging.basicConfig(format='%(message)s')
        logging.getLogger(__package__).setLevel(logging.INFO)
        self._logger = logging.getLogger(__name__)
        self._helper = helper
        self._markdown = markdown
        self._output_dir = output_dir
        self._output_file = output_file
        self._template = template

    def _check_tex_libraries(self) -> bool:
        # pandoc is necessary for document generation
        if which('pandoc') is None:
            self._logger.error('No executable "pandoc" found.')
            return False
        # tlmgr is necessary for TeX library
        if which('tlmgr') is None:
            self._logger.error('No executable "tlmgr" found.')
            return False
        mandatory_packages = ('sectsty', 'fvextra', 'wrapfig', 'titling', 'everypage', 'background')
        for package in mandatory_packages:
            if not texlivemetadata.get_package_info(package)['installed']:
                self._logger.error('Mandatory packages missing, please run "tlmgr install" with: %s',
                                   mandatory_packages)
                return False
        return True

    def execute(self):
        start_time = time.time()
        rprint("[italic yellow]Checking for requirements (can be a bit long)[/italic yellow] ...")
        # before executing, we need to check for local requirements
        if not self._check_tex_libraries():
            self._logger.error('Missing requirements, aborting...')
            exit(1)
        elapsed_time = round(time.time() - start_time, 2)
        rprint(f"[blue]Everything is installed, awesomeness can go on, checked in {elapsed_time}s[/blue] :thumbs_up:")

        start_time = time.time()
        try:
            pypandoc.convert_file(os.path.abspath(self._markdown), 'pdf',
                                  outputfile=os.path.abspath(self._output_file),
                                  extra_args=['--pdf-engine=xelatex', f'--template={self._template}'])
        except RuntimeError as error:
            self._logger.error('Error converting %s: %s', self._markdown, error)
            exit(1)
        elapsed_time = round(time.time() - start_time, 2)
        rprint(f"[bold green]Documentation generation complete[/bold green] in {elapsed_time}s :thumbs_up:")


@click.command(help='Generate a new documentation from Markdown file based on TeX template')
@global_options
@click.option('--markdown', required=True, type=str,
              help='Markdown file path to use for documentation')
@click.option('--output-file', required=False, type=str, default='output.pdf',
              help='Output PDF filename, default=output.pdf')
@click.option('--template', required=False, type=str, default='template.tex',
              help='TeX template file path')
def generate(markdown: str, output_file: str, template: str, output_dir: str):
    ''' Generate a new documentation from Markdown file based on TeX template '''
    Generator(Helper(), markdown, output_file, template, output_dir).execute()
