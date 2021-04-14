import requests
from typing import Optional, Dict, List
from .utils import (
    assert_valid_name,
    raise_resp_exception_error,
    requests_retry,
    _upload_local_files,
    _upload_local_zip
)
import json


class TrojClient:
    def __init__(
        self,
        *,
        api_endpoint: str = "https://wct55o2t7c.execute-api.ca-central-1.amazonaws.com/prod/api/v1",
        **kwargs,
    ) -> "Client":
        self._creds_id_token = None
        self._creds_refresh_token = None
        self._creds_api_key = None
        self.api_endpoint = api_endpoint
        self.cognito_client_id = "46ca3qqhhkos18k3hjqn10b4uc"
        requests_retry.hooks["response"].append(
            self.reauth
        )  # https://github.com/psf/requests/issues/4747 - Important for Retry vs urllib3

    def _get_creds_headers(self):
        """
        Get appropriate request headers for the currently set credentials.

        Raises:
            Exception: No credentials set.
        """
        if self._creds_id_token:
            return {
                "Authorization": f"Bearer {self._creds_id_token}",
                "x-api-key": f"{self._creds_api_key}",
            }
        else:
            raise Exception("No credentials set.")

    def set_credentials(
        self,
        *,
        id_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Set credentials for the client.

        Args:
            id_token (str, optional): Used by the client to authenticate the user. Defaults to None.
            refresh_token (str, optional): Used to refresh the ID Token. Defaults to None.
            api_key (str, optional): Used to gain access to API
        Raises:
            Exception: Invalid credential combination provided.
        """

        # TODO: Change to require id_token and api_key together
        if id_token is not None:
            self._creds_id_token = id_token
        else:
            raise Exception("Please provide an ID Token.")
        if refresh_token is not None:
            self._creds_refresh_token = refresh_token
        else:
            raise Exception("Please provide a Refresh Token.")
        if api_key is not None:
            self._creds_api_key = api_key
        else:
            raise Exception("Please provide an API Key.")

    def test_api_endpoint(self):
        try:
            r = requests_retry.get(
                "https://wct55o2t7c.execute-api.ca-central-1.amazonaws.com/prod/ping"
            )
            return r.status_code
        except Exception as exc:
            raise Exception(f"test_api_endpoint error: {exc}")

    def create_project(self, project_name: str):
        """
        Create a new project via the REST API.

        Args:
            project_name (str): Name you want to give your project
        """

        assert_valid_name(project_name)

        data = {"project_name": project_name}

        r = requests_retry.post(
            f"{self.api_endpoint}/projects",
            headers=self._get_creds_headers(),
            json=data,
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}

    def get_projects(self):
        """
        Get data about the users projects
        """

        r = requests_retry.get(
            f"{self.api_endpoint}/projects",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}

    def project_exists(self, project_name: str):
        """
        Check if a project exists.

        Args:
            project_name (str): Project name

        Returns:
            Dict[int, dict]: dict(data) will either be False or the project itself
        """

        r = requests_retry.get(
            f"{self.api_endpoint}/projects/{project_name}",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}

    def delete_project(self, project_name: str):
        """
        Try to delete a project

        Args:
            project_name (str): Name of the project to be deleted
        """

        if self.project_exists(project_name)["data"] is False:
            raise Exception(f"Project '{project_name}' does not exist.")

        r = requests_retry.delete(
            f"{self.api_endpoint}/projects/{project_name}",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}

    def create_dataset(
        self,
        project_name: str,
        dataset_name: str,
    ):
        assert_valid_name(dataset_name)
        project_data = self.project_exists(project_name)

        data = {
            "project_uuid": project_data["data"]["project_uuid"],
            "dataset_name": dataset_name,
        }

        r = requests_retry.post(
            f"{self.api_endpoint}/datasets",
            headers=self._get_creds_headers(),
            json=data,
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}
        # End of create_dataset()

    def get_project_datasets(self, project_name: str):
        """
        Get info about existing datasets for a specific project

        Args:
            project_name (str): Name of the project you want to find datasets under
        """

        r = requests_retry.get(
            f"{self.api_endpoint}/projects/{project_name}/datasets",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}

    def dataset_exists(self, project_name: str, dataset_name: str):
        """
        Check if a dataset exists.

        Args:
            project_name (str): Project name
            dataset_name (str): Dataset name

        Returns:
            Dict[int, dict]: dict(data) will either be False or the dataset itself
        """
        if self.project_exists(project_name)["data"] is False:
            raise Exception(f"Project '{project_name}' does not exist.")

        r = requests_retry.get(
            f"{self.api_endpoint}/projects/{project_name}/datasets/{dataset_name}",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}

    def delete_dataset(self, project_name: str, dataset_name: str):
        if self.dataset_exists(project_name, dataset_name)["data"] is False:
            raise Exception(
                f"Dataset '{dataset_name}' does not exist in project '{project_name}'."
            )

        r = requests_retry.delete(
            f"{self.api_endpoint}/projects/{project_name}/datasets/{dataset_name}",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}

    def upload_dataset_files(
        self, image_filepaths: List, project_name: str, dataset_name: str
    ):
        download_urls = []
        get_upload_path = f"{self.api_endpoint}/projects/{project_name}/datasets/{dataset_name}/fetch_upload_dataset_url"

        download_urls = _upload_local_files(
            image_filepaths,
            get_upload_path,
            self._get_creds_headers(),
            "",  # suffix
            "",  # prefix
            delete_after_upload=False,
        )

        return download_urls

    def upload_dataset_files_zipped(
        self, zip_filepath: str, project_name: str, dataset_name: str
    ):
        download_urls = []
        get_upload_path = f"{self.api_endpoint}/projects/{project_name}/datasets/{dataset_name}/fetch_upload_dataset_url_zip"
        complete_upload_path = f"{self.api_endpoint}/projects/{project_name}/datasets/{dataset_name}/fetch_upload_dataset_url_zip/complete"
        download_urls = _upload_local_zip(
            zip_filepath,
            get_upload_path,
            complete_upload_path,
            self._get_creds_headers(),
            "",  # suffix
            "",  # prefix
            delete_after_upload=False,
        )

        return download_urls

    def upload_df_results(self, project_name: str, dataset_name: str, dataframe: dict):
        """
        Uploads dataframe results to database.

        Args:
            project_name (str): Project name
            dataset_name (str): Dataset name
            dataframe (dict): JSONified dataframe

        Returns:
            Dict[int, bool]: status_code and bool whether success/fail to upload
        """
        try:
            dataset = self.dataset_exists(project_name, dataset_name)["data"]

            if dataset is not False:
                dataset_uuid = dataset["dataset_uuid"]

                r = requests_retry.post(
                    f"{self.api_endpoint}/projects/{project_name}/datasets/{dataset_name}/fetch_upload_dataframe_url",
                    headers=self._get_creds_headers(),
                )

                raise_resp_exception_error(r)

                s3_payload_dict = r.json()

                file_to_save = json.dumps(dataframe).encode("utf-8")
                file_name_on_s3 = s3_payload_dict["fields"]["key"]

                files = {"file": (file_name_on_s3, file_to_save)}
                upload_response = requests.post(
                    s3_payload_dict["url"], data=s3_payload_dict["fields"], files=files
                )

                print(f"Upload response: {upload_response.status_code}")

                return {"status_code": upload_response.status_code}
            else:
                raise Exception(
                    "Something went wrong. Double check the project and dataset names."
                )
        except Exception as exc:
            raise Exception(f"post_dataframe error: {exc}")

    def refresh_tokens(self):

        url = "https://troj.auth.ca-central-1.amazoncognito.com/oauth2/token"

        payload = f"grant_type=refresh_token&client_id={self.cognito_client_id}&refresh_token={self._creds_refresh_token}"
        requests.utils.quote(payload)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self._creds_id_token = json.loads(response.text)["id_token"]

        return response

    def reauth(self, res, *args, **kwargs):
        """Hook to re-authenticate whenever authentication expires."""
        if res.status_code == requests.codes.forbidden:
            if res.request.headers.get("REATTEMPT"):
                res.raise_for_status()
            self.refresh_tokens()
            req = res.request
            req.headers["REATTEMPT"] = 1
            req = self.auth_inside_hook(req)
            res = requests_retry.send(req)
            return res

    def auth_inside_hook(self, req):
        """Set the authentication token for the premade request during reauth attempts inside the retry hook."""
        req.headers["Authorization"] = f"Bearer {self._creds_id_token}"
        return req
