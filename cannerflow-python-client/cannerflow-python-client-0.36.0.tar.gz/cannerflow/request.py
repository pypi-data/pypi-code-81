import sys
import functools
import requests
from typing import Optional
from http import HTTPStatus
from requests.models import Response
from cannerflow.exceptions import CannerflowError, HttpError
from cannerflow.logging import get_logger

__all__ = ["CannerRequest"]
# close detail error traceback.
sys.tracebacklimit = 0
logger = get_logger("CannerRequest")


class CannerRequest:
    def __init__(self, endpoint: str, headers: Optional[dict] = None):
        self._endpoint = endpoint
        self._headers = headers

    # The decorator for catching and show message
    def _handle_exception(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                response = func(self, *args, **kwargs)
                return response
            except CannerflowError as err:
                logger.error(
                    f"Error occurred => code: {err.error_code}, message: {err.message}"
                )
                raise err
            except Exception as err:
                # Connection error (exceptions from requests package.)
                logger.error(f"Error occurred => {err}")
                raise err

        return wrapper

    def _parse_graphql(self, resp: Response):
        # handle non 200 error (not from cannerflow backend graphql e.g: some middlewares)
        if resp.status_code != HTTPStatus.OK:
            # Check the graphql response error format
            if resp.content and "code" in resp.json():
                error = resp.json()
                raise CannerflowError(
                    error_code=error["code"], message=error["message"]
                )
            raise HttpError(message=resp.content)
        else:
            result = resp.json()
            # handle graphql error (status code is 200, but check error from errors)
            if "errors" in result:
                error = result["errors"][0]
                raise CannerflowError(
                    error_code=error["extensions"]["code"], message=error["message"]
                )
            data = result.get("data")
            return data

    def _parse_restful(self, resp: Response):
        if resp.status_code != HTTPStatus.OK:
            # Check the restful response error format
            if resp.content and "code" in resp.json():
                error = resp.json()
                raise CannerflowError(
                    error_code=error["code"], message=error["message"]
                )
            raise HttpError(message=resp.content)
        # If status code is 200 or not 200
        data = resp.json()
        return data

    @_handle_exception
    def graphql_exec(self, payload: dict):
        """
        The graphql request method
        """
        graphql_url = f"{self._endpoint}/graphql"
        resp: Response = requests.post(
            url=graphql_url, json=payload, headers=self._headers
        )
        return self._parse_graphql(resp)

    @_handle_exception
    def get(self, path: str):
        """
        The restful HTTP Get request method
        """
        rest_url = f"{self._endpoint}/{path}"
        resp: Response = requests.get(url=rest_url, headers=self._headers)
        return self._parse_restful(resp)
