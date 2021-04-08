from invoke import Config, Context
from odoo_manager.core import configs
from odoo_manager.core import paths as path_helpers


class BaseCommand(object):
    def __init__(self, options, depends_on_project=True, *args, **kwargs):
        """
        Initialize a BaseCommand object.

        :param {dict} options: Command line arguments passed in.
        :param {bool} depends_on_project:
            Determines if the command requires an odoo project to exist in the
            current directory. Examples of this are command like `run`, which
            require a project to actually run. Command like `new` do not need
            an existing project because it creates one.
        """
        self.options = options
        self.supported_commands = ()
        self.args = args
        self.kwargs = kwargs
        self.ctx = Context(Config())
        self._paths = None
        if depends_on_project:
            self._paths = path_helpers.Paths()
            configs.init()

    @property
    def paths(self):
        """
        Abstraction for accessing paths for the current project.

        This depends on the `get_paths` method for caching and retreival of the
        Paths object.

        :return {odoo_manager.core.paths.Paths}:
            Returns a Paths object containing references to paths in the current
            project.
        """
        return self.get_paths()

    def get_paths(self):
        """
        Get the Paths object for the current project, and cache the object.

        :return {odoo_manager.core.paths.Paths}:
            Returns a Paths object containing references to paths in the current
            project.
        """
        if not self._paths:
            self._paths = path_helpers.Paths()
        return self._paths

    def run(self):
        """
        Implements general functionality for the run command. Adds support for
        subcommand via the `supported_commands` tuple.

        Each command class should call super when inheriting the run method.

        ```
        class MyCommand(BaseCommand):
            def run(self):
                subcommand = super(MyCommand, self).run()
                if not subcommand:
                    pass  # Perform some logic
        ```

        :return {NoneType}:
        """
        if not self.supported_commands:
            raise NotImplementedError("All commands must implement the run() method.")

        for command in self.supported_commands:
            if command in self.options and self.options[command]:
                method = "run_{}".format(command)
                if not hasattr(self, method):
                    raise NotImplementedError("The function {} has not been implemented yet.".format(method))
                getattr(self, method)()
                return method

        return None
