import requests

class SOAPSnow:

    def __init__(self,
        username: str,
        password: str,
        instance: str
    ):
        self.username = username
        self.password = password
        self.instance = instance

    @property
    def xml_head(self):
        '''
        Returns XML payload head.
        '''
        return (
            '<soapenv:Envelope '
            'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
            'xmlns:x="http://www.service-now.com/"><soapenv:Body>'
        )

    @property
    def xml_tail(self):
        '''
        Returns XML payload tail.
        '''
        return '</soapenv:Body></soapenv:Envelope>'

    @property
    def auth(self):
        '''
        Returns self.username and self.password as a tuple.
        '''
        return (self.username, self.password)

    def __url(self, **kwargs):
        '''
        Returns formatted request URL.
        '''
        url = (
            f'https://{self.instance}.service-now.com/'
            f'{kwargs.get("endpoint")}.do?SOAP'
        )

        if (dvl := kwargs.get('display_value')):
            url += f'&displayvalue={dvl}'

        if (dvr := kwargs.get('display_variables')):
            url += f'&displayvariables={dvr}'

        if (aev := kwargs.get('allow_empty_value')):
            url += f'&allow_empty_value={aev}'

        return url

    def __payload_to_xml(self, data: dict):
        '''
        Returns request payload dict in XML format.
        '''
        xml = [f'<{k}>{v}</{k}>' for k, v in data.items()]
        return ''.join(xml)

    def request(self,
        method: str,
        endpoint: str,
        display_value: str = None,
        display_variables: str = None,
        allow_empty_value: str = None,
        payload: dict = None
    ):
        '''
        Posts request and returns response.
        '''
        data = (
            f'{self.xml_head}'
            f'<x:{method}>'
            f'{self.__payload_to_xml(payload)}'
            f'</x:{method}>'
            f'{self.xml_tail}'
        )
        url = self.__url(
            endpoint=endpoint,
            display_value=display_value,
            display_variables=display_variables,
            allow_empty_value=allow_empty_value
        )
        return requests.post(url=url, data=data, auth=self.auth)