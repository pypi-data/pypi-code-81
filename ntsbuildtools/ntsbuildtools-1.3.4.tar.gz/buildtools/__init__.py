# Try to follow 'semmantic versioning' scheme, e.g. https://semver.org/
__version__ = '1.3.4'

from configargparse import ArgParser, Namespace
from typing import List, Dict


class BuildToolsTemplate:

    def __init__(self, cli_path: List[str] = None, cli_descriptions: Dict[str, str] = None, summary: str = None):
        self.cli_path = cli_path
        self.cli_descriptions = cli_descriptions
        self.summary = summary

    def run(self, args: Namespace) -> None:
        """Abstract method that SHOULD BE OVERWRITTEN. This method should provide the real functionality of this
        particular BuildTool.

        :param args: A simple object for storing 'argument' attributes.
        :type args: configargparse.Namespace
        :return: None
        """
        pass

    def config_parser(self, parser: ArgParser, parents: List[ArgParser] = None) -> None:
        """Abstract method that SHOULD BE OVERWRITTEN. This method should provide the real functionality of this
        particular BuildTool.

        :param parser: The Parser to be configured in the concrete implementation of this method.
        :type parser: configargparse.ArgParser
        :param parents: Parent parsers that should be
        :type parents: List[configargparse.ArgParser]
        :return: None
        """
        pass
