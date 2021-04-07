import logging
from requests import request

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TornAPIError(Exception):
    def __init__(self, url, response):
        super(TornAPIError, self).__init__("Exception raised when there is an error in the TornAPI response.\n"
                                           f"Url requested: {url}.\n"
                                           f"Test your request here: https://www.torn.com/api.html#")

        self.error_code = response['error']


class TornWrapper:
    request_string = "https://api.torn.com/{section}/{id}?selections={selection}&key={api_key}"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def request(self, section: str, id_='', selections=None):
        if selections is None:
            selections = []

        request_url = self.request_string.format(section=section,
                                                 id=str(id_),
                                                 selection=','.join(selections),
                                                 api_key=self.api_key)

        logger.debug('Request: '+request_url)
        data = request(
            method='get',
            url=request_url
        ).json()

        if 'error' in data:
            raise TornAPIError(request_url, data)

        return data


