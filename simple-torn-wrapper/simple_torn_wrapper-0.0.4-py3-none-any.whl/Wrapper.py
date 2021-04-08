import logging
from requests import get
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TornAPIError(Exception):
    def __init__(self, url, response, message=None):
        if message:
            super(TornAPIError, self).__init__(message)
        else:
            super(TornAPIError, self).__init__("Exception raised when there is an error in the TornAPI response.\n"
                                               f"Url requested: {url}.\n"
                                               "Test your request here: https://www.torn.com/api.html#")

        self.error_code = response['error']


class TornAPIRateError(TornAPIError):
    def __init__(self, url, response):
        super(TornAPIRateError, self).__init__(url,
                                               response,
                                               message="Exception raised when you reach the TornAPI rate limit.\n"
                                               f"Url requested: {url}.\n"
                                               "Test your request here: https://www.torn.com/api.html#")

        self.error_code = response['error']


class TornWrapper:
    """A wrapper class for the Torn API"""

    request_string = "https://api.torn.com/{section}/{id}"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def request(self, section: str, req_id='', selections=None, **kwargs):
        """Sends a request to the Torn API.

        Args:
            section (str): the section of the Torn API for the request to be made to the
            req_id (int, optional): the ID of the data that needs to be requested.
            selections (list, optional): a list of selections from the section of the Torn API
            **kwargs: extra keyword args that will be passed as params to the request.

                Note that tsfrom, and tsto will reference the API search to and from a timestamp
                If a datetime is passed as these parameters it will be converted to a timestamp.


        Returns:
            dict: A Python dictionary of the data from the Torn API

        Raises:
            TornAPIError: If the request is bad, raises a TornAPIError

        """
        if selections is None:
            selections = []

        request_url = self.request_string.format(section=section,
                                                 id=str(req_id))

        main_data = dict(selections=','.join(selections),
                         key=self.api_key)

        # Handle if to/from in kwargs => convert to a timestamp.
        for extra_arg in ['tsto', 'tsfrom']:
            if extra_arg in kwargs:
                value = kwargs.pop(extra_arg)
                extra_arg = extra_arg[2:]
                kwargs[extra_arg] = value
                if isinstance(kwargs[extra_arg], datetime):
                    kwargs[extra_arg] = kwargs[extra_arg].timestamp()

        # Join the main_data with the extra options in kwargs
        data = main_data | kwargs
        logger.info(data)

        # Get the response from torn
        response = get(
            url=request_url,
            params=data
        ).json()

        # Send request_url and data to logger
        logger.debug(f' GET: {request_url} DATA: {str(data)}')
        logger.debug(f' RESPONSE: {str(response)}')

        # Handle error in request
        if 'error' in response:
            if '5' in response['error']:
                raise TornAPIRateError(request_url, response)
            else:
                raise TornAPIError(request_url, response)

        return response
