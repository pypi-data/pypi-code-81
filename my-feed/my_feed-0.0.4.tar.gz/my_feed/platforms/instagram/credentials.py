import json

file_name = 'configs/instagram_creds.json'
with open(file_name, 'r', encoding='utf8') as f:
    file_data = json.loads(f.read())
    f.close()


class CredentialsManager:
    """
    Load all the Users Credentials in an array
    """
    class _UserCredentials:
        def __init__(self, username, password):
            self.username = username
            self.password = password
            self.pass_code = None

    def __init__(self):
        """
        Load the credentials from the json file
        Store them ar list of _UserCredentials obj
        """
        self.credentials = []

        _credentials = file_data.get('creds')
        for el in _credentials:
            key = list(el.keys())[0]
            self.credentials.append(self._UserCredentials(key, el[key]))


credentials_manager = CredentialsManager()
