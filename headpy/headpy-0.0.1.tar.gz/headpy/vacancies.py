import os
import json

import requests
from tqdm import tqdm

from .auth import AppAuth
from .auth import CREDENTIAL_DIR

VACANCIES_ENDPOINT = 'https://api.hh.ru/vacancies'


class App:
    def __init__(self):
        self.url = VACANCIES_ENDPOINT
        self.access_token = AppAuth().access_token

        # compose user-agent for request headers
        if 'app_credentials' in os.listdir(CREDENTIAL_DIR):
            with open(os.path.join(CREDENTIAL_DIR, 'app_credentials')) as cred_file:
                app_credentials = json.loads(cred_file.read())
        else:
            app_credentials = os.environ
        self.name = app_credentials['hh_app_name']
        self.version = app_credentials['hh_app_version']
        self.contacts = app_credentials['hh_app_contacts']
        self.user_agent = f"{self.name}/{self.version} ({self.contacts})"

        # compose access_token header
        self.authorization = f"Bearer {self.access_token}"

        # compose headers
        self.request_headers = {'User-Agent': self.user_agent,
                                'Authorization': self.authorization}


class Search(App):
    def __init__(self):
        App.__init__(self)

    def __get_vacancies_number(self, params: dict) -> int:
        """__get_vacancies_number returns total number of vacancies with params specified"""

        params['per_page'], params['page'] = 1, 0
        response = requests.get(self.url, headers=self.request_headers, params=params)
        response_json = json.loads(response.content)
        return int(response_json['found'])

    def __get_requests_number(self, params: dict, max_vac_num: int, per_page: int) -> int:
        """__get_requests_number returns number of paginated requests needed to collect all vacancy ids"""

        vac_number = min(self.__get_vacancies_number(params), max_vac_num)  # api allows to get up to 2000 vacancies
        requests_number = vac_number / per_page if vac_number % per_page == 0 else vac_number // per_page + 1
        return int(requests_number)

    def __get_vacancies(self, params: dict, max_vac_num: int, per_page: int, url: str) -> list:
        """__get_vacancies collects all vacancy ids and use them to collect all vacancies data"""

        # collect ids of vacancies
        vacancies_ids = list()
        requests_number = self.__get_requests_number(params, max_vac_num, per_page)

        for page in tqdm(range(requests_number), desc='Getting vacancies ids'):
            # adds pagination
            params['per_page'], params['page'] = per_page, page

            # gets page and stores vacancy ids
            vacancies_json = requests.get(url, headers=self.request_headers, params=params)
            response_body = json.loads(vacancies_json.content)
            part_ids = [int(item['id']) for item in response_body['items']]
            vacancies_ids.extend(part_ids)

        vacancies_ids = vacancies_ids[:max_vac_num]  # cut number of vacancies to max_vac_num

        vacancies = list()
        for vac_id in tqdm(vacancies_ids, desc='Getting vacancies'):
            url = self.url + f'/{vac_id}'
            response = requests.get(url, headers=self.request_headers)
            vacancy = json.loads(response.content)
            vacancies.append(vacancy)

        return vacancies

    def search_by_params(self, params: dict, max_vac_num: int = 2000, per_page: int = 100) -> list:
        """Search vacancies by params (more at https://github.com/hhru/api/blob/master/docs/vacancies.md#search)"""

        url = self.url
        return self.__get_vacancies(params, max_vac_num, per_page, url)

    def search_similar(self, vacancy_id: int, params: dict = None,
                       max_vac_num: int = 2000, per_page: int = 100) -> list:
        """Search vacancies similar to a certain vacancy (also can use params to narrow the search)"""

        if params is None:
            params = dict()
        url = self.url + f'/{vacancy_id}/similar_vacancies'
        return self.__get_vacancies(params, max_vac_num, per_page, url)
