import logging

from cliff.command import Command
from tracklr import Tracklr


class Info(Command):

    log = logging.getLogger(__name__)

    tracklr = Tracklr()

    def take_action(self, parsed_args):
        """Display information about the current instance.
        """
        self.tracklr.banner(
            parsed_args.kalendar, parsed_args.title, parsed_args.subtitle
        )

        self.log.info("\nCalendars:\n")

        calendars = []
        for cal in self.tracklr.calendars:
            self.log.info(
                "* {} | {} | {}\n".format(
                    cal,
                    self.tracklr.get_title(cal, parsed_args.title),
                    self.tracklr.calendars[cal]["location"],
                )
            )

    def get_description(self):
        return "display info about the current instance"

    def get_parser(self, prog_name):
        parser = super(Info, self).get_parser(prog_name)
        return self.tracklr.get_base_parser(parser)
