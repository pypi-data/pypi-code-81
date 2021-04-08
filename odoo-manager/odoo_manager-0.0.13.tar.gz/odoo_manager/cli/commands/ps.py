from .base import BaseCommand
from odoo_manager.core import shell


class Ps(BaseCommand):
    """
    Represents the `odoo-manager ps` command which lists the current running or
    non-running containers.
    """

    def __init__(self, options, *args, **kwargs):
        """
        Inheriting the parent class for initializes command to defined that this
        command does not depend on a project.

        See the parent `__init__` method for parameters.
        """
        super(Ps, self).__init__(options, depends_on_project=False, *args, **kwargs)

    def run(self):
        """
        Runs the command. See the parent class for more details about how
        commands are organized and ran.

        :return {NoneType}:
        """
        if not self.options.get("--all", False):
            self.ctx.run("docker-compose ps")
        else:
            self.ctx.run("docker ps")
