from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import oauthlib
import AIH_SDK.AIHExceptions as AIHE
import time
import json



class AIHClient:
    """
    AIHClient is the client that authenticates and connects to the APIs for the given environment.
    """
    
    _instance = None
    
    @staticmethod
    def get_instance():
        if AIHClient._instance:
            return AIHClient._instance
        else:
            raise AIHE.AIHClientException('AIHClient has not been initialized yet.')
        
    
    def __init__(self, environment:str, client_id:str, client_secret:str):
        """
        IN: environment (str)   - Defines where the client should connect to.
            client_id (str)     - The id the client should connect with. 
            client_secret (str) - The secret the client should connect with.
        """
        AIHClient._instance = self
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.environment = environment
        self.token_url = f'https://{self.environment}-idsvr-we-api.azurewebsites.net/connect/token'
        
        # Creates the client
        backend = BackendApplicationClient(client_id=self.client_id)
        self.client = OAuth2Session(client=backend)
        self._update_token()
    
    
    def _is_expired(self):
        """
        Checks if the Bearer token for the OAuth2 connection is expired
        """
        
        return time.time() > self.expires_at - 10000
  
    
    def _update_token(self):
        """
        Gets a new Bearer token.
        Raises Exceptions if the specified environment or client credentials are wrong.
        """
        
        try:
            self.client.token = self.client.fetch_token(token_url=self.token_url, client_id=self.client_id, client_secret=self.client_secret)
            self.expires_at = self.client.token['expires_at']
            
        except oauthlib.oauth2.rfc6749.errors.InvalidClientError:
            raise AIHE.AIHClientException('Could not get access token. Please check client_id and client_secret.')
        
        except oauthlib.oauth2.rfc6749.errors.MissingTokenError:
            raise AIHE.AIHClientException('Could not get token. Please check the token URL.')
     
        
    def _get(self, api:str, endpoint:str, parameters:dict={}):
        """
        Sends a HTTPS GET request for the given endpoint.
        Raises an error if HTTPS error occurs.
        
        IN: api (str)         - Defines which API to use
            endpoint (str)    - Defines the endpoint send a GET request to.
            parameters (dict) - Dictionary with the parameters to include in the query.
        
        OUT: response (json) - A json object for the response
        """
        
        if(self._is_expired()):
            self._update_token()
        
        if parameters:
            params = '&'.join([f'{k}={v}' for k,v in parameters.items()])
            url = f'https://{self.environment}-{api}-we-api.azurewebsites.net/{endpoint}?{params}'   
        else:
            url = f'https://{self.environment}-{api}-we-api.azurewebsites.net/{endpoint}'
        
        response = self.client.get(url)
                
        try:
            return response.json()
        except:
            raise AIHE.AIHClientException(f'Cannot interpret response as JSON. API might be wrong.\nAPI was: {url}')
        

    def _put(self, api:str, endpoint:str, data:dict):
        """
        Sends a HTTPS PUT request for the given endpoint.
        Raises an error if HTTPS error occurs.
        
        IN: api (str)      - Defines which API to use
            endpoint (str) - Defines the endpoint send a PUT request to.
            data (dict)    - The data it should send in the body. It gets converted to json.
        """
        
        if(self._is_expired()):
            self._update_token()
        
        url = f'https://{self.environment}-{api}-we-api.azurewebsites.net/{endpoint}' 
        headers = {"Content-Type": "application/json"}
        response = self.client.put(url=url, data=json.dumps(data), headers=headers)
        
        if response.status_code < 200 or response.status_code >= 300:
            raise AIHE.AIHClientException(f'PUT request failed: {response.status_code}\n{response.text}')
        
        
    def _post(self, api:str, endpoint:str, data:dict):
        """
        Sends a HTTPS POST request for the given endpoint.
        Raises an error if HTTPS error occurs.
        
        IN: api (str)      - Defines which API to use
            endpoint (str) - Defines the endpoint send a PUT request to.
            data (dict)    - The data it should send in the body. It gets converted to json.
            
        OUT: (json)        - The response from the server in a json object
        """
        
        if(self._is_expired()):
            self._update_token()
        
        url = f'https://{self.environment}-{api}-we-api.azurewebsites.net/{endpoint}' 
        headers = {"Content-Type": "application/json"}
        response = self.client.post(url=url, data=json.dumps(data), headers=headers)
        
        if response.status_code < 200 or response.status_code >= 300:
            raise AIHE.AIHClientException(f'POST request failed: {response.status_code}\n{response.text}')
            
        try:
            return response.json()
        except:
            raise AIHE.AIHClientException(f'Cannot interpret response as JSON. API might be wrong.\nAPI was: {url}')
            
            
    def _delete(self, api:str, endpoint:str, id:str):
        """
        Sends a HTTPS DELETE request for the given endpoint.
        Raises an error if HTTPS error occurs.
        
        IN: api (str)      - Defines which API to use
            endpoint (str) - Defines the endpoint send a GET request to.
        """
        
        if(self._is_expired()):
            self._update_token()
        
        url = f'https://{self.environment}-{api}-we-api.azurewebsites.net/{endpoint}/{id}'        
        response = self.client.delete(url)
        
        if response.status_code < 200 or response.status_code >= 300:
            raise AIHE.AIHClientException(f'DELETE request failed: {response.status_code}\n{response.text}')
        
            
    def _download_file(self, file_id:str):
        """
        download_file downloads the file from DataUpload API.
        
        IN: file_id (str) - The id for the file to download.
        
        OUT: (content) - The response content.
        """
        
        if(self._is_expired()):
            self._update_token()
        
        url = f'https://{self.environment}-du-we-api.azurewebsites.net/files/download/{file_id}'
        response = self.client.get(url)

        return response.content

        
    def _upload_file(self, datatype_id:str, file, name:str):
        """
        upload_file uploads a file for a DataType to the DataUpload API.

        IN: datatype_id (str) - The id of the DataType to uplaod the file to.
            file (bytes)      - The bytes for the file to upload.
            name (str)        - The name the file should be stored as. The name must include the file extension.

        OUT: (json) - The json response
        """

        if(self._is_expired()):
            self._update_token()
        
        fileextension = name.split('.')[-1]
        url = f'https://{self.environment}-du-we-api.azurewebsites.net/Files'
        files = {
            'Id' : (None, ''),
            'DataTypeId' : (None, datatype_id),
            'File' : (name, file, f'image/{fileextension}')
        } 
        
        response = self.client.post(url=url, files=files)
        
        return response.json()


    def _download_media(self, container:str, name:str):
        """
        To get download a file from the media objects.
        IN: container (str) - To specify the type of file to donwload e.g. image
            name (str) - To specify the name of the file to download
            
        OUT: the content of the downloaded file
        """
        if(self._is_expired()):
            self._update_token()
        
        url = f'https://{self.environment}-aih-we-api.azurewebsites.net/api/v1/multimedia/{container}/{name}'        
        response = self.client.get(url)
                
        return response.content


    def _upload_media(self, container, file, name):
        """
        upload_file uploads a file to a data type.

        IN: datatype_id (str) - The id of the DataType to uplaod the file to.
            file (bytes)      - The bytes for the file to upload.
            name (str)        - The name the file should be stored as. The name must include the file extension.

        OUT: (json) - The json response
        """
        
        if(self._is_expired()):
            self._update_token()
        
        
        url = f'https://{self.environment}-aih-we-api.azurewebsites.net/api/v1/media'
        #url = f'https://{self.environment}-aih-we-api.azurewebsites.net/api/v1/multimedia/upload/{container}'
        
        files = {'file' : (name, file)}
        
        response = self.client.post(url=url, files=files)
        
        return response.json()
        
        