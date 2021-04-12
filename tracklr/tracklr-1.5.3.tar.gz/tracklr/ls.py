import logging

from cliff.lister import Lister
from tracklr import Tracklr


class Ls(Lister):

    log = logging.getLogger(__name__)

    tracklr = Tracklr()

    def take_action(self, parsed_args):
        """Generates report and logs total number of hours."""
        ts = self.tracklr.get_report(
            parsed_args.group,
            parsed_args.kalendar,
            parsed_args.date,
            parsed_args.include,
            parsed_args.exclude,
        )
        self.tracklr.banner(
            parsed_args.kalendar, parsed_args.title, parsed_args.subtitle
        )
        self.log.info("\nTotal hours: {}".format(self.tracklr.total_hours))
        self.log.info("Number of events: {}\n".format(len(ts)))
        if self.tracklr.total_sum > 0.0:
            self.log.info("Total sum: {}\n".format(self.tracklr.total_sum))

        if parsed_args.group is not None:
            return (("Date", "Summary", "Description", "Hours", "Group"), ts)
        return (("Date", "Summary", "Description", "Hours"), ts)

    def get_description(self):
        """Returns command description"""
        return "creates report"

    def get_parser(self, prog_name):
        """Gets default parser ie. this command does not add any new args"""
        parser = super(Ls, self).get_parser(prog_name)
        return self.tracklr.get_parser(parser)
