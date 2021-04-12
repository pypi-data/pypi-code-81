#!/usr/bin/env python3
import sys

import configargparse
import argcomplete
from anytree import NodeMixin

from buildtools.post_bitbucket_build_status import PostBitbucketBuildStatus
from buildtools.post_bitbucket_comment import PostBitbucketPRComment
from buildtools.post_teams_actionable_message import PostTeamsCard
from buildtools.parse_ansible_json import ParseAnsibleJson
from buildtools import __version__, BuildToolsTemplate


class BTNode(NodeMixin):
    def __init__(self, cli_term, parser=None, subparsers=None, buildtool_ext=None, parent=None, children=None):
        self.cli_term = cli_term
        self.parser = parser
        self.subparsers = subparsers
        self.buildtool_ext = buildtool_ext
        self.parent = parent
        if children:
            self.children = children

class BTNodeSubparsers(BTNode):
    def __init__(self, cli_term, subparsers=None, parent=None, children=None):
        super().__init__(cli_term, parser=None, subparsers=subparsers, buildtool_ext=None, parent=parent, children=children)

class BTNodeParser(BTNode):
    def __init__(self, cli_term, parser=None, buildtool_ext=None, parent=None, children=None):
        super().__init__(cli_term, parser=parser, subparsers=None, buildtool_ext=buildtool_ext, parent=parent, children=children)

class BuildTools:
    def __init__(self):
        self.base_parser = configargparse.ArgumentParser(add_help=False)
        self.base_parser.add('--version', action='version', version=f"BuildTools Version: v{__version__}")
        self.base_parser.add('--bitbucket-url', env_var='BITBUCKET_URL', help="URL for Bitbucket.")
        self.parser = configargparse.ArgumentParser(description="Tools that help with Jenkins build scripts.", parents=[self.base_parser])

        self.subparsers = self.parser.add_subparsers(dest='act0')
        self.subparsers.required = True
        # The 'root' is not a 'leaf' of the tree, so it is a 'inner-node' -- AKA BTNodeSubparsers
        self.root = BTNodeSubparsers('root', subparsers=self.subparsers)

    def _add_leaf(self, buildtool_ext, parent):
        return self._insert_subparser(buildtool_ext, parent)

    def _insert_subparser(self, buildtool_ext, parent):
        """
        Internal method. Assumes that self.root contains the tree with all subparsers needed
        to support the buildtool_ext.

        Args:
            buildtool_ext (BuildToolsTemplate): A BuildToolsTemplate extension.
            parent (BTNode): The node that is the parent of this subparser. 
        """
        cli_term = buildtool_ext.cli_path[-1]
        # Create the leaf BTNode with the subparser
        parser = parent.subparsers.add_parser(cli_term, help=buildtool_ext.summary, parents=[self.base_parser])
        return BTNodeParser(cli_term, parser=parser, buildtool_ext=buildtool_ext, parent=parent)

    def _add_inner(self, buildtool_ext, index, parent):
        return self._insert_subparsers(buildtool_ext, index, parent)

    def _insert_subparsers(self, buildtool_ext, index, parent):
        cli_term = buildtool_ext.cli_path[index]
        subparsers = parent.subparsers.add_parser(cli_term, help=buildtool_ext.cli_descriptions[cli_term]).add_subparsers(dest=f'act{index}')
        subparsers.required = True
        return BTNodeSubparsers(cli_term, subparsers=subparsers, parent=parent)

    def register(self, buildtool_ext):
        # Insert 'subparsers' as needed, if they don't exist (think `mkdir -p` behavior)
        # 'iterator' variable used to 'walk' a path down the tree (from root to leaf)
        current = self.root
        for index in range(len(buildtool_ext.cli_path) - 1):
            # How to get 'current subparser(s)' if current.children
            # Determine if the subparser is already in the tree (based on cli_path of buildtool_ext (AKA cli_term))
            cli_term = buildtool_ext.cli_path[index]
            children_cli_terms = {_.cli_term: _ for _ in current.children}
            if cli_term in children_cli_terms.keys():
                current = children_cli_terms[cli_term]
                continue
            current = self._add_inner(buildtool_ext, index, parent=current)
        # 3. In general: create the 'leaf' node -- the actual "Parser"
        # TODO Handle exception if this subparser already exists!
        leaf_node = self._add_leaf(buildtool_ext, parent=current)
        buildtool_ext.config_parser(leaf_node.parser)

    def run(self, args):
        # Enable tab completion
        argcomplete.autocomplete(self.parser)
        # Actually run the parser!
        args = self.parser.parse_args(args)
        # We have 'required=true' for subparsers, so we are sure that the default 'func' is sure to be 'set' in args
        args.func(args)

def main(args):
    bt = BuildTools()
    bt.register(PostBitbucketBuildStatus())
    bt.register(PostBitbucketPRComment())
    bt.register(PostTeamsCard())
    bt.register(ParseAnsibleJson())
    #bt.register(PostBitbucketPR())
    bt.run(args)

if __name__ == '__main__':
    main(sys.argv[1:])