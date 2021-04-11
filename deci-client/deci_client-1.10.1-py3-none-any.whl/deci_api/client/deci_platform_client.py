import requests

from deci_client.deci_api import ApiClient, Configuration, ApiException
from deci_client.deci_api.api.platform_api import PlatformApi
from deci_client.deci_api.models import ModelMetadata, AddModelResponse


def get_docstring_from(original_function):
    """
    A decorator that attaches the docstring one function to another function in real time (for transparent auto completion).
    """

    def doc_wrapper(target):
        target.__doc__ = original_function.__doc__
        return target

    return doc_wrapper


class DeciPlatformClient(PlatformApi):
    """
    A wrapper for OpenAPI's generated client http library to deci's API.
    Extends the functionality of generated platform client and ease it's usage and experience.
    """

    def __init__(self, api_host='api.deci.ai', api_port=443, https=True):
        """
        :param api_host: The host of deci's platform HTTP API.
        :type api_host: str
        :param api_host: The port of deci's platform HTTP API.
        :type api_port: int
        :param https: Whether to use https instead of HTTP. Using https Will add latency.
        :type https: bool
        """

        assert isinstance(api_port, int), 'The api_port must be an int object'
        endpoint_host = '{api_host}:{api_port}'.format(api_host=api_host, api_port=api_port)
        self._api_host = api_host
        self._endpoint_host = endpoint_host
        if https:
            base_url = 'https://{endpoint}'.format(endpoint=endpoint_host)
        else:
            base_url = 'http://{endpoint}'.format(endpoint=endpoint_host)

        self._base_url = base_url
        client_config = ApiClient(configuration=Configuration(host=base_url))
        super().__init__(client_config)

    def login(self, username: str, password: str):
        """
        Login to the platform.
        """
        token = super(DeciPlatformClient, self).login(username, password)
        authorization_header = ' '.join([token.token_type, token.access_token])
        self.api_client.default_headers['Authorization'] = authorization_header
        print('Successfully logged in to the platform.')

    def logout(self):
        """
        Log out of the platform (Disposes the credentials).
        """
        self.api_client.default_headers.pop('Authorization')

    def add_model(self, add_model_request: ModelMetadata, model_local_path: str, **kwargs):
        """
        Adds a new model to the company's model repository.
        The new model arguments are passed to the API, and the model itself is uploaded to s3 from the local machine.
        :param add_model_request: The model metadata
        :param model_local_path: The path of the model on the local operating system.
        """
        with open(model_local_path, 'rb') as f:
            # Upload the model to the s3 bucket of the company
            signed_url_upload_request = self.get_model_signed_url_for_upload(model_name=add_model_request.name)
            upload_request_parameters = signed_url_upload_request.data
            requests.post(upload_request_parameters['url'], data=[])

            # Making sure the model arguments are OK before uploading the file
            try:
                super(DeciPlatformClient, self).assert_model_arguments(model_metadata=add_model_request)
            except ApiException as e:
                print(f'Found bad arguments: {e}')
                raise e

            print('Uploading the model file...')
            files = {'file': (upload_request_parameters['fields']['key'], f)}
            http_response = requests.post(upload_request_parameters['url'],
                                          data=upload_request_parameters['fields'],
                                          files=files)

            # Getting the s3 created Etag from the http headers, and passing it to the 'add_model' call
            s3_file_etag = http_response.headers.get('ETag')  # Verify the model was uploaded
            http_response.raise_for_status()
            print('Finished uploading the model file.')

            # Adding the model metadata via the API, after verification that the file exists.
            add_model_response: AddModelResponse = super(DeciPlatformClient, self).add_model(
                model_metadata=add_model_request,
                etag=s3_file_etag,
                **kwargs)

            new_model_id = add_model_response.data.model_id
        print('Successfully added the model to the repository.')
        return add_model_response

    def download_model(self, model_id: str, download_to_path: str):
        """
        Downloads a model with the specified UUID to the specified path.
        :param model_id: The model UUID
        :download_path: The full path to which the model will be written to.
        """
        download_url = self.get_model_signed_url_for_download(model_id)
        with open(download_to_path, 'wb') as model_file:
            print('Downloading the model file...')
            model_request = requests.get(download_url.data, stream=True)
            model_request.raise_for_status()
            for model_chunk in model_request.iter_content():
                if model_chunk:
                    model_file.write(model_chunk)
            print(f'Finished downloading the model file. The model is located at {download_to_path}')
        return True
