#!/usr/bin/env python3
''' post_teams_actionable_message.py
Posts some type of "build message" to a Teams Channel.
'''
import os
import sys
import requests
import configargparse
from textwrap import dedent, indent

from buildtools import __version__, BuildToolsTemplate
from buildtools.util.teams_cards import TeamsCardFactory, TeamsMessageTypes
from buildtools.util.teams_card_builder import TeamsCardTemplateError
    
def infer_missing_arguments(expected, provided):
    missing = expected - provided
    missing_args = [f"--{arg.replace('_', '-')}" for arg in missing]
    return ', '.join(missing_args)

def _raise_for_http_413(response):
    # Teams does not actually set the status_code for HTTP 413... so we parse the response.text to handle for it
    if 'HTTP error 413' in response.text:
        response.status_code = 413
        response.raise_for_status()

class PostTeamsCard(BuildToolsTemplate):
    def __init__(self):
        cli_path = ['post', 'teams', 'card']
        cli_descriptions = { 'post': 'Make an HTTP POST to a target.', 
                            'teams': 'Target Microsoft Teams.', 
                            'card': "Post a Teams Card",
                        }
        summary = dedent('''\
        Posts a preformatted card (aka 'actionable message', or 'MessageCard') to a Microsoft Teams channel.
        This script supports specific preformatted messages oriented towards supporting our Jenkins build process. 
        (additional preformatted cards may be created/added by extending the 'TeamsCardTemplate' class in teams_cards.py 
        and updating this CLI application to suport it).
        ''')
        super().__init__(cli_path, cli_descriptions, summary)

    def config_parser(self, parser):
        parser.set_defaults(func=self.run)
        parent_parser = configargparse.ArgParser(add_help=False)
        parent_parser.add('--webhook-url', '-u', required=True, env_var='TEAMS_WEBHOOK_URL',
            help='The Teams "Incoming Webhook" URL for a Teams channel (where messages will be posted).')
        parent_parser.add('--message', help='Custom messgage to be printed at the top of the card.')
        parent_parser.add('--file', help='Custom message to be printed at the top of the card, loaded from the file indicated.')
        parent_parser.add('--diff-markdown', action='store_true',
            help='Wrap the custom message(s) in ```diff\n\{message\}\n``` markdown.')
        parent_parser.add('--code-markdown', action='store_true',
            help='Wrap the custom message(s) in ```\n\{message\}\n``` markdown.')
        parent_parser.add('--clean-ansi-colors', action='store_true',
            help='Clean/remove any ANSI Color codes that are in the provided message/file.')
        parent_parser.add('--tail', type=int, 
            help='Only print the last `TAIL` lines of the provided message/file.')    
        subparsers = parser.add_subparsers(title="message-type", dest='message_type',
            description="There are built in 'message types' that can be sent.")
        subparsers.required = True
        subparsers.dest = 'message_type'
        # Subparser for Build Status Cards
        sp = subparsers.add_parser('build-status', parents=[parent_parser],
            help='Generate a "Jenkins build status" message.')
        sp.add('status', choices=['STARTED', 'SUCCESS', 'UNSTABLE', 'FAILURE', 'NOT_BUILD', 'ABORTED'],
            help='Provide the build status here (from the provided choices).')
        sp.add('--build-type', default='BUILD', choices=['BUILD', 'DEPLOYMENT'],
            help="The 'type' of the build (from provided choices).")
        sp.add('--jenkins-build-url', env_var='BUILD_URL',
            help='The URL that links directly to the Jenkins build.')
        sp.add('--pull-request-url', env_var='PR_URL',
            help='The URL that links directly to the Pull Request to which this build is associated.')
        sp.add('--pull-request-id', env_var='PR_ID',
            help='The ID of the Bitbucket pull request.')
        sp.add('--jenkins-job-name', env_var='JOB_NAME',
            help='The name of the Job in Jenkins.')
        sp.add('--jenkins-build-id', env_var='BUILD_ID',
            help='The ID of this particular build in Jenkins.')
        sp.add('--playbook-limit', env_var='PLAYBOOK_LIMIT',
            help='A string indicating the PLAYBOOK_LIMIT for this build.')
        # Subparser for Pull Request Cards
        sp = subparsers.add_parser('pull-request', parents=[parent_parser],
            help='Generate a "Bitbucket Pull Request" message.')
        sp.add('--pull-request-id', required=True, env_var='PR_ID',
            help='The ID of the Bitbucket pull request.')
        sp.add('--pull-request-update', action='store_true', env_var='PR_UPDATE', # TODO Document the following: Assign "true" to PR_UPDATE env variable, per configargparse docs
            help='Provide this flag if this is a pull request update (it will produce a much smaller/simpler Teams Card).')
        sp.add('--pull-request-author', env_var='PR_AUTHOR',
            help='The person who submitted the Bitbucket pull request.')
        sp.add('--project', env_var='BITBUCKET_PROJECT',
            help='The Bitbucket project key for the project where the pull request exists.')
        sp.add('--repo-slug', env_var='BITBUCKET_REPO',
            help='The Bitbucket repository slug.')
        sp.add('--pull-request-title', env_var='PR_TITLE', 
            help='The title of the Bitbucket pull request.')
        sp.add('--pull-request-dest', env_var='PR_DESTINATION', 
            help='The destination branch of the Bitbucket pull request.')
        sp.add('--pull-request-description', env_var='PR_DESCRIPTION',
            help='The description of the Bitbucket pull request.')
        sp.add('--playbook-limit', env_var='PLAYBOOK_LIMIT',
            help='A string indicating the PLAYBOOK_LIMIT for this build.')
        self.parser = parser
        return parser

    def run(self, args):
        try:
            card = TeamsCardFactory.build(args)
            response = requests.post(args.webhook_url, json = card.to_json())
            response.raise_for_status()
            _raise_for_http_413(response)
        except requests.exceptions.HTTPError as error:
            print(f"[ERROR] HTTP Error ({error.response.status_code}): {error.response.text}")
            exit(-1)
        except TeamsCardTemplateError as error:
            print(f'[ERROR] Missing arguments detected when creating {error.card_type}: {infer_missing_arguments(error.required_args, error.provided_args)}.')
            # Add the list of arguments that were missing
            if len(error.optional_args) > 0:
                print(f'[INFO] Optional arguments for {error.card_type}: {infer_missing_arguments(error.optional_args, error.provided_args)}.')
            print(dedent(f'''\
                [INFO] Was '{error.card_type}' the type of card you meant to build? 
                    If not, review the TeamsCardFactory.build() method in buildtools/util/teams_cards.py 
                    to understand how this card type was chosen (based on the arguments you provided).
                '''))
            exit(-1)

