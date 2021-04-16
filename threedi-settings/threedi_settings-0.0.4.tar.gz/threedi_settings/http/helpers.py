from urllib3.exceptions import MaxRetryError
from urllib.request import Request, urlopen
from urllib.parse import urljoin

from threedi_api_client.threedi_api_client import get_auth_token
from threedi_settings.http import api_config
from openapi_client.exceptions import ApiException

from enum import Enum
from typing import Tuple, Union
from http.client import HTTPResponse


class SwaggerSpecificationCode(int, Enum):
    ok = 0
    retrieve_auth_token_error = 1
    resp_status_error = 2
    connection_error = 3


def get_threedi_openapi_specification() -> Tuple[SwaggerSpecificationCode, Union[str, HTTPResponse]]:
    """

    """
    url = urljoin(api_config["API_HOST"], "v3.0/swagger.yaml")
    try:
        token = get_auth_token(
            api_config["API_USERNAME"],
            api_config["API_PASSWORD"],
            api_config["API_HOST"]
        )
    except MaxRetryError:
        msg = f"Failed to retrieve access token from {api_config['API_HOST']}"
        return SwaggerSpecificationCode.retrieve_auth_token_error, msg
    except ApiException as err:
        return SwaggerSpecificationCode.retrieve_auth_token_error, str(err)

    req = Request(url, None, {"Authorization": f"Bearer {token.access}"})
    try:
        resp = urlopen(req)
    except Exception as err:
        return SwaggerSpecificationCode.connection_error, str(err)
    if resp.status != 200:
        msg = f"Failed to retrieve swagger API definition from {url} Reason: {resp.reason} (code {resp.status})"
        return SwaggerSpecificationCode.resp_status_error, msg
    return SwaggerSpecificationCode.ok, resp
