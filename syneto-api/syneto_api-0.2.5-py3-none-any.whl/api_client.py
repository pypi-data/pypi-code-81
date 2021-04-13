import os
import requests
import urllib.parse
import logging

from .settings import get_env_flag

logger = logging.getLogger(__name__)


def make_url(url_base, *path_args, query_args: dict = None, **path_kwargs):
    path_args = [urllib.parse.quote(v, safe="") for v in path_args]
    path_kwargs = {k: urllib.parse.quote(v, safe="") for k, v in path_kwargs.items()}
    path = url_base.format(*path_args, **path_kwargs)

    if query_args is None or len(query_args) == 0:
        return path
    query_string = urllib.parse.urlencode(
        query_args, doseq=True, quote_via=urllib.parse.quote
    )
    return f"{path}?{query_string}"


class APIException(Exception):
    def __init__(
        self, url: str, status_code: int = 0, request_body: dict = None, response=None
    ):
        self.url = url
        self.status_code = status_code
        self.request_body = request_body
        self.response = response
        message = f"API Error: {self.url}"
        if self.status_code and self.response is not None:
            message = (
                f"API {self.url} returned HTTP {self.status_code}: {self.response.text}"
            )
        super().__init__(message)


class APIClientBase:
    SUCCESS_CODES = {
        "GET": [200],
        "POST": [200, 201, 202],
        "PUT": [200, 202],
        "PATCH": [200, 202],
        "DELETE": [200, 202, 204],
    }

    def __init__(self, url_base=None, default_protocol="http", insecure_ssl=None):
        self.url_base = url_base
        protocols = ["http://", "https://"]
        if not any(self.url_base.lower().startswith(p) for p in protocols):
            self.url_base = f"{default_protocol}://{self.url_base}"

        self.url_base = self.url_base.rstrip("/")

        self.headers = {}
        self._verify_ssl_cert = True
        if insecure_ssl is not None:
            self.set_insecure_ssl(insecure_ssl)
        elif get_env_flag("ALLOW_INSECURE_SSL"):
            self.set_insecure_ssl(True)

    def _request(
        self,
        method: str,
        relative_url: str,
        *args,
        query_args: dict = None,
        body: dict = None,
        success_codes: list = None,
        **kwargs,
    ):
        relative_url = relative_url.lstrip("/")
        url = make_url(
            self.url_base + "/" + relative_url, *args, query_args=query_args, **kwargs
        )
        logger.debug(f"Calling {method} {url}")

        if not success_codes:
            success_codes = APIClientBase.SUCCESS_CODES[method]

        method_func = self._get_method_func(method)
        method_args = {"verify": self._verify_ssl_cert}
        if self.headers is not None and len(self.headers) > 0:
            method_args["headers"] = self.headers

        if body is not None:
            method_args["json"] = body

        try:
            response = method_func(url, timeout=20, **method_args)
            if response.status_code in success_codes:
                logger.debug(f"Received {response.status_code} from {method} {url}")
                return response.json()

            logger.info(f"Received {response.status_code} from {method} {url}")
            raise APIException(
                url=url,
                status_code=response.status_code,
                request_body=body,
                response=response,
            )

        except APIException as e:
            raise

        except TypeError:
            raise

        except Exception as e:
            logger.warning(f"Failed {method} request to {url}: {str(e)}")
            raise APIException(url=url, request_body=body,) from e

    def _get_method_func(self, method):
        requests_methods = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "PATCH": requests.patch,
            "DELETE": requests.delete,
        }
        return requests_methods[method]

    def get_request(
        self,
        relative_url: str,
        *url_path_args,
        query_args: dict = None,
        success_codes: list = None,
        **url_path_kwargs,
    ):
        return self._request(
            "GET",
            relative_url,
            *url_path_args,
            query_args=query_args,
            success_codes=success_codes,
            **url_path_kwargs,
        )

    def delete_request(self, *args, **kwargs):
        # Same args as get_request
        return self._request("DELETE", *args, **kwargs)

    def post_request(
        self,
        relative_url: str,
        *url_path_args,
        query_args: dict = None,
        body: dict = None,
        success_codes: list = None,
        **url_path_kwargs,
    ):
        return self._request(
            "POST",
            relative_url,
            *url_path_args,
            query_args=query_args,
            body=body,
            success_codes=success_codes,
            **url_path_kwargs,
        )

    def put_request(self, *args, **kwargs):
        # Same args as post_request
        return self._request("PUT", *args, **kwargs)

    def patch_request(self, *args, **kwargs):
        # Same args as post_request
        return self._request("PATCH", *args, **kwargs)

    def set_insecure_ssl(self, insecure=True):
        self._verify_ssl_cert = not insecure

    def set_auth_jwt(self, jwt):
        self.headers["Authorization"] = f"Bearer {jwt}"
