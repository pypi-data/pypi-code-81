import os
from .base import BaseCommand
from odoo_manager.core import configs, shell, validation
from odoo_manager.core.git import git_clone, redirect


class Build(BaseCommand):
    def __init__(self, options, *args, **kwargs):
        """
        Inheriting the parent class for initializes command to defined that this
        command does not depend on a project.

        See the parent `__init__` method for parameters.
        """
        super(Build, self).__init__(options, depends_on_project=False, *args, **kwargs)

    # TODO: odoo-manager build[--no-cache][--no-depends][--no-setup][--pull][--verbose]
    def run(self):
        """
        This method builds your project.  It installs requirements.txt, builds
        the docker image, makes required directories and installs odoo.

        :return {NoneType}:
        """
        nocache = self.options.get("--no-cache", False)
        nodepends = self.options.get("--no-depends", False)
        nosetup = self.options.get("--no-setup", False)
        pull = self.options.get("--pull", False)
        verbose = self.options.get("--verbose", False)
        paths = self.get_paths()
        config = configs.load_standard_config(paths.base(".env"))
        user = ""
        password = ""

        validation.check_env(config, ["ODOO_VERSION", "USE_ENTERPRISE", "GIT_DEPTH"])

        shell.out("Running build process...")

        shell.out("  *Install pip3 requirements...")

        self.ctx.run("pip3 install {} --quiet -r {}".format("--user", paths.base("requirements.txt")))

        shell.out("  *Building docker image with docker-compose build...")

        self.ctx.run(
            "docker-compose build{}{}{}".format(
                " --pull" if pull else "", " --no-cache" if nocache else "", redirect(verbose)
            )
        )

        shell.out("  *Making directories...")

        if not os.path.isdir(paths.base(".container/testresults")):
            self.ctx.run("mkdir -p {}".format(paths.base(".container/testresults")))

        odoo_version = config.get("options", "ODOO_VERSION")
        use_enterprise = config.get("options", "USE_ENTERPRISE") != "0"
        depth = config.get("options", "GIT_DEPTH")

        shell.out("  *Installing odoo source...")
        shell.out("      odoo version:      {}".format(odoo_version), color="lightgrey")
        shell.out("      using enterprise?: {}".format(use_enterprise), color="lightgrey")
        shell.out("      repo depth:        {}".format(depth), color="lightgrey")
        shell.out("", color="lightgrey")

        if not os.path.isdir(paths.base(".container/core/addons")):
            if os.path.isdir(paths.base(".container/core")):
                shell.out("      Cleaning up existing core folder...")
                self.ctx.run("rm -rf {}".format(paths.base(".container/core")))
            shell.out("      Cloning down repo from github.com/odoo/odoo...")
            git_clone(
                self.ctx,
                "https://github.com/odoo/odoo",
                odoo_version,
                "odoo/odoo",
                output=paths.base(".container/core"),
                depth=depth,
            )

        us_locale_path = paths.base(".container/core/addons/web/static/lib/moment/locale/en-us.js")
        ca_locale_path = paths.base(".container/core/addons/web/static/lib/moment/locale/en-ca.js")

        if not os.path.isfile(us_locale_path) and os.path.isfile(ca_locale_path):
            shell.out("  *Cleaning up moment locales...")
            self.ctx.run("cp {} {}".format(ca_locale_path, us_locale_path))

        if use_enterprise:
            if not os.path.isdir(paths.base(".container/enterprise/account_reports")):
                if os.path.isdir(paths.base(".container/enterprise")):
                    shell.out("      Cleaning up existing enterprise folder...")
                    self.ctx.run("rm -rf {}".format(paths.base(".container/enterprise")))
                shell.out("      Cloning down repo from github.com/odoo/enterprise...")
                git_clone(
                    self.ctx,
                    "https://github.com/odoo/enterprise",
                    odoo_version,
                    "odoo/enterprise",
                    output=paths.base(".container/enterprise"),
                    depth=depth,
                    user=user,
                    password=password,
                )
