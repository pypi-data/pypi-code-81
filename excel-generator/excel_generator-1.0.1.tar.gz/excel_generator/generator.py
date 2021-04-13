import click
import pyexcel as p

from .env_constants import EnvConstants
from .io_utils import IOUtils


class Generator:
    def __init__(self, json_file, excel_file):
        """
        The constructor. This class generates the Excel from the JSON file. The JSON file is list of dicts / dict
        """

        self.__in_file = json_file
        self.__out_file = excel_file

    def generate(self):

        if self.__in_file is None:
            raise Exception(
                "Input file was not detected in command and neither environment variable " + EnvConstants.IN_FILE + "\n" +
                "Please set option '--infile' in command line interface or set the " + EnvConstants.IN_FILE + " environment variable \n")

        if self.__out_file is None:
            raise Exception(
                "Output file was not detected in command and neither environment variable " + EnvConstants.OUT_FILE + "\n" +
                "Please set option '--outfile' in command line interface or set the " + EnvConstants.OUT_FILE + " environment variable \n")

        if "xls" not in self.__out_file and "xlsx" not in self.__out_file:
            raise Exception(f"Unsupported Excel file extension: {self.__out_file}\n")

        io_utils = IOUtils()
        try:
            messages = io_utils.read_dict_from_file(self.__in_file)
        except Exception as e:
            click.echo("Exception: {}".format(e.__str__()))
            return

        try:
            if not isinstance(messages, list) or isinstance(messages[0], str):
                click.echo(f"The input file {self.__in_file} is not list of dicts")
                return
        except Exception as e:
            click.echo("Exception: {}".format(e.__str__()))
            return

        p.isave_as(records=messages, dest_file_name=self.__out_file)
