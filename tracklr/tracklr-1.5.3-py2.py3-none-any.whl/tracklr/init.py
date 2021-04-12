import os
import logging

from cliff.command import Command

from tracklr import Tracklr
from tracklr.pdf import Pdf


class Init(Command):

    log = logging.getLogger(__name__)

    tracklr = Tracklr()

    def take_action(self, parsed_args):
        """Creates ``tracklr.yml`` and ``pdf.html`` out of defaults in:

        * *user config* directory
        * *local* directory
        """
        actions = {"config": self.init_config, "template": self.init_template}
        action = parsed_args.action
        self.tracklr.banner(
            parsed_args.kalendar, parsed_args.title, parsed_args.subtitle
        )
        self.log.info("\nInitializing {}\n".format(action))
        actions[action](parsed_args)

    def init_config(self, parsed_args):
        """Creates local or global config.
        """
        self.create_file_type(
            parsed_args, self.tracklr.config_file, self.tracklr.__config__
        )

    def init_template(self, parsed_args):
        """Creates local or global template.
        """
        self.create_file_type(
            parsed_args, self.tracklr.pdf_template_file, Pdf.__template__
        )

    def create_file_type(self, parsed_args, file_name, file_content):
        """Handles creation of given file.
        """
        if parsed_args.user_config_dir:
            self.log.info("user config dir")
            self.create_file(
                parsed_args, self.tracklr.global_path, file_name, file_content
            )
        else:
            self.log.info("current dir")
            self.create_file(
                parsed_args, self.tracklr.local_path, file_name, file_content
            )

    def create_file(self, parsed_args, file_path, file_name, file_content):
        """Creates desired file at given path with given content.
        """
        f = os.path.join(file_path, file_name)
        if os.path.isfile(f):
            self.log.info(
                "file {} already exists. " "nothing to do here...".format(f)
            )
        else:
            if not os.path.exists(file_path):
                self.log.info(
                    "directory {} does not exist. "
                    "creating...".format(file_path)
                )
                os.makedirs(file_path)
            self.log.info("file {} does not exist. " "creating...".format(f))
            fd = open(f, "w")
            fd.write(file_content)
            fd.close()

    def get_description(self):
        """initializes ``tracklr.yml`` and ``pdf.html``
        """
        return "initializes tracklr.yml and pdf.html"

    def get_parser(self, prog_name):
        """Adds two arguments:

        * ``action`` - inits either ``config`` or ``template``
        * ``--user-config-dir`` - use this option to generate file in
          *user config* directory instead of current directory
        """
        parser = super(Init, self).get_parser(prog_name)
        parser.add_argument(
            "action",
            type=str,
            choices=["config", "template"],
            help="init config/template in the current directory",
        )
        parser.add_argument(
            "--user-config-dir",
            action="store_true",
            help="create config/template in {} "
            "instead of the current directory".format(self.tracklr.global_path),
        )
        return self.tracklr.get_base_parser(parser)
