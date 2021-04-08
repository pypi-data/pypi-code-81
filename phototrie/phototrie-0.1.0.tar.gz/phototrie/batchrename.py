import os
import re
import sys
import argparse
from typing import List


def cli():
    parser = argparse.ArgumentParser(
        description="Renames files in batch by regex.",
    )

    parser.add_argument(
        "pattern",
        type=str,
        help="regex pattern to be replaced (on the basename)",
    )

    parser.add_argument(
        "replacement",
        type=str,
        help="replacement pattern",
    )

    parser.add_argument(
        "files",
        type=str,
        nargs="*",
        help="list of files to rename",
    )

    parser.add_argument(
        "--apply",
        "-y",
        action="store_true",
        help="actually apply the replacement (dry-run if omitted)",
    )

    args = parser.parse_args(sys.argv[1:])

    pattern = re.compile(args.pattern)

    for filename in sys.argv[3:]:
        base = os.path.basename(filename)
        dirn = os.path.dirname(filename)
        new_base = pattern.sub(args.replacement, base)

        if base == new_base:
            print(f"no match: {filename}", file=sys.stderr)
            continue

        target_filename = dirn + "/" + new_base

        if os.path.exists(target_filename):
            print(f"target exists: {target_filename}", file=sys.stderr)
            continue

        if args.apply:
            os.rename(filename, target_filename)
        else:
            print(f"{filename} → {target_filename}", file=sys.stderr)


if __name__ == "__main__":
    cli()
