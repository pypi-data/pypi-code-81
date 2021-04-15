import os
import json

from requests import Request, Session

AUTH_ENDPOINT = 'https://hh.ru/oauth/token'
CREDENTIAL_DIR = 'credentials\\'


class AppAuth:
    """AppAuth class wraps app authorization. It encloses auth app_credentials and
    acquires app_access_token for app specified in app_credentials file"""

    def __init__(self, with_file: bool = True):
        # client id and secret stored in file or passed trough env vars
        if with_file:
            cred_path = os.path.join(CREDENTIAL_DIR, 'app_credentials')
            with open(cred_path) as cred_file:
                app_credentials = json.loads(cred_file.read())
        else:
            app_credentials = os.environ
        self.client_id = app_credentials['hh_app_client_id']
        self.client_secret = app_credentials['hh_app_client_secret']

        # access_token stored in file only
        if 'app_access_token' in os.listdir(CREDENTIAL_DIR):
            with open(os.path.join(CREDENTIAL_DIR, 'app_access_token')) as token_file:
                access_token = token_file.read()
            if len(access_token) > 3:
                self.access_token = access_token
        else:
            self.access_token = None

    def has_token(self) -> bool:
        """has_token indicates whether an app_access_token present or not"""
        return bool(self.access_token)

    def write_token(self):
        """write_token writes token to separate file in credentials dir"""

        with open(os.path.join(CREDENTIAL_DIR, 'app_access_token'), 'w') as token_file:
            token_file.write(self.access_token)

    def get_new_token(self):
        """get_new_token acquires new app_access_token (existing app_access_token will be revoked)"""

        request_body = '&'.join(['grant_type=client_credentials',
                                 f'client_id={self.client_id}',
                                 f'client_secret={self.client_secret}'])
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Content-Length': f'{len(request_body)}'}

        session = Session()
        request = Request('POST', url=AUTH_ENDPOINT, headers=headers)
        prepared_request = request.prepare()
        prepared_request.body = request_body
        response = session.send(prepared_request)

        if response.status_code == 400:
            print('400 Bad request')
        elif response.status_code == 403:
            print('403 Forbidden - access token have been issued in the last 5 min.')

        response_dict = json.loads(response.content)
        access_token = response_dict.get('app_access_token')
        if access_token is not None:
            self.access_token = access_token
            self.write_token()
