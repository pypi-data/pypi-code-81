import argparse
import os
import sys
import exifread
import re

DATETIME_KEY = "Image DateTime"
DATETIME_PATTERN = re.compile(r"^(\d{4}):(\d{2}):(\d{2}) (\d{2}):(\d{2}):(\d{2})$")


def get_new_name(filename, date_matches):
    dirn = os.path.dirname(filename)
    # base = os.path.basename(filename)
    extension = os.path.splitext(filename)[1]

    year, month, date, hour, second, minute = date_matches.groups()
    suffix = 0

    while True:
        if suffix == 0:
            target = (
                f"{dirn}/{year}-{month}-{date}_{hour}:{second}:{minute}.{extension}"
            )
        else:
            target = f"{dirn}/{year}-{month}-{date}_{hour}:{second}:{minute}_{suffix}.{extension}"

        if not os.path.exists(target):
            return target

        suffix += 1


def cli():
    parser = argparse.ArgumentParser(
        description="Renames files in batch by regex.",
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

    for filename in args.files:
        f = open(filename, "rb")
        tags = exifread.process_file(f)

        if DATETIME_KEY not in tags:
            print(f"No datetime tag found for: {filename}", file=sys.stderr)
            continue

        match = DATETIME_PATTERN.match(tags[DATETIME_KEY])
        if match is None:
            print(
                f"Invalid datetime tag ({tags[DATETIME_KEY]!r}) found for: {filename}",
                file=sys.stderr,
            )

        # also search for raw CR2
        unextended = os.path.splitext(filename)[0]
        found_raw = None
        if os.path.exists(unextended + ".CR2"):
            found_raw = unextended + ".CR2"
        else:
            unextended_basename = os.path.basename(unextended)
            try_next = os.path.dirname(filename) + "/CR2/" + unextended_basename
            if os.path.exists(try_next):
                found_raw = try_next

        # for k, v in tags.items():
        #     print(f"{k} = {v}")
        # print(tags[DATETIME_KEY])
        # print(found_raw)

        if args.apply:
            os.rename(filename, get_new_name(filename, match))
            if found_raw is not None:
                os.rename(found_raw, get_new_name(found_raw, match))
        else:
            print(filename, "→", get_new_name(filename, match))
            if found_raw is not None:
                print(found_raw, "→", get_new_name(found_raw, match))


if __name__ == "__main__":
    cli()
