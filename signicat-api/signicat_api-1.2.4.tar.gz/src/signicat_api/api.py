import requests

from .request_types import *
from requests.auth import HTTPBasicAuth


class SignicatAPI:
    PDF_DOCUMENT_TYPE = 'application/pdf'

    def __init__(self, url, basic_auth_user: str, basic_auth_password: str):
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.url = url
        self.access_token = None
        self.basic_auth_user = basic_auth_user
        self.basic_auth_password = basic_auth_password

    def __url(self, url):
        return self.url + url

    def __authorize(self):
        """
        Perform authentication call to create access token.
        Token will be stored in access_token property.
        """
        r = requests.post(self.__url('/oidc/token'),
                          auth=HTTPBasicAuth(self.basic_auth_user, self.basic_auth_password),
                          headers={
                              'Content-Type': 'application/x-www-form-urlencoded'
                          },
                          data={
                              'scope': 'client.signature',
                              'grant_type': 'client_credentials'
                          })

        self.access_token = r.json()['access_token']

    def __to_json(self, response):
        return response.json()

    @staticmethod
    def from_json(data, type):
        return json.loads(data, object_hook=lambda d: type(**d))

    def __set_headers(self, need_auth=True):
        if need_auth:
            self.headers['Authorization'] = 'Bearer {0}'.format(self.access_token)

    def __get(self, url, need_auth=True):
        self.__authorize()
        self.__set_headers(need_auth)

        return requests.get(self.__url(url), headers=self.headers)

    def __post(self, url, data=None, need_auth=True):
        self.__authorize()
        self.__set_headers(need_auth)

        return requests.post(self.__url(url), headers=self.headers, data=data)

    def post_upload_one_document(self, document_file: bytes, document_content_type: str = PDF_DOCUMENT_TYPE):
        """
        Upload one document to receive documentIds
        """
        self.headers['Content-Type'] = document_content_type
        response = self.__post('/sign/documents', data=document_file)
        self.headers['Content-Type'] = 'application/json'
        return response.status_code, self.__to_json(response)

    def post_sign_order(self, sign_order: SignOrder):
        """
        Create sign order
        """
        response = self.__post('/sign/orders', data=sign_order.to_json())
        return response.status_code, self.__to_json(response)

    def get_task_events(self, order_id: str, task_id: str):
        """
        Get all events related to a task
        """
        response = self.__get('/sign/orders/{0}/tasks/{1}/events'.format(order_id, task_id))
        return response.status_code, self.__to_json(response)

    def get_packaging_task_result_document(self, order_id: str, task_id: str):
        """
        Get document related to packaging task by order id
        """
        response = self.__get('/sign/orders/{0}/packaging-tasks/{1}/result'.format(order_id, task_id))
        return response.status_code, self.__to_json(response)

    def get_signing_order(self, order_id: str) -> (int, SignOrder):
        """
        Get the signing order with the given ID
        """
        response = self.__get('/sign/orders/{0}'.format(order_id))

        return response.status_code, self.__to_json(response)

    def get_document(self, document_id: str) -> (int, bytes):
        """
        Download document
        """
        response = self.__get('/sign/documents/{0}'.format(document_id))
        return response.status_code, response.content
