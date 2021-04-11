from os.path import join, dirname, expanduser
from textx import metamodel_from_file

GRAMMAR_FILE = 'grammar.tx';


def retrieve_commands(file_path):
    this_folder = dirname(__file__)

    meta_model = metamodel_from_file(join(this_folder, GRAMMAR_FILE))
    commands_file = open(expanduser(file_path))
    commands = commands_file.read()

    command_model = meta_model.model_from_str(commands)

    return command_model.commands
