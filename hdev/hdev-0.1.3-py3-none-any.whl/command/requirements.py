"""Sub-command of `hdev` to manipulate requirements files."""
from hdev.command.sub_command import SubCommand
from hdev.configuration import load_configuration
from hdev.requirements_file import compile_in_files


class Requirements(SubCommand):
    """Sub-command of `hdev` to manipulate requirements files."""

    name = "requirements"
    help = "Compiles .txt requirements file based on the existing .in files using pip-tools"

    def __call__(self, args):
        """Run the command.

        :param args: An ArgParser Namespace object
        """
        config = load_configuration(args.project_file)

        requirements_files = compile_in_files(
            reformat=config.get("tool.hdev.requirements.reformat", None),
            in_files=config.get("tool.hdev.requirements.order", None),
        )

        if not requirements_files:
            print("No requirements files found")
        else:
            print("Reformatted:")
            for requirement_file in requirements_files:
                print(f"\t{requirement_file}")
