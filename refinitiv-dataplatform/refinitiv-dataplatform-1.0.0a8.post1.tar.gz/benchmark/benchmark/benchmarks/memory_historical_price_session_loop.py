"""
Usage: python [--iter-count=<count>]

Options:
    -i count, --iter-count=<count>        Iteration count [default: 1].
    -h, --help                  Show this help message and exit
"""

import helper
import refinitiv.dataplatform as rdp

args = helper.docopt_parse_argv(__doc__)
iter_count = int(args.get('--iter-count'))


def main():
    session = helper.create_platform_session(rdp)
    for _ in range(iter_count):
        session.open()
        events = rdp.HistoricalPricing.get_events(
            universe='VOD.L',
            session=session,
        )
        df = events.data.df
        session.close()


main()
