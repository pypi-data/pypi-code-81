import copy
from src.exceptions.proxy_exception import ProxyException
from src.utils.file_to_string_utils import FileToStringUtils


class Proxy:

    session = None
    http_client = None

    def __init__(self, http_client, session):
        self.session = session
        self.http_client = http_client

    """
	Clears the har log of any captured requests/responses currently stored in the proxy
	memory. If you have a long running test session, it is a good idea to regularly
	clear the har log to prevent proxy crashes.
	
	:raises ProxyException: If the session har log cannot be cleared.
	"""
    def clear_har_log(self):
        session = copy.deepcopy(self.session)
        session['action'] = 'clear_har_log'
        self.__handler(self.http_client.post_to_server('proxy', session))

    """
	Gets the har log of all requests/responses from app launch, or from
	the last time the har log was cleared.
	
	:returns: Path to the har file..
	:raises ProxyException: If the proxy har data cannot be retrieved.
	"""
    def get_har_log(self):
        session = copy.deepcopy(self.session)
        session['action'] = 'get_har_log'
        proxy_json = self.__handler(
            self.http_client.post_to_server('proxy', session))
        return FileToStringUtils().save_string_to_file(proxy_json['har_log'], '.har')

    def __handler(self, element_json):
        if element_json['results'] != 'success':
            raise ProxyException(element_json['results'])
        return element_json
