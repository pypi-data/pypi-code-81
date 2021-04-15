"""CLI for executing AI quality analyses"""
import argparse

from aidkitcli.data_access.api import RESTApi


def main():
    """Get arguments and execute performance measurement."""
    argument_parser = argparse.ArgumentParser(
        prog="Analysis",
        usage="python " + __file__,
        description='Upload and list analyses.'
    )

    argument_parser.add_argument(
        '--file',
        help="We expect toml files satisfying a certain specification.",
        default=None,
        type=str
    )

    args = argument_parser.parse_args()

    api = RESTApi()

    if args.file is None:
        return api.get_status()
    else:
        return api.post_pipeline(toml_path=args.file)


if __name__ == "__main__":
    print(main())
