"""Provides a parent class for convenient sub-commands."""


class SubCommand:
    """A sub-command for attaching to an argparser parser object."""

    name = None
    """The name to use when added as a sub-command."""

    help = None
    """The help to use when added as a sub-command."""

    def add_to_parser(self, sub_parsers):
        """Add this command to the provided sub-parser object.

        This provides default behavior which will register this command with
        the name and help specified in the class and also set the object
        as `handler` on the returned args object.

        :param sub_parsers: The return value of calling `add_subparsers()` on
            an ArgParser parser object
        """
        parser = sub_parsers.add_parser(name=self.name, help=self.help)
        parser.set_defaults(handler=self)
        self.configure_parser(parser)

    def configure_parser(self, parser):
        """Set up arguments needed for the sub-command."""

    def __call__(self, args):
        """Run the command.

        :param args: An ArgParser Namespace object
        """
