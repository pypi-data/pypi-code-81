from .base import BaseCommand
from invoke import UnexpectedExit
from odoo_manager.core import configs, shell, validation
from odoo_manager.core.git import redirect


class Run(BaseCommand):
    """
    Represents the `odoo-manager run` command which runs the current odoo
    project locally.
    """

    def run(self):
        """
        Runs the command. See the parent class for more details about how
        commands are organized and ran.

        :return {NoneType}:
        """
        validation.check_env(configs.config, ["PIP_EXE", "ODOO_EXE", "LOCAL_PORT"])

        if self.options.get("--rebuild", False):
            # Tasks.build(ctx, update=update, verbose=verbose)
            shell.out("Rebuild is not supported yet.", color="yellow")
            exit(0)

        args = self.options.get("--args", "")
        if (
            args
            and ("-i" in args or "--install" in args or "-u" in args or "--upgrade" in args)
            and ("-d" not in args and "--database" not in args)
        ):
            shell.out("Make sure you include the -d flag when trying to upgrade or install modules.", color="yellow")
            exit(1)

        compose = self.options.get("--compose", False) or "docker-compose.yml"
        verbose = self.options.get("--verbose", False)
        detach = self.options.get("--detach", False)

        # We are going to rewrite args every time no matter if it was passed
        # in or not. We don't want to run into a situation where a user uses
        # args once, and then has the same flags passed in over and over since
        # the odoo.env file will be written.
        #
        # If the user passes in args, then the next time does not, we should
        # assume we need to write an empty string to the odoo.env.
        if configs.config.has_option("options", "ODOO_FLAGS"):
            try:
                self.ctx.run("sed -i '' '/^ODOO_FLAGS/d' {}{}".format(configs.standard_env_path, redirect(verbose)))
            except:
                self.ctx.run("sed -i '/^ODOO_FLAGS/d' {}{}".format(configs.standard_env_path, redirect(verbose)))
        if configs.odoo_env_config.has_option("options", "ODOO_FLAGS"):
            try:
                self.ctx.run("sed -i '' '/^ODOO_FLAGS/d' {}{}".format(configs.odoo_env_path, redirect(verbose)))
            except:
                self.ctx.run("sed -i '/^ODOO_FLAGS/d' {}{}".format(configs.odoo_env_path, redirect(verbose)))

        shell.out("Running project...")
        if not verbose:
            shell.out(
                "You are not running in verbose mode, so container logs/output will not appear here. Tail "
                "logs or run this command with the --verbose flag to see output. It may take a minute for "
                "all containers to fully start.",
                color="yellow",
            )
        shell.out("  detach?: {}".format(detach), color="lightgrey")
        shell.out("  args:    {}".format(args or "None"), color="lightgrey")
        shell.out("  port:    {}".format(configs.config.get("options", "LOCAL_PORT")), color="lightgrey")
        shell.out(
            "  url:     http://localhost:{}".format(configs.config.get("options", "LOCAL_PORT")), color="lightgrey"
        )

        try:
            cmd = "docker-compose -f {} up {}{}".format(compose, "-d" if detach else "", redirect(verbose))
            if self.options.get("--show-cmd", False):
                shell.out(cmd)

            self.ctx.run("echo 'ODOO_FLAGS={}' >> {}".format(args or "", configs.odoo_env_path))
            self.ctx.run(cmd)
        except UnexpectedExit as e:
            # Handle the unexpected exit while trying to run docker-compose up.
            # There are a couple of scenarios. We only care about an error code
            # "1" coming back which means that our program died on it's own. We
            # do not care about the user stopping the command with a ctrl-c
            # input.
            if e.result.exited == 1:
                shell.out(
                    "There was a problem running docker-compose.{}".format(
                        " Try again with --verbose to see the error information." if not verbose else ""
                    ),
                    color="pink",
                )
