# -*- coding: utf-8 -*-
"""
Description:
    This module contains all of the ssh util used for a test framework.

Author:
    Ray Gomez

Date:
    12/7/20
"""

import os
import socket
import time

import paramiko
from scp import SCPClient

from epython import errors
from epython.environment import _LOG, EPYTHON_SSH_RETRIES, EPYTHON_SSH_RETRY_INTERVAL
from epython import handlers

# The base list of exceptions to retry on
# (NOTE: This is meant to only handle connection-related errors, not authentication issues)
SSH_CONN_EXCEPTIONS = (paramiko.ssh_exception.ChannelException,
                       paramiko.ssh_exception.NoValidConnectionsError,)


# pylint: disable=W0703
class SSHConnect:
    """SSH Helper class that provides a context manager.

    NOTE: This could have been done with a @contextmanager decorator, but was done as a class for future
    extensibility.
    """

    def __init__(self, host, username, password, port=22, pkey=None):
        """ The SSHConnect helper class is used solely to provide a context manager for ssh
        operations.

        Args:
            host (str): The host that is being logged into
            username (str): The username to use to log into the host
            password (str): The password for the provided username
            port (int): The port to connect ssh over
            pkey (str): The path to the ssh key to use
        """
        self.host = host
        self.username = username
        self.password = password
        self.client = None

        self.port = port

        # Set the public key to use
        self.pkey = None
        self.pkey_path = pkey
        if self.pkey_path:
            # Read key location
            if not os.path.exists(self.pkey_path):
                raise errors.ssh.SSHKeyNotFound(f"Failed to find ssh key at: {self.pkey_path}")
            self.pkey_path = os.path.expanduser(self.pkey_path)

            # If it's not an RSA key, try an ECDSA key.
            try:
                self.pkey = paramiko.RSAKey.from_private_key_file(self.pkey_path)
                _LOG.debug("RSA Key has been selected for use with paramiko")
            except Exception:
                self.pkey = paramiko.ECDSAKey.from_private_key_file(self.pkey_path)
                _LOG.debug("ECDSA Key has been selected for use with paramiko")

    def __enter__(self):

        # Make sure we automatically register the keys
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self.client.connect(self.host, username=self.username, password=self.password,
                                port=self.port, pkey=self.pkey)
        except Exception as exp:
            # Let's raise our internal SSHError to simplify retries for issues related to ssh connections
            raise errors.ssh.SSHError(f"Failed to connect to '{self.host}' due to:\n{exp}") from exp

        return self.client

    def __exit__(self, *exc):
        # Ignore any errors during the disconnect
        try:
            self.client.close()
        except Exception:
            pass
        self.client = None
# pylint: enable=W0703


# Probably need both local and remote checks
@handlers.basic_retry_handler(SSH_CONN_EXCEPTIONS,
                              retries=EPYTHON_SSH_RETRIES,
                              interval=EPYTHON_SSH_RETRY_INTERVAL)
def execute_command(host, username, password, cmd, port=22, pkey=None, banner=False):
    """Execute a given command on a host over ssh.

    Args:
        host (str): The host that is being logged into
        username (str): The username to use to log into the host
        password (str): The password for the provided username
        cmd (str): The command to execute on the host
        port (int): The port to connect ssh over
        pkey (str): The path to the ssh key to use
        banner (bool): Whether or not to display the results in an info statement (as opposed to debug)

    Returns:
        (tuple): RC, Standard Out, Standard Error
    """
    ret_code = None

    with SSHConnect(host, username, password, port=port, pkey=pkey) as client:
        # Execute the command and get the goodies
        _, stdout, stderr = client.exec_command(cmd)

        try:
            ret_code = stdout.channel.recv_exit_status()
        except Exception as exp:
            _LOG.error("Failed to recieve return code due to:\n%s", exp)
            raise errors.ssh.SSHError("Failed retrieving RC!")

        try:
            stdout = stdout.read().decode().strip()
        except Exception as exp:
            _LOG.error("Failed to read stdout due to:\n%s", exp)
            raise errors.ssh.SSHStreamDecodeError("Failed decoding stdout stream!")

        try:
            stderr = stderr.read().decode().strip()
        except Exception as exp:
            _LOG.error("Failed to read stderr due to:\n%s", exp)
            raise errors.ssh.SSHStreamDecodeError("Failed decoding stderr stream!")

        msg = (f"Results from executed command:\n"
               f"\tHOST: {host}\n"
               f"\tCMD: {cmd}\n"
               f"\tRC: {ret_code}\n"
               f"\tSTDOUT: {stdout}\n"
               f"\tSTDERR: {stderr}")
        if banner:
            _LOG.info(msg)
        else:
            _LOG.debug(msg)

        return ret_code, stdout, stderr


def remote_file_exists(host, username, password, remote_file_path, port=22, pkey=None):
    """ Check to see if a remote file exists

    Args:
        host (str): The ip or FQDN of the host to check file existence on
        username (str): The username for the host
        password (str): The password for the username
        remote_file_path (str): The remote file to check exists
        port (int): The port to scp over
        pkey (str): The path to the ssh key to use

    Returns:
        (bool): Whether or not the file exists
    """

    cmd = f"[[ -e {remote_file_path} ]]"
    rc, out, err = execute_command(host, username, password, cmd, pkey=pkey)
    if rc != 0:
        _LOG.debug(f"Log {remote_file_path} doesn't exist, skipping...")
        return False
    return True


def get(host, username, password, remote_file, local_path, port=22, pkey=None):
    """ SCP a remote file to a local file

    Args:
        host (str): The ip or FQDN of the host to retrieve file from
        username (str): The username for the host
        password (str): The password for the username
        remote_file (str): The remote file to retrieve
        local_path (str): The local dir to store the remote file
        port (int): The port to scp over
        pkey (str): The path to the ssh key to use
    """

    with SSHConnect(host, username, password, port=port, pkey=pkey) as client:
        with SCPClient(client.get_transport()) as scp:
            _LOG.debug("Extablished scp session")
            return scp.get(remote_file, local_path=local_path)


def put(host, username, password, local_file, remote_path=b'.', port=22, pkey=None):
    """ SCP a local file to a remote file

    Args:
        host (str): The ip or FQDN of the host to retrieve file from
        username (str): The username for the host
        password (str): The password for the username
        local_file (str): The remote file's local filename
        remote_path (str): The remote path to put the file into (default: .)
        port (int): The port to scp over
        pkey (str): The path to the ssh key to use
    """

    with SSHConnect(host, username, password, port=port, pkey=pkey) as client:
        with SCPClient(client.get_transport()) as scp:
            _LOG.debug("Extablished scp session")
            return scp.put(local_file, remote_path)


def ssh_running(host, port=22):
    """ Check if SSH is running

    Args:
        host (str): The FQDN or IP of the host to connect to
        port (int): The port to connect on
    """

    try:
        socket.create_connection((host, port), timeout=5)
        return True
    # pylint: disable=W0703
    except Exception:
        return False
    # pylint: enable=W0703


def wait_for_ssh(host, port=22, timeout=300, interval=1):
    """ Wait for the ssh service to respond.

    Args:
        host (str): The FQDN or IP of the host to connect to
        port (int): The port to connect on
        timeout (int): The time to wait for SSH to become available in seconds (Default: 300)
        interval (int): The time to sleep between checks in seconds (Default: 1)
    """
    _LOG.info("Waiting for SSH to become available on %s at port: %s", host, port)
    start_time = time.time()
    while not ssh_running(host, port=port):
        if time.time() - start_time > timeout:
            raise errors.ssh.SSHTimeoutError(f"Timed out waiting for ssh to '{host}' on port '{port}'")
        time.sleep(interval)
    _LOG.info("SSH is available on %s at port: %s", host, port)
