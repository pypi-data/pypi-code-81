import json
import codecs
import os.path

from instagram_private_api import (
    Client,
    ClientError,
    ClientLoginError,
    ClientCookieExpiredError,
    ClientLoginRequiredError,
    __version__ as client_version,
)


class InstagramLogin:

    @staticmethod
    def to_json(python_object):
        if isinstance(python_object, bytes):
            return {'__class__': 'bytes',
                    '__value__': codecs.encode(python_object, 'base64').decode()}
        raise TypeError(repr(python_object) + ' is not JSON serializable')

    @staticmethod
    def from_json(json_object):
        if '__class__' in json_object and json_object['__class__'] == 'bytes':
            return codecs.decode(json_object['__value__'].encode(), 'base64')
        return json_object

    def on_login_callback(self, api, new_settings_file):
        cache_settings = api.settings
        with open(new_settings_file, 'w') as outfile:
            json.dump(cache_settings, outfile, default=self.to_json)
            print('SAVED: {0!s}'.format(new_settings_file))

    def login(self, username, password, settings_file_path):

        api: Client

        print('Client version: {0!s}'.format(client_version))

        device_id = None
        try:

            settings_file = settings_file_path
            if not os.path.isfile(settings_file):
                # settings file does not exist
                print('Unable to find file: {0!s}'.format(settings_file))

                # login new
                api = Client(
                    username, password,
                    auto_patch=True, authenticate=True,
                    on_login=lambda x: self.on_login_callback(x, settings_file_path))
            else:
                with open(settings_file) as file_data:
                    cached_settings = json.load(file_data, object_hook=self.from_json)
                print('Reusing settings: {0!s}'.format(settings_file))

                device_id = cached_settings.get('device_id')
                # reuse auth settings
                api = Client(
                    username, password,
                    auto_patch=True, authenticate=True,
                    settings=cached_settings)

        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

            # Login expired
            # Do re-login but use default ua, keys and such
            api = Client(
                username, password,
                auto_patch=True, authenticate=True,
                device_id=device_id,
                on_login=lambda x: self.on_login_callback(x, settings_file_path))

        except ClientLoginError as e:
            print('ClientLoginError {0!s}'.format(e))
            return
        except ClientError as e:
            print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
            return
        except Exception as e:
            print('Unexpected Exception: {0!s}'.format(e))
            return

        return api
