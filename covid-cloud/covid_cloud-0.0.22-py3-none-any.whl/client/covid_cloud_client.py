from covid_cloud.client import *
from covid_cloud import constants
from pandas import DataFrame
from getpass import getpass
import json


class COVIDCloud: 

    def __init__(self, email=None, personal_access_token=None, search_url=None, auth_params=auth_params):
        self.email = email
        self.personal_access_token = personal_access_token
        self.search_url = search_url
        self.auth_params = auth_params
        self.oauth_token = {}

    def login(self, server=None, email=None, personal_access_token=None):
        
        #if the user did not provide a PAT or email, get that from input
        if not server:
            server = input("Enter your DRS Server: ")

        if not (personal_access_token or self.personal_access_token):
            personal_access_token = getpass("Enter your Personal Access Token (PAT): ")
        
        if not (email or self.email):
            email = input("Enter your Email: ")

        drs_host = get_host(server)

        self.oauth_token[drs_host] = login(email=email if email else self.email,
                                 personal_access_token= personal_access_token if personal_access_token else self.personal_access_token,
                                 auth_params=self.auth_params,
                                 search_url=self.search_url,
                                 drs_url=server)

    def query(self, q, download=False, use_json=False, raw=False):
        return json.loads(query(self.search_url, q, download, use_json, raw, self.oauth_token))

    def list_tables(self):
        return json.loads(get_tables(self.search_url, self.oauth_token))

    def get_table(self, table_name):
        return json.loads(get_table(self.search_url, table_name, self.oauth_token))

    def load(self, urls, output_dir=downloads_directory):
        download_content = []
        download_files(urls, output_dir, self.oauth_token, self.email, self.personal_access_token, self.auth_params, download_content)
        return download_content

    def download(self, urls, output_dir=downloads_directory):
        return download_files(urls, output_dir, self.oauth_token, self.email, self.personal_access_token, self.auth_params)
