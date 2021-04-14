import os

auth_params = {
    "wallet_uri": 'https://wallet.staging.dnastack.com',
    "redirect_uri": "https://92a15358-9be7-4edf-8758-ec87ee1f81e3.mock.pstmn.io/" ,
    "client_id": "9110B5F6-B6E4-41D1-A88A-7BD96524FEA3",
    "client_secret": "5DpuE4tXMHi9SShgOCyUmOjyU5RsDYZGTj9yKtPqCo4e58Q8MEILEz0oybNu3TENphHovg8YbxjuHtZk2tFECaPdtRtrkRNIuUw5XCSYhhOzADiCPqZohFsTfpQkoCmS"
}

wallet_uri = 'https://wallet.staging.dnastack.com' #TODO: replace with prod
redirect_uri = "https://92a15358-9be7-4edf-8758-ec87ee1f81e3.mock.pstmn.io/" #TODO: replace this with a proper DNAstack URI
config_file_path = f"{os.path.expanduser('~')}/.covid-cloud/config.yaml"
cli_directory = f"{os.path.expanduser('~')}/.covid-cloud"
downloads_directory = f"{os.path.expanduser('~')}/.covid-cloud/downloads"

ACCEPTED_CONFIG_KEYS = ['search-url', 'drs-url', 'personal_access_token', 'email', 'oauth_token', 'oauth_token_expiry',
                        'wallet-url', 'client-id', 'client-secret', 'client-redirect-uri']

auth_scopes = "openid drs-object:write drs-object:access search:info search:data search:query"