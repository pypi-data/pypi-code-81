from .commands import in1_upsample


def main():
    args = parse_arguments()
    execute(args)


def execute(args):
    # Dictionary containing functions
    commands = {"upsample": in1_upsample}

    to_execute = commands[args.command]
    to_execute(args)


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser()

    commands_parser = parser.add_subparsers()
    commands_parser.required = True
    commands_parser.dest = "command"

    # Define available commands
    upsample_parser = commands_parser.add_parser("upsample")

    # Set up the subparsers
    upsample_parser.add_argument(
        "-api",
        "--api",
        required=True,
        type=str,
        help="Personal API key to gain access to in1",
    )
    upsample_parser.add_argument(
        "-s",
        "--source",
        required=True,
        type=str,
        help="Path name including file format of low resolution input to be upsampled",
    )
    upsample_parser.add_argument(
        "-r",
        "--result",
        required=True,
        type=str,
        help="Path name including .tif format for saving the upsampled source",
    )
    upsample_parser.add_argument(
        "-m",
        "--metrics",
        required=False,
        default=False,
        action="store_true",
        help="Specify for metric computation",
    )
    upsample_parser.add_argument(
        "-q",
        "--quiet",
        default=False,
        action="store_true",
        help="Specify for silencing detailed logging information during upsampling ",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
