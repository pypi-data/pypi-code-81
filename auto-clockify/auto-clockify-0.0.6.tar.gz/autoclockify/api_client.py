from autoclockify.config import get_config
import requests


class ApiClient:
    request: any
    method: str
    endpoint: str
    arguments: any

    def __init__(self):
        self.request = None

    def getEndpointUrl(self, endpoint):
        base_url = get_config('base_url')
        return "{0}{1}".format(base_url, endpoint)

    def getMergedHeaders(self, headers=None):
        if headers is None:
            headers = {}
        headers["X-API-KEY"] = get_config('api_key')
        return headers

    def send_request(self, method, endpoint, **kwargs):
        self.method = method
        self.endpoint = endpoint
        self.arguments = kwargs
        url = self.getEndpointUrl(endpoint)
        headers = self.getMergedHeaders(kwargs["headers"])
        payload = kwargs["data"]

        print("Request: {0}: {1}".format(method, url))
        print("Headers: {0}".format(headers))
        print("Payload: {0}".format(payload))

        try:
            self.request = requests.request(method, url, headers=headers, json=payload)
        except Exception as e:
            print("Not good!")
            exit(e)

        if self.request.ok:
            print(self.request.content)
        else:
            print("Error({}): {}".format(self.request.status_code, self.request.content))
