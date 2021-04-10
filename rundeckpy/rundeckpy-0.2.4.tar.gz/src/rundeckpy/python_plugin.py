'''
Base classes for python based Rundeck plugin.

'''

import os
import sys
import logging
import pprint
from .python_connectors import SSHConnector, RESTConnector

logger = logging.getLogger(__name__)

class PythonPlugin:

    '''Base class for Rundeck python plugin'''

    # pylint: disable=too-many-instance-attributes
    # Even though there are too many and some could be grouped in tuples,
    # Seven is too low. (Some should still be put in tuples)

    def __init__(self):
        self.condition = os.environ.get('RD_CONFIG_CONDITION', 'Always')
        logger.debug('Condition set : %s', self.condition)
        self.a_var = os.environ.get('RD_CONFIG_A_VAR')
        self.b_var  = os.environ.get('RD_CONFIG_B_VAR')
        self.execute = self.conditionals_continue()
        self.output = {}
        debug_level = os.environ.get('RD_CONFIG_DEBUG_LEVEL', 'ERROR')
        level = logging.getLevelName(debug_level)
        self.job_project = os.environ.get('RD_JOB_PROJECT', '')
        self.job_username = os.environ.get('RD_JOB_USERNAME', '')
        self.nodename = os.environ.get('RD_NODE_NAME', '')
        self.hostname = os.environ.get(
            'RD_OPTION_HOSTNAME',
            os.environ.get('RD_NODE_HOSTNAME', '127.0.0.1'))
        self.ssh_username = os.environ.get(
            'RD_OPTION_SSH_USERNAME',
            os.environ.get('RD_NODE_USERNAME', ''))
        self.ssh_authentication = os.environ.get(
            'RD_OPTION_SSH_AUTHENTICATION',
            os.environ.get('RD_NODE_SSH_AUTHENTICATION', 'password'))
        self.ssh_password = os.environ.get(
            'RD_PRIVATE_SSH_PASSWORD',
            os.environ.get('RD_OPTION_SSH_PASSWORD_STORAGE_PATH',
            os.environ.get('RD_NODE_SSH_PASSWORD_STORAGE_PATH', '')))
        self.ssh_key = os.environ.get(
            'RD_PRIVATE_SSH_KEY',
            os.environ.get('RD_OPTION_SSH_KEY_STORAGE_PATH',
            os.environ.get('RD_NODE_SSH_KEY_STORAGE_PATH', '')))
        self.ssh_passphrase = os.environ.get(
            'RD_PRIVATE_SSH_PASSPHRASE',
            os.environ.get('RD_OPTION_SSH_PASSPHRASE_STORAGE_PATH',
            os.environ.get('RD_NODE_SSH_PASSPHRASE_STORAGE_PATH', '')))
        self.ssh_port = os.environ.get(
            'RD_OPTION_SSH_PORT',
            os.environ.get('RD_NODE_SSH_PORT', 22))
        self.jumphost = os.environ.get(
            'RD_OPTION_JUMPHOST',
            os.environ.get('RD_NODE_JUMPHOST',
            os.environ.get('RD_NODE_LEC', '')))
        self.jumphost_username = os.environ.get(
            'RD_OPTION_JUMPHOST_USERNAME',
            os.environ.get('RD_NODE_JUMPHOST_USERNAME', ''))
        self.jumphost_ssh_authentication = os.environ.get(
            'RD_OPTION_JUMPHOST_SSH_AUTHENTICATION',
            os.environ.get('RD_NODE_JUMPHOST_SSH_AUTHENTICATION', 'password'))
        self.jumphost_ssh_password = os.environ.get(
            'RD_PRIVATE_JUMPHOST_PASSWORD',
            os.environ.get('RD_OPTION_JUMPHOST_SSH_PASSWORD_STORAGE_PATH',
            os.environ.get('RD_NODE_JUMPHOST_SSH_PASSWORD_STORAGE_PATH', '')))
        self.jumphost_ssh_key = os.environ.get(
            'RD_PRIVATE_SSH_KEY',
            os.environ.get('RD_OPTION_JUMPHOST_SSH_KEY_STORAGE_PATH',
            os.environ.get('RD_NODE_JUMPHOST_SSH_KEY_STORAGE_PATH', '')))
        self.jumphost_ssh_passphrase = os.environ.get(
            'RD_PRIVATE_JUMPHOST_SSH_PASSPHRASE',
            os.environ.get('RD_OPTION_JUMPHOST_SSH_PASSPHRASE_STORAGE_PATH',
            os.environ.get('RD_NODE_JUMPHOST_SSH_PASSPHRASE_STORAGE_PATH', '')))
        self.jumphost_ssh_port = os.environ.get(
            'RD_OPTION_JUMPHOST_SSH_PORT',
            os.environ.get('RD_NODE_JUMPHOST_SSH_PORT', 22))
        self.connection = os.environ.get('RD_CONFIG_CONNECTION', 'SSH')
        if self.connection == 'SSH':
            self.connector = SSHConnector(
                hostname=self.hostname, port=self.ssh_port,
                authentication=self.ssh_authentication,
                username=self.ssh_username, password=self.ssh_password)
        elif self.connection == 'API':
            self.connector = RESTConnector()
        if os.environ.get('RD_JOB_LOGLEVEL') == 'DEBUG':
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=level)
        if not self.execute:
            self.output['warning'].append('Condition set to never. Step not executed.')
            logger.warning('Conditional execution not satisfied. Closing')
            sys.exit(0)


    def conditionals_continue(self) -> bool:
        '''Check conditionals require execution. Exit if not.'''
        if self.condition == 'Always':
            return True
        return False

    def print_output(self, out_format:str='dict'):
        '''Print output attribute with requuired formatting '''
        if isinstance(self.output, dict) and out_format == 'text':
            for key, value in self.output:
                print(key)
                print('  ', value)
        elif isinstance(self.output, dict) and out_format == 'dict':
            pprint.pprint(self.output, indent=4)
        elif isinstance(self.output, dict) and out_format == 'dict':
            print (self.output)
        else:
            print (self.output)
