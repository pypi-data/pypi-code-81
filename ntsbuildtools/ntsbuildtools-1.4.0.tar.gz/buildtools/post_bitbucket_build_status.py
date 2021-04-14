#!/usr/bin/env python3
''' post_bitbucket_build_status.py
Posts a build status to this project's bitbucket repository.
'''
import os
import requests
import configargparse

from . import __version__, BuildToolsTemplate

class PostBitbucketBuildStatus(BuildToolsTemplate):
    def __init__(self):
        cli_path = ['post', 'bitbucket', 'build-status']
        cli_descriptions = { 'post': 'Make an HTTP POST to a target.', 
                            'bitbucket': 'Target Bitbucket.', 
                            'build-status': 'Set the "Build Status" in Bitbucket.',
                        }
        summary = 'Set the "Build Status" in Bitbucket for a particular git commit.'
        super().__init__(cli_path, cli_descriptions, summary)

    def config_parser(self, parser):
        parser.add('--commit', required=True, env_var='COMMIT', 
            help='The FULL LENGTH git commit for which this build is being run.')
        parser.add('--build-status', required=True, choices=['STARTED', 'SUCCESS', 'UNSTABLE', 'FAILURE', 'NOT_BUILD', 'ABORTED'],
            help='The build status to be reported to Bitbucket. Accepts Jenkins build statuses, as well as the keyword "STARTED".')
        parser.add('--user', required=True, env_var='BITBUCKET_USER',
            help="Bitbucket user that will be used to authenticate to Bitbucket.")
        parser.add('--password', required=True, env_var='BITBUCKET_PASSWORD',
            help="Bitbucket password (or Personal Access Token) for the Bitbucket user.")
        parser.add('--build-url', required=True, env_var='BUILD_URL',
            help="Direct-URL to the Jenkins build.")
        parser.add('--job-name', required=True, env_var='JOB_NAME',
            help="The Jenkins Job/Pipeline name that called this build.")
        parser.add('--build-key', env_var='BUILD_KEY', default="UPDATE_ONLY", 
            help="""Unique identifier to differentiate consecutive builds (optional). If omitted, 
            consecutive builds will *update* the existing build status for this Jenkins Job/Pipeline.""")
        parser.add('-m', '--message', help="Build message, to be shown in Bitbucket. Should be kept very short.")
        parser.set_defaults(func=self.run)
        self.parser = parser
        return parser

    def _parse_status(self, jenkins_status):
        if  jenkins_status == "STARTED":
            return "INPROGRESS"
        if  jenkins_status == "SUCCESS":
            return "SUCCESSFUL"
        # By default, fail the build (and for all the other build statuses)
        else:
            return "FAILED"

    def _build_json(self, status, build_key, job_name, build_url, message=None):
        status = self._parse_status(status)
        if message:
            return {
                "state": status,
                "key": build_key,
                "name": job_name,
                "url": build_url,
                "description": message
            }
        return {
            "state": status,
            "key": build_key,
            "name": job_name,
            "url": build_url
        }

    def run(self, args):
        json_payload = self._build_json(args.build_status, args.build_key, 
            args.job_name, args.build_url, args.message)
        try:
            response = requests.post(f'{args.bitbucket_url}/rest/build-status/1.0/commits/{args.commit}',
                json = json_payload, auth = (args.user, args.password))
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f"[ERROR] HTTP Error ({error.response.status_code}): {error.response.text}")
            exit(-1)