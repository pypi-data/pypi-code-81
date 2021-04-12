#!/usr/bin/env python3
''' post_bitbucket_comment.py
Posts a comment to this project's bitbucket repository with 'build annotations' and the option
to encapsulate the inner-message with diff-markdown. To support the build annotations, this 
script requires many parameters (most provided as environment variables, some as CLI arguments).
'''
import requests
from textwrap import dedent

from buildtools import util, __version__, BuildToolsTemplate
from buildtools.util.markdown_comment_builder import BitbucketMarkdownComment
from buildtools.util import split_markdown


def create_comment(args, message):
    mc = BitbucketMarkdownComment()
    # When 'json_output' or 'json_file' is provided, that is a special case.
    if util.hasattr_nonempty_str(args, 'json_output') or util.hasattr_nonempty_str(args, 'json_file'):
        results = util.parse_ansible_json(message)
        mc.add_ansible_results(results)
    elif args.code_markdown:
        mc.add_code_markdown(message)
    elif args.diff_markdown:  # Should be mutex with code_markdown...
        mc.add_diff_markdown(message)
    else:
        mc.add_message(message)
    if args.clean_ansi_colors:
        mc.clean_ascii_codes()
    if args.tail:
        mc.trim_comment(args.tail)
    if args.build_annotation:
        mc.add_build_annotation(args.build_id, args.build_url, args.playbook_limit, args.build_status)
    return str(mc)


class PostBitbucketPRComment(BuildToolsTemplate):
    def __init__(self):
        cli_path = ['post', 'bitbucket', 'pr-comment']
        cli_descriptions = { 
            'post': 'Make an HTTP POST to a target.', 
            'bitbucket': 'Target Bitbucket.', 
            'build-status': 'Post a comment on a Pull Request.',
        }
        summary = dedent('''\
            Posts a comment to a Bitbucket pull request, with optional arguments for 'Jenkins build 
            annotations', indicating build status, encasing content in 'diff markdown', and more!
        ''')
        super().__init__(cli_path, cli_descriptions, summary)

    def run(self, args):
        # Get the core comment message, either from CLI or from file (and save it as 'comment')
        if args.comment_message:
            comment = create_comment(args, args.comment_message)
        elif args.json_output:
            comment = create_comment(args, args.json_output)
        else:
            try:
                if args.json_file:
                    comment = create_comment(args, util.readfile(args.json_file))
                elif args.comment_file:
                    comment = create_comment(args, util.readfile(args.comment_file))
            except FileNotFoundError as error:
                print(f"[ERROR] No such file: {args.comment_file}\n")
                exit(-1)

        if len(str(comment).strip()) == 0:
            raise ValueError("Some comment contents must be provided -- the comment to be sent was an empty string.")

        # Actually make the request
        try:
            # If the comment will exceed the max comment size, do fragmentation instead!
            if args.max_comment_size and len(str(comment)) > args.max_comment_size:
                comment_fragments = split_markdown(str(comment), args.max_comment_size)
                # Comments are in reverse chronological, so we should render the fragments in reverse.
                comment_fragments.reverse()
                # cp_i => "Comment Part Index"
                cp_i = len(comment_fragments)
                for comment_part in comment_fragments:
                    pagination_str = f'> Comment __{cp_i}__ of __{len(comment_fragments)}__.'
                    msg = f'{pagination_str}\n{comment_part}'
                    cp_i -= 1
                    response = requests.post(
                        f'{args.bitbucket_url}/rest/api/1.0/projects/{args.project}/repos/{args.repo}/pull-requests/{args.pull_request_id}/comments',
                        json={'text': msg},
                        auth=(args.user, args.password)
                        )
                    response.raise_for_status()
            else:
                response = requests.post(f'{args.bitbucket_url}/rest/api/1.0/projects/{args.project}/repos/{args.repo}/pull-requests/{args.pull_request_id}/comments',
                    json = {'text': comment if comment else '*Empty string provided.*'},
                    auth = (args.user, args.password)
                    )
                response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f"[ERROR] HTTP Error ({error.response.status_code}): {error.response.text}")
            exit(-1)

    def config_parser(self, parser):
        self.parser = parser
        parser.set_defaults(func=self.run)
        # Parse the 'comment type' with mutex logic -- don't allow user to provide more than one type of message from the provided options.
        c_parser = parser.add_mutually_exclusive_group(required=True)
        c_parser.add('--message', '-m', dest='comment_message',
            help='Provide the comment as a message on the command line.')
        c_parser.add('--file', '-f', dest='comment_file', 
            help='Provide the comment in a file.')
        c_parser.add('--json', '-j', dest='json_output', 
            help='''Provide ansible JSON output as a message on the command line (which will be parsed to extract build-status info).
                    NOTE: Additional 'formatting' arguments, such as '--code-markdown', are ignored when using json input.''')
        c_parser.add('--json-file', dest='json_file', 
            help='''Provide ansible JSON output as a file (which will be parsed to extract build-status info).
                    NOTE: Additional 'formatting' arguments, such as '--code-markdown', are ignored when using json input.''')
        # Core parsing bits.
        parser.add('--user', required=True, env_var='BITBUCKET_USER',
            help="Bitbucket user that will be used to authenticate to Bitbucket.")
        parser.add('--password', required=True, env_var='BITBUCKET_PASSWORD',
            help="Bitbucket password (or Personal Access Token) for the Bitbucket user.")
        parser.add('--project', required=True, env_var='BITBUCKET_PROJECT',
            help='The Bitbucket project key for the project where the pull request exists.')
        parser.add('--repo', required=True, env_var='BITBUCKET_REPO',
            help='The Bitbucket repository slug for the repository where the pull request exists.')
        parser.add('--pull-request-id', required=True, env_var='PR_ID',
            help='The ID of the Bitbucket pull request to be commented on.')
        # Group of arguments to do with formatting.
        formatting = parser.add_argument_group('formatting')
        formatting.add('--diff-markdown', action='store_true',
            help='Wrap the provided comment in diff markdown. E.g. ```diff\n\{comment\})\n```')
        formatting.add('--clean-ansi-colors', action='store_true',
            help='Clean/remove any ANSI Color codes that are in the provided message/file.')
        formatting.add('--code-markdown', action='store_true',
            help='Wrap the provided comment in code markdown. E.g. ```\n\{comment\})\n```')    
        formatting.add('--max-comment-size', type=int,
            help='Fragment the comment into based on the maximum comment size.')
        formatting.add('--tail', type=int,
            help='Only print the last `TAIL` lines of the provided message/file.')    
        # Build Annotation (aka 'ba') parser.
        ba_parser = formatting.add_argument_group('Build Annotation')
        ba_parser.add('--build-annotation', action='store_true',
            help='Provide a "build annotation" in the comment, with information about a Jenkins build.')
        ba_parser.add('--playbook-limit', env_var='PLAYBOOK_LIMIT',
            help='A string indicating the PLAYBOOK_LIMIT for this build. (Optional)')
        ba_parser.add('--build-id', env_var='BUILD_ID',
            help='Jenkins build ID. (Optional)')
        ba_parser.add('--build-url', env_var='BUILD_URL',
            help="Direct-URL to the Jenkins build. (Optional)")
        ba_parser.add('--build-status', choices=['SUCCESS', 'UNSTABLE', 'FAILURE', 'NOT_BUILD', 'ABORTED'],
            help='The build status to be reported in the comment. Accepts Jenkins build statuses.')
        return parser
