import logging

from cliff.lister import Lister
from tracklr import Tracklr


class Group(Lister):

    log = logging.getLogger(__name__)

    tracklr = Tracklr()

    def take_action(self, parsed_args):
        """Generates report and logs total number of hours.
        """
        if parsed_args.group is None:
            group = "#"
        else:
            group = parsed_args.group

        ts = self.tracklr.get_matches(
            group,
            parsed_args.kalendar,
            parsed_args.date,
            parsed_args.include,
            parsed_args.exclude,
        )

        self.tracklr.banner(
            parsed_args.kalendar, parsed_args.title, parsed_args.subtitle
        )

        self.log.info("\nTotal hours: {}\n".format(self.tracklr.total_hours))

        return (("Group", "Hours"), ts)

    def get_description(self):
        return "creates group report"

    def get_parser(self, prog_name):
        parser = super(Group, self).get_parser(prog_name)
        return self.tracklr.get_parser(parser)
