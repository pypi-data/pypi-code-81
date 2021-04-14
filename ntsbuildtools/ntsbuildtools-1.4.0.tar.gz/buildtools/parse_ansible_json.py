#!/usr/bin/env python3
""" parse_ansible_json.py
Parses Ansible JSON output and turns it into pretty markdown output.
"""
from textwrap import dedent
from typing import List

import configargparse
from mistletoe import Document

from . import BuildToolsTemplate
from buildtools import util
from buildtools.util.markdown_comment_builder import BitbucketMarkdownComment
from buildtools.util import split_markdown


class ParseAnsibleJson(BuildToolsTemplate):
    def __init__(self):
        cli_path = ['parse', 'ansible', 'json']
        cli_descriptions = {
            'parse': 'Parse some input (typically from a file).',
            'ansible': 'Parse Ansible output.',
            'json': 'Parse JSON formatted output.',
        }
        summary = dedent('Parses Ansible JSON output and turns it into pretty markdown output.')
        super().__init__(cli_path, cli_descriptions, summary)

    def _save_fragments_to_files(self, fragments, dst_file_base):
        # Calculate index and 'max_index_str_size' for use in formatting the output filename
        max_index_str_size = len(str(len(fragments) + 1))
        index = 0
        for fragment in fragments:
            index += 1
            fragment_filename = f'{dst_file_base}_{str(index).zfill(max_index_str_size)}.md'
            with open(fragment_filename, 'w') as dst_file:
                dst_file.write(str(fragment))

    def run(self, args):
        try:
            json_output = util.readfile(args.src)
            results = util.parse_ansible_json(json_output)
            markdown = BitbucketMarkdownComment()
            markdown.add_ansible_results(results)

            # Fragment the file only if the 'fragment_size' argument is provided (also, if 'less than 2 fragments' would
            # be created, skip the fragmentation handling).
            if args.fragment_size and args.fragment_size > 1:
                fragments = split_markdown(str(markdown), args.fragment_size)
                self._save_fragments_to_files(fragments, args.dst)
            else:
                with open(f'{args.dst}.md', 'w') as dst_file:
                    dst_file.write(str(markdown))
        except FileNotFoundError:
            print(f"[ERROR] No such file: {args.src}\n")
            exit(-1)

    def config_parser(self, parser: configargparse.ArgumentParser, parents: List[configargparse.ArgumentParser] = None):
        parser.set_defaults(func=self.run)
        parser.add_argument('src', help='''\
        Path to a Ansible JSON output file. This JSON file should be generated using the ["ansible.posix.json – Ansible 
        screen output as JSON" Callback Plugin.]
        (https://docs.ansible.com/ansible/latest/collections/ansible/posix/json_callback.html)
        ''')
        parser.add_argument('dst', help='''\
        Path to a file where the output should be saved. NOTE: If the file exists, it's contents will be overwritten.
        ''')
        parser.add_argument('--fragment-size', type=int, help='''\
        Fragment the output message into multiple chunks/files. This argument should be 'How many bytes per fragment.'
        ''')
        return parser
