from .base import BaseCommand


class Log(BaseCommand):
    """
    Represents the `odoo-manager log` command which tails the log file for the
    current project.
    """

    def run(self):
        """
        Runs the command. See the parent class for more details about how
        commands are organized and ran.

        :return {NoneType}:
        """
        grep = self.options.get("--grep")

        if grep:
            cmd = "tail -f {} | grep {}".format(self.paths.base(".container/log/odoo.log"), grep)
        else:
            cmd = "tail -f {}".format(self.paths.base(".container/log/odoo.log"))

        self.ctx.run(cmd, pty=True)
