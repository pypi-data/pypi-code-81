'''
Base classes for python Rundeck plugin connectors.

'''

import logging
import paramiko
from paramiko.ssh_exception import AuthenticationException, PasswordRequiredException

logger = logging.getLogger(__name__)

class BaseConnector():

    '''Abstract class for connector'''

    def __init__(self) -> None:
        pass

    def __login(self) -> bool:
        '''Connect to device and login.'''
        raise NotImplementedError

    def __logout(self) -> bool:
        '''Logout and close connection'''
        raise NotImplementedError

    def get_config(self, config:str):
        '''Should return configuration requested in yang format
        https://www.openconfig.net/projects/models/'''
        raise NotImplementedError

    def get_status(self, status:str):
        '''Should return status requested in yang format
        https://www.openconfig.net/projects/models/'''
        raise NotImplementedError

class SSHConnector(BaseConnector):

    '''SSH connector'''

    # pylint: disable=too-many-arguments
    # Even though there are too many and some could be grouped in tuples,
    # Five is too low. (Some should still be put in tuples)

    def __init__(self, hostname:str, port=22, authentication = 'password',
                 username:str='', password:str='') -> None:
        self.hostname = hostname
        self.port = port
        self.authentication = authentication
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        super().__init__()

    def __login(self):
        '''Connects to host using SSH'''
        if self.authentication == 'password':
            if self.hostname and self.username:
                if self.password:
                    logger.debug (
                        'Trying to connect with to %s with username %s and password %s',
                        self.hostname, self.username, '*****'+self.password[-1])
                    self.client.connect(
                        self.hostname, port=self.port,
                        username=self.username, password=self.password)
                else:
                    logger.error(
                        'Password authentication selected but password not provided or blank')
                    raise PasswordRequiredException
            else:
                logger.error(
                    '''Hostname or username not provided or blank. Hostname: %s\nUsername: %s''',
                    self.hostname, self.username)
                raise AuthenticationException
        else:
            raise NotImplementedError

    def __logout(self):
        '''Logout and close session'''
        self.client.close()

    def get_config(self, config:str):
        '''Should return configuration requested in yang format
        https://www.openconfig.net/projects/models/'''
        raise NotImplementedError

    def get_status(self, status:str):
        '''Should return status requested in yang format
        https://www.openconfig.net/projects/models/'''
        raise NotImplementedError

    def send_command(self, command: str) -> tuple:
        '''Sends a single command returns tuple with
        stdin, stdout, stderr'''
        try:
            self.__login()
            stdin, stdout, stderr = self.client.exec_command(command)
            return (stdin, stdout, stderr)
        finally:
            self.__logout()

    def send_commands(self, commands: list) -> dict:
        '''Sends multiple commands returns dict of tuples with
        command : stdin, stdout, stderr'''
        output = {}
        try:
            self.__login()
            for command in commands:
                stdin, stdout, stderr = self.client.exec_command(command)
                output[command] = stdin, stdout, stderr
        finally:
            self.__logout()




class RESTConnector(BaseConnector):
    '''REST connector.'''
    def __init__(self) -> None:
        logger.warning('REST connector needs implementation')
        super().__init__()

    def __login(self):
        '''Call API authentication URL and update session '''
        raise NotImplementedError

    def __logout(self):
        '''Call API logout URL'''
        raise NotImplementedError

    def get_url(self:str) -> dict:
        '''Get specified API URL return session results'''
        self.__login()
        self.__logout()
        raise NotImplementedError

    def get_urls(self, urls:list) -> dict:
        '''Get a list of specified API URLs return sessions results'''
        self.__login()
        print ('for url in {}, get response'.format(urls))
        self.__logout()
        raise NotImplementedError

    def get_config(self, config:str) -> dict:
        '''Get named configuration return configuration'''
        self.__login()
        print('get {} and return as yang'.format(config))
        self.__logout()
        raise NotImplementedError
