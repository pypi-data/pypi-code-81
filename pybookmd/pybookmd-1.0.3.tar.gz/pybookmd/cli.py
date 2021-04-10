#!/usr/bin/env python
import os
from argparse import ArgumentParser

from generators import GENERATOR_BY_OUTPUT_FORMAT
from exceptions import OutputNotSupported


def get_parser():
	parser = ArgumentParser()
	parser.add_argument('build', default=True, action="store_true")
	parser.add_argument('--format', type=str, default="pdf")
	parser.add_argument(
		"--chapters_dir", type=str, required=False, default="chapters"
	)
	parser.add_argument(
		"--release_dir", type=str, required=False, default="release"
	)
	parser.add_argument(
		"--title", type=str, required=True, nargs="+"
	)
	return parser

def main():
	parser = get_parser()
	args = parser.parse_args()
	
	if args.build is True:
		output_format = args.format
		try:
			book_generator_class = GENERATOR_BY_OUTPUT_FORMAT[output_format]
		except KeyError:
			raise OutputNotSupported(f"Output format {output_format} is not supported at this time")
		else:
			generator = book_generator_class(args)
			generator.generate_book()
