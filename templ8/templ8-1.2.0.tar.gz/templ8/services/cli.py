from argparse import ArgumentParser

cli = ArgumentParser("templ8")
cli.add_argument("input", help="Input file path")


for (short, long, msg) in [
    ("-d", "--dry-run", "Don't generate anything"),
    ("-v", "--verbose", "Output verbose logs"),
    ("-c", "--schema", "Print schema"),
    ("-s", "--silent", "Don't output any logs"),
]:
    cli.add_argument(short, long, help=msg, action="store_true")
