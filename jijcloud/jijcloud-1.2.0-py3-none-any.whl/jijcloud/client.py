from base64 import encode
from typing import Any, Dict, Optional
import requests
import json
import zstandard

from requests.exceptions import HTTPError
from jijcloud.config import Config


class JijCloudClient:
    def __init__(
            self,
            url: Optional[str] = None,
            token: Optional[str] = None,
            config: Optional[str] = None,
            config_env: str = 'default'):

        self.config = Config(url, token, config, config_env)
        url = self.config.url
        self.url = url if url[-1] != '/' else url[:-1]
        self.token = self.config.token

        self.instance_id: Optional[str] = None
        self.req_solution_id: Optional[str] = None

    def post_instance(
            self,
            instance_type: str,
            instance: Dict[str, Any],
            endpoint: str = '/jijcloudpostinstance/instance'
            ) -> Dict[str, str]:
        if not isinstance(instance_type, str):
            raise TypeError(
                    "'instance_type' is `str`, not `{}`"
                    .format(type(instance_type)))
        if not isinstance(instance, dict):
            raise TypeError(
                    "instance is `dict`, not `{}`".format(type(instance)))

        endpoint = endpoint[:-1] if endpoint[-1] == '/' else endpoint

        # ------- Upload instance data to JijCloud ---------
        upload_endpoint = self.url + endpoint + '/upload'
        headers = {
            'Content-Type': "application/zstd",
            "Ocp-Apim-Subscription-Key": self.token
        }

        # encode instance
        json_data = json.dumps(instance)
        json_binary = json_data.encode('ascii')
        compressed_binary = zstandard.ZstdCompressor().compress(json_binary)
        res = requests.post(
                upload_endpoint,
                headers=headers,
                data=compressed_binary,
                stream=True)

        status_check(res)

        # res_body => {
        #   "file_name": str
        # }
        res_body: dict = res.json()
        self.instance_data_id = res_body["instance_data_id"]
        # -----------------------------------------------

        # ---- `instance_type` registration to JijCloud-API -----
        regist_endpoint = self.url + endpoint + '/'
        req_body = json.dumps({
            "instance_type": instance_type,
            "instance_data_id": self.instance_data_id
        })
        headers = {
            'Content-Type': "application/json",
            "Ocp-Apim-Subscription-Key": self.token
        }
        res = requests.post(
                regist_endpoint,
                headers=headers,
                data=req_body)
        status_check(res)

        self.instance_id = res.json()['instance_id']
        # ------------------------------------------------------
        return self.instance_id

    def submit_solve_query(
            self,
            solver_name: str,
            parameters: dict,
            instance_id: Optional[str] = None,
            endpoint: str = '/jijcloudquery/solution'):
        if self.instance_id is None and instance_id is None:
            message = "solve_request() missing 1 "
            message += "require positional argument: 'instance_id'"
            raise TypeError(message)

        if not isinstance(solver_name, str):
            raise TypeError("`solver_name` is str. not {}"
                            .format(type(solver_name)))

        if not isinstance(parameters, dict):
            raise TypeError("`parameters` is dict. not {}"
                            .format(type(parameters)))

        instance_id = self.instance_id if instance_id is None else instance_id

        query_endopoint = self.url + endpoint
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.token
        }

        json_data = json.dumps({
            'instance_id': instance_id,
            'solver_params': parameters,
            'solver': solver_name
        })

        res = requests.post(query_endopoint, headers=headers, data=json_data)

        status_check(res)

        # res_body => {
        #   "solution_id": str,
        # }
        res_body: dict = res.json()
        self.req_solution_id = res_body["solution_id"]

        return res_body

    def fetch_result(
            self,
            solution_id: Optional[str] = None,
            endpoint: str = '/jijcloudquery/solution') -> dict:
        if self.req_solution_id is None and solution_id is None:
            message = "fetch_result() missing 1 "
            message += "require positional argument: 'solution_id'"
            raise TypeError(message)

        solution_id = self.req_solution_id if solution_id is None else solution_id

        fetch_endpoint = self.url + endpoint

        headers = {
            'Ocp-Apim-Subscription-Key': self.token
        }

        params = {
            'solution_id': solution_id
        }

        res = requests.get(fetch_endpoint, headers=headers, params=params)

        status_check(res)

        res_body = res.json()
        if res_body is None:
            raise HTTPError('solution_id is not found')

        return res_body


def status_check(res):
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        res = e.response
        try:
            res_body = res.json()
        except json.decoder.JSONDecodeError:
            raise requests.exceptions.HTTPError(e)

        raise requests.exceptions.HTTPError(e, res_body)
