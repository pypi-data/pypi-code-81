from .base import BaseCommand
from odoo_manager.core import shell
from odoo_manager.core.git import redirect


class Stop(BaseCommand):
    """
    Represents the `odoo-manager stop` command which shuts down the running
    instances locally for the current odoo project.
    """

    def run(self):
        """
        Runs the command. See the parent class for more details about how
        commands are organized and ran.

        :return {NoneType}:
        """
        shell.out("Stopping containers...")
        self.ctx.run("docker-compose stop{}".format(redirect(verbose=False)))
        shell.out("Containers stopped.")
