"""
This is a convenience module designed to manage OpenID Connect authorization
to the HyperThought system.  Detailed usage instructions can be found in the
Authorization class.
"""

import base64
from datetime import datetime
import json
from threading import Thread
from time import sleep

import dateutil.parser
from dateutil.tz import tzlocal
import requests
import urllib3


# Number of seconds prior to expiration when a refresh request should be
# initiated.
REFRESH_MARGIN = 200

# Disable insecure request warnings.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AuthExpirationException(Exception):
    pass


class Authorization:
    """
    Authorization manager for access to HyperThought via the REST API.

    Parameters
    ----------
    auth_payload : str
        Base-64 encoded text containing a dict with authorization info.

    Public methods
    --------------
    *   get_headers
    *   get_cookies
    *   get_base_url
    *   get_username
    *   get_first_name
    *   get_last_name
    *   get_email

    Usage
    -----
    1.  Go to the My Account page in HyperThought.  Copy the API Access code
        to the clipboard.
    2.  Instantiate an Authorization object using this code as the parameter
        value (auth_payload argument).
    3.  Make calls to the API using headers and cookies obtained from the
        get_headers and get_cookies methods.  (Also user verify=False.)            
    4.  If using this module from an application (e.g. HyperDrive), use
        get_base_url to construct urls and the remaining methods (get_username,
        get_first_name, get_last_name, get_email) to get information on the
        currently logged-in user.
    """

    # Expected fields in the auth payload parameter.
    EXPECTED_AUTH_FIELDS = (
        'baseUrl',          # Base URL for HyperThought instance.
        'clientId',         # ID for auth client.
        'clientSecret',     # Needed for token refresh.
        'accessToken',      # Access token used to HyperThought endpoints.
        'expiresIn',        # Seconds to expiration for access token.
        'expiresAt',        # Time of expiration for access token.
        'refreshToken',     # Token to refresh access / get a new access token.
    )

    def __init__(self, auth_payload):
        auth_payload = json.loads(base64.b64decode(auth_payload))

        # TODO:  Improve upon parameter validation.
        for field in self.EXPECTED_AUTH_FIELDS:
            assert field in auth_payload

        self._base_url = auth_payload['baseUrl']

        # TODO:  Is this needed?
        if '127.0.0.1' in self._base_url:
            self._base_url = self._base_url.replace('127.0.0.1', 'localhost')

        self._token_url = f'{self._base_url}/openid/token/'
        self._client_id = auth_payload['clientId']
        self._client_secret = auth_payload['clientSecret']
        self._access_token = auth_payload['accessToken']
        self._refresh_token = auth_payload['refreshToken']
        self._user_info = None

        # This cookie is needed to avoid being redirected to the HyperThought
        # banner page.
        self._cookies = {
            'dodAccessBanner': 'true'
        }

        # Time to sleep prior to requesting an access token refresh.
        expiration_time = dateutil.parser.parse(auth_payload['expiresAt'])
        current_time = datetime.now(tzlocal())
        time_delta = expiration_time - current_time
        seconds_to_expiration = time_delta.total_seconds()
        self._refresh_margin = REFRESH_MARGIN

        if seconds_to_expiration < self._refresh_margin:
            raise AuthExpirationException(
                (
                    'Insufficient margin for access token refresh.\n'
                    'Margin: {}\n'
                    'Expires in: {}\n'
                ).format(
                    self._refresh_margin,
                    seconds_to_expiration
                )
            )
        
        self._refresh_sleep_time = seconds_to_expiration - self._refresh_margin

        # Define a refresh thread without starting it.
        self._refresh_thread = Thread(target=self._refresh)
        self._refresh_thread.setDaemon(True)
        self._refresh_thread.start()

    def get_base_url(self):
        """Get the base url for the auth client."""
        return self._base_url

    def get_base_url_dns(self):
        """Get the base url DNS for the auth client."""
        if '//' in self._base_url:
            split_dns_name = self._base_url.split('//')[1].split(':')

            if len(split_dns_name) > 1:
                return '.'.join(split_dns_name)

            return split_dns_name[0]
        else:
            return self._base_url

    def get_headers(self):
        """Get headers for authenticated REST API requests."""
        return {
            'Authorization': f'Bearer {self._access_token}'
        }

    def get_cookies(self):
        """Get cookies for authenticated REST API requests."""
        return dict(self._cookies)

    def _set_user_info(self):
        """Set self._user_info by calling the userinfo endpoint."""
        url = '{}/api/auth/userinfo/'.format(self._base_url)
        headers = self.get_headers()
        cookies = self.get_cookies()
        r = requests.get(url, headers=headers, cookies=cookies, verify=False)

        if r.status_code >= 400:
            raise Exception('Unable to set user info.')

        self._user_info = r.json()

    def get_username(self):
        """Get the username associated with the currently logged in user."""
        if not self._user_info:
            self._set_user_info()

        return self._user_info['username']

    def get_first_name(self):
        """Get the first name of the currently logged-in user."""
        if not self._user_info:
            self._set_user_info()

        return self._user_info['first_name']

    def get_last_name(self):
        """Get the last name of the currently logged-in user."""
        if not self._user_info:
            self._set_user_info()

        return self._user_info['last_name']

    def get_email(self):
        """Get the email address of the currently logged-in user."""
        if not self._user_info:
            self._set_user_info()

        return self._user_info['email']

    def _refresh(self):
        """
        Refresh the access and refresh tokens using the refresh token.

        This method is the target of a separate execution thread.
        It should run as long as the client application is running, to ensure
        that the user is continuously authorized.
        """
        while True:
            sleep(self._refresh_sleep_time)

            data = {
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': self._refresh_token,
            }

            r = requests.post(
                url=self._token_url,
                data=data,
                cookies=self._cookies,
                verify=False
            )

            if r.status_code >= 400:
                raise Exception("Attempt to set tokens by calling "
                                f"{self._token_url} has failed")

            auth_info = r.json()
            self._access_token = auth_info['access_token']
            self._refresh_token = auth_info['refresh_token']
            seconds_to_expiration = auth_info['expires_in']

            if seconds_to_expiration < self._refresh_margin:
                raise Exception(
                    (
                        'Insufficient margin for access token refresh.\n'
                        'Margin: {}\n'
                        'Expires in: {}\n'
                    ).format(
                        self._refresh_margin,
                        seconds_to_expiration
                    )
                )

            self._refresh_sleep_time = seconds_to_expiration - self._refresh_margin
