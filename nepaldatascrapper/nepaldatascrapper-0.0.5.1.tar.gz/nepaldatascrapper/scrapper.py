import requests

class Scrapper:
    """
    Base class designed to scrap data as if user is using browser to get the data
    """

    def __init__(self, source, endpoints):
        self.source = source
        self.endpoints = endpoints

    def createParameter(self, endpoint, **kwargs):
        """
        create parameter of specific endpoint
        :param endpoint: the endpoint that we need to get data from
        :type endpoint: str
        :rtype: dict
        """
        postData = self.endpoints[endpoint]["parameter"]
        for par in postData:
            if par in kwargs:
                postData[par] = kwargs.get(par)
        return postData

    def post(self, endpoint, **kwargs):
        """
        send the post request on specific endpoint

        :param endpoint: the endpoint that we need to get data from
        :type endpoint: str

        :rtype: response
        """
        response = requests.post(self.getEndpoint(endpoint), json=kwargs, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
        return response

    def get(self, endpoint, **kwargs):
        """
        send the get request on specific endpoint

        :param endpoint: the endpoint that we need to get data from
        :type endpoint: str
        
        :rtype: response
        """
        response = requests.get(self.getEndpoint(endpoint), params=kwargs, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "*/*"}, verify=False)
        return response

    def getEndpoint(self, endpoint):
        """
        get the url where data is to be fetched
        
        :param endpoint: the endpoint that we need to get data from
        :type endpoint: str
        
        :rtype: str
        """
        return self.source + self.endpoints[endpoint]["endpoint"]
