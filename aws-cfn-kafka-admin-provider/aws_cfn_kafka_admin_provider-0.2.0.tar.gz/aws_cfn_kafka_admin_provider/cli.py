#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@ews-network.net>

"""Console script for aws_cfn_kafka_admin_provider."""

import argparse
import sys

from aws_cfn_kafka_admin_provider.aws_cfn_kafka_admin_provider import KafkaStack


def main():
    """Console script for aws_cfn_kafka_admin_provider."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file-path",
        required=True,
        dest="file_path",
        help="Path to the kafka definition file",
    )
    parser.add_argument(
        "--override-file-path",
        required=False,
        dest="override_path",
        help="Override file path to the kafka definition file",
        default=None,
    )
    parser.add_argument(
        "-o", "--output-file", dest="output_file", help="Path to file output"
    )
    parser.add_argument(
        "--format",
        dest="format",
        help="Template format",
        default="json",
        choices=["json", "yaml"],
    )
    parser.add_argument("_", nargs="*")
    args = parser.parse_args()

    stack = KafkaStack(args.file_path, args.override_path)
    stack.render_topics()
    stack.render_acls()
    if args.output_file:
        with open(args.output_file, "w") as output_fd:
            if args.format == "yaml":
                output_fd.write(stack.template.to_yaml())
            else:
                output_fd.write(stack.template.to_json())
    else:
        if args.format == "yaml":
            print(stack.template.to_yaml())
        else:
            print(stack.template.to_json())
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
