""" GuardiPy - a Guardicore Centra API client for Python 3.x """
import logging
import json
from enum import IntEnum
from time import sleep
from typing import List, TypeVar, Union, Dict

import requests

from GuardiPy import CentraObject
from GuardiPy.exceptions import AuthFailedException
from GuardiPy.helpers import CentraApiPayload, CentraEntity, CentraApiExportable

AnyCentraEntity = TypeVar("AnyCentraEntity", bound=CentraEntity)


class ExportStatus(IntEnum):
    IN_PROGRESS = 1
    COMPLETE = 2
    NO_INCIDENTS = 4


class Centra:
    """ Base Centra API Client """

    @staticmethod
    def convert_to_dictionary(entity: CentraEntity, class_key=None) -> Union[Dict, List[Dict]]:
        """
            Converts any CentraEntity (objects returned from the API) into a flat dictionary. Does so recursively to
            allow for flexibility with reporting tools or anything requiring an object to be JSON serialized on-demand.
        """
        if isinstance(entity, dict):
            data = {}
            for (k, v) in entity.items():
                data[k] = Centra.convert_to_dictionary(v, class_key)
            return data
        elif hasattr(entity, "__iter__") and not isinstance(entity, str):
            return [Centra.convert_to_dictionary(v, class_key) for v in entity]
        elif hasattr(entity, "__dict__"):
            data = dict([(key, Centra.convert_to_dictionary(value, class_key))
                         for key, value in entity.__dict__.items()
                         if not callable(value) and not key.startswith('_')])
            if class_key is not None and hasattr(entity, "__class__"):
                data[class_key] = entity.__class__.__name__
            return data
        else:
            return {}

    def execute(self, action: Union[CentraApiPayload, CentraApiExportable]) \
            -> Union[AnyCentraEntity, List[AnyCentraEntity]]:
        # TODO Finish pagination wrapper.
        """
            This method is used to perform searches/lookups. A CentraApiPayload (or CentraApiExportable) should be
            generated from a CentraObject static method such as `.list()` for querying.
        """
        if action.method == 'GET':
            logging.debug(f"Making GET request to {self._base_url + action.path}")
            result = self._session.get(url=self._base_url + action.path, params=action.get_querystring_params())
            logging.debug(f"Full request path was:  {result.request.path_url}")
            try:
                parsed_result = result.json()
                if not action.response_pagination:  # short circuit to return only one instance for certain API calls
                    return action.return_type(**parsed_result)
                else:
                    objects = []
                    for obj in parsed_result.get('objects', []):
                        logging.debug(f"casting this json to instance of {action.return_type}")
                        objects.append(action.return_type(**obj))
                    else:
                        return objects
            except (ValueError, json.JSONDecodeError):
                return None
        elif action.method == 'POST':
            logging.debug(f"Making POST request to {self._base_url + action.path}")
            data = json.dumps(action.data)
            result = self._session.post(url=self._base_url + action.path, data=data)
            logging.debug(f"Full request path was: {result.request.path_url}")
            try:
                parsed_result = result.json()
            except (ValueError, json.JSONDecodeError):
                parsed_result = None
            return parsed_result
        else:
            logging.warning(f"Unsupported request type {action.method}")
        return []

    def export_to_csv(
            self,
            action: CentraApiExportable,  # export descriptor
            task_polling_interval: int = 5,  # time to wait between checks for the export to have finished
            filename: str = None,
    ) -> str:
        """
            This method is similar to .execute() except it is meant to submit a task to the server for exporting a
            CSV. Submitting this request to the server is non-blocking. For simplicity, this method wraps
            the submission, polling, fetching/returning of the CSV synchronously. TODO: async bool + callback param.
        """
        logging.debug(f"Priming export_task_status with View ID {action.export_view_name}...")
        # If we do not send a new request and specify a view_name, then we are (somehow) likely to download
        # a duplicate copy of a previously submitted report... Probably a UI workaround server-side?
        logging.debug(f"{self._base_url}/export_csv_task_status/{action.export_view_name}")
        priming_request = self._session.get(url=f"{self._base_url}/export_csv_task_status",
                                            params={"view_name": action.export_view_name})
        export_url = self._base_url + action.path + action.export_suffix
        logging.debug(f"Submitting export task via GET request to  {export_url}...")

        job_submission = self._session.get(url=export_url, params=action.get_querystring_params())
        if job_submission.status_code == 500:
            logging.info(job_submission.request.path_url)
            logging.info(job_submission.request.body)
            logging.warning("Internal Server Error While Exporting CSV Results")
            logging.warning(f"{job_submission.reason}")
            return ""
        job_submission_result: dict = job_submission.json()  # Should contain a GUID at key 'export_task_status_id'
        assert "export_task_status_id" in job_submission_result
        task_guid = job_submission_result['export_task_status_id']
        csv_guid: str = ""  # Seed with a falsey value to kick off the while loop
        csv_polls: int = 0
        while not csv_guid:
            sleep(task_polling_interval)  # give the server a chance to process the job before we query for completion.
            csv_polls += 1
            logging.debug(f"Polling attempt number {csv_polls} for the finished CSV...")

            # Send request to query if the CSV is ready for download
            export_poll = self._session.get(
                url=f"{self._base_url}/export_csv_task_status", params={"task_id": task_guid}
            )

            export_poll_results: dict = export_poll.json()
            logging.debug("%s" % export_poll_results)

            # TESTING FOR LARGE FILES
            export_status = export_poll_results.get('state', ExportStatus.IN_PROGRESS)
            if export_status == ExportStatus.COMPLETE:
                csv_guid = export_poll_results.get('exported_csv_file_id', None)
                logging.debug(f"CSV file GUID given was '{csv_guid}'")
            elif export_status == ExportStatus.NO_INCIDENTS:
                logging.debug(f"No incidents available for task {task_guid}")
                return ""
            assert csv_polls < 40  # something is pretty badly wrong if we haven't gotten it by now...
            # that or you, the library user, need to curb your task_polling_interval value...

        # The behavior of the web UI shows that the following URL will return "406 NOT ACCEPTABLE" with a
        # Location: header present. That redirection points to the URL with the token in a different format.
        # As of writing this, v31 and v35 require a ?token= qs param to access the CSV...
        # However - looks like v31(ish)/shared prod instance requires the actual token itself,
        # While the v35(ish)/staging instance uses a Location: header to redirect you to the same URL but with an
        # obfuscated-ish ?token= parameter. Tested/compared the redirect token vs the actual session token - some
        # some areas of the URL were 1:1 near the beginning, but for the most part it was totally shuffled. So:

        init_attempt_url = f"{self._base_url}/exported_csv_files/{csv_guid}"
        csv_initial_attempt = self._session.get(url=init_attempt_url, params={"token": self.__session_token})
        logging.debug(f"Made initial attempt on following CSV URL (plus ?token=....) with response"
                      f" code {csv_initial_attempt.status_code}. \n\t{init_attempt_url}")

        if "location" in csv_initial_attempt.headers:  # v35(ish?)+, we have something to work around...
            second_attempt_url = self._http_host + csv_initial_attempt.headers.get("location", "")
            logging.debug(
                f"There is a location header present. Most likely staging-ish instance with 4xx status code and"
                f" manual redirection needed. Location header is pointing to:"
                f"\n\t{second_attempt_url}")

            # FIXME: Requests not following the redirect header... is it bc the code is 4xx?
            csv_export = self._session.get(url=second_attempt_url).text

        else:  # v31(ish?), no hoop jumping needed
            logging.debug(f"CSV initial attempt worked. Most likely a prod-ish instance. Should be CSV with "
                          f"{len(csv_initial_attempt.text.splitlines()) - 1} rows of data...")
            csv_export = csv_initial_attempt.text

        if filename:
            with open(filename, 'w', newline='') as csv_file:
                csv_file.write(csv_export)

        return csv_export


        # def get_max_export_rows(self, action: CentraApiExportable) -> int:
    #     """
    #         This method fetches the maximum number of rows that the API will give back to you.
    #     """
    #     pass  # TODO Implementation

    @property
    def _http_host(self) -> str:
        """
            Generates a base URL without the presumed API directory.
            Primarily split so this can be called against Location headers.
        """
        if not (("https://" in self.hostname) or ("http://" in self.hostname)):
            host = "https://" if self.https else "http://"
            host += self.hostname
        else:
            host = self.hostname
        return host

    @property  # presents like a variable,
    def _base_url(self) -> str:  # is actually a function.
        """ Generates a base URL at the time of each API request based on SSL, API Version, and hostname. """
        return f"{self._http_host}/api/v{self.api_version}"

    def _authenticate(self, password: str, mfa_token: str = None) -> str:
        auth_attempt = self._session.post(
            url=self._base_url + "/authenticate",
            json={
                "username": self.username,
                "password": password,
                "two_factor_auth_phase": 0
            }
        )

        auth_response: dict = auth_attempt.json()

        if 'access_token' in auth_response:
            return auth_response['access_token']

        elif auth_response.get('2fa_required') and auth_response.get('2fa_temp_token'):
            auth_attempt = self._session.post(
                url=self._base_url + "/authenticate",
                json={
                    "username": self.username,
                    "password": mfa_token,  # The password field must be a TOTP token
                    "two_factor_auth_phase": 1,  # Tell API the password field is for 2nd auth factor
                    "temp_token": auth_response.get('2fa_temp_token')  # Give the token back; likely for timeouts.
                }
            )

            mfa_response: dict = auth_attempt.json()
            return mfa_response['access_token']

        else:
            raise AuthFailedException

    def __init__(self, hostname: str, username: str, password: str = None, mfa_token: str = None,
                 session_resume_token: str = None, https: bool = True, api_version: str = "3.0"):
        # TODO - Asserting username/passwd OR session resume token + checks for MFA requirement
        self.hostname: str = hostname
        self.username: str = username
        self.https: bool = https
        self.api_version: str = api_version
        self._session = requests.Session()

        self.__session_token = session_resume_token or self._authenticate(password or '', mfa_token)
        self._session.headers['Authorization'] = f"bearer {self.__session_token}"
        self._session.headers['Content-type'] = "application/json"
