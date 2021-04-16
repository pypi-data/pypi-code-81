import requests
# from dukeai._config._config import


def get_rpa_token(username, password):
    url = "https://api.duke.ai/token/get_token"

    headers = {
              'username': username.upper(),
              'password': password
             }

    response = requests.request("GET", url, headers=headers)

    return response.json
