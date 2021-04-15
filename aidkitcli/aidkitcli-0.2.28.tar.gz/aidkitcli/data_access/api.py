"""Send requests to REST api"""

import json
import os
from pathlib import Path
from typing import Dict, List

import requests

from aidkitcli.core.report import Report, dict2report
from aidkitcli.data_access.authentication import get_token, get_url
from aidkitcli.data_access.utils import dict_to_bytes, path_to_bytes

AIDKIT_PORT = os.getenv('HOME_PATH', 80)


class RESTApi:
    def post_data(self, zip_path):
        """Upload data."""
        resource = 'api/data/'
        url = f'{get_url()}:{AIDKIT_PORT}/{resource}'
        file = {
            Path(zip_path).name: path_to_bytes(path=zip_path)
        }
        response = requests.post(
            url=url,
            headers=self.header,
            files=file
        )
        return _responder(response, url)

    def list_data(self) -> List[str]:
        """List uploaded data."""
        resource = 'api/data/'
        url = f'{get_url()}:{AIDKIT_PORT}/{resource}'
        response = requests.get(
            url=url,
            headers=self.header
        )
        return _responder(response, url)

    def post_model(self, model_path: str) -> str:
        """Upload model."""
        resource = 'api/ml-models/'
        url = f'{get_url()}:{AIDKIT_PORT}/{resource}'
        file = {
            Path(model_path).name: path_to_bytes(path=model_path)
        }

        response = requests.post(
            url=url,
            headers=self.header,
            files=file
        )
        return _responder(response, url)

    def list_models(self):
        """List uploaded models."""
        resource = 'api/ml-models/'
        url = f'{get_url()}:{AIDKIT_PORT}/{resource}'
        response = requests.get(
            url=url,
            headers=self.header
        )
        return _responder(response, url)

    # def get_status(self) -> Dict[str, int]:
    #     """Get status of running pipelines."""
    #     resource = 'api/analyses/'
    #     url = f'{get_url()}:{AIDKIT_PORT}/{resource}'
    #     response = requests.get(
    #         url=url,
    #         headers=self.header
    #     )
    #     return _responder(response, url)

    def post_pipeline(self, toml_path: str) -> Dict[str, int]:
        """Start pipeline."""
        resource = 'api/analyses/'
        url = f'{get_url()}:{AIDKIT_PORT}/{resource}'
        response = requests.post(
            url=url,
            headers=self.header,
            files=dict(
                toml=path_to_bytes(path=toml_path)
            )
        )
        return _responder(response, url)

    def post_pipeline_from_dict(self, toml_dict: dict) -> Dict[str, int]:
        """Start pipeline."""
        resource = 'api/analyses/'
        url = f'{get_url()}:{AIDKIT_PORT}/{resource}'
        response = requests.post(
            url=url,
            headers=self.header,
            files=dict(
                toml=dict_to_bytes(config=toml_dict)
            )
        )
        return _responder(response, url)

    def get_status(self, analysis_id: int) -> Dict[str, int]:
        resource = f'api/analyses/{analysis_id}/status/'
        url = f'{get_url()}:{AIDKIT_PORT}/{resource}'
        response = requests.get(
            url=url,
            headers=self.header,
        )
        return _responder(response, url)

    def get_report(self, analysis_id: int) -> Report:
        resource = f'api/analyses/{analysis_id}/report/'
        url = f'{get_url()}:{AIDKIT_PORT}/{resource}'
        response = requests.get(
            url=url,
            headers=self.header,
        )
        report_dict = _responder(response, url)
        report_model = dict2report(report_dict=report_dict)
        return report_model

    @property
    def header(self) -> dict:
        """Authorized header."""
        return {"Authorization": f"Bearer {get_token()}"}


def _responder(response, url):
    if response.status_code == 401:
        raise ConnectionError(
            f"You are not authorized for {url}. Please check your authentication.")
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        return response.text
