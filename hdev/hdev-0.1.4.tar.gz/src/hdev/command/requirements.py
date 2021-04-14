"""Sub-command of `hdev` to manipulate requirements files."""
from hdev.command.sub_command import SubCommand
from hdev.configuration import load_configuration
from hdev.requirements_file import compile_in_files, existing_in_files, upgrade_package


class Requirements(SubCommand):
    """Sub-command of `hdev` to manipulate requirements files."""

    name = "requirements"
    help = "Compiles .txt requirements file based on the existing .in files using pip-tools"

    def configure_parser(self, parser):
        """Set up arguments needed for the sub-command."""
        parser.add_argument(
            "upgrade",
            nargs="?",
            default=False,
            help="Upgrade or downgrade a package",
        )

        parser.add_argument(
            "--env",
            dest="env",
            help="""The environment containing the package to be upgraded.
            This should match the base name of one of the requirements/*.in
            files. Example:
            hdev requirements upgrade --env tests --package pytest.
            If no --env is given requirements.txt will be used.
            """,
        )

        parser.add_argument(
            "--package",
            dest="package",
            help="""The package to upgrade.
             `--package foo` will upgrade foo to the latest version.
            `--package foo==1.2.3 will upgrade or downgrade foo to version
            1.2.3.
            """,
        )

    def __call__(self, args):
        """Run the command.

        :param args: An ArgParser Namespace object
        """
        config = load_configuration(args.project_file)
        in_files = existing_in_files(config.get("tool.hdev.requirements.order", None))
        reformat = config.get("tool.hdev.requirements.reformat", None)

        if not in_files:
            print("No requirements files found")
            return

        if args.upgrade and not args.package:
            print("error: must provide a --package while using upgrade")
            return

        if args.upgrade:
            if not upgrade_package(in_files, args.package, args.env):
                return

        # Compile and reformat always
        requirements_files = compile_in_files(
            in_files,
            reformat,
        )

        print("Reformatted:")
        for requirement_file in requirements_files:
            print(f"\t{requirement_file}")
