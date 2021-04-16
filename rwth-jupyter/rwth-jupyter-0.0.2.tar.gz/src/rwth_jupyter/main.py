#!/bin/env python3

import os
import signal
import sys
import requests
import pathlib
import subprocess
import tempfile
import rpmfile
import gzip
import shutil
import atexit
import pkgutil
import logging
import threading
import time
import getpass
import site

JUPYTERHUB_URL = 'https://jupyter.rwth-aachen.de'

CHISEL_URL = 'https://github.com/jpillora/chisel/releases/download/v1.7.6/chisel_1.7.6_linux_amd64.gz'
SSHFS_URL = 'https://download-ib01.fedoraproject.org/pub/epel/7/x86_64/Packages/f/fuse-sshfs-2.10-1.el7.x86_64.rpm'

HOME_PATH = str(pathlib.Path.home())


LOCAL_BIN_PATH = f'{site.USER_BASE}/bin'
CHISEL_PATH = f'{site.USER_BASE}/bin/chisel'
JUPYTER_PATH = f'{site.USER_BASE}/bin/jupyterhub-singleuser'
SSHFS_PATH = f'{site.USER_BASE}/bin/sshfs'
TOKEN_PATH = f'{HOME_PATH}/.jupyter/token'
USER_MOUNT_PATH = f'{HOME_PATH}/jupyter-home'
TMP_MOUNT_PATH = f'/tmp/' + getpass.getuser() + '/jupyter'

jupyter = None
chisel = None


class Process(threading.Thread):

    def __init__(self, name, command, env={}):
        super().__init__()

        self.name = name
        self.command = command
        self.env = env

        self.start()

    def stop(self):
        self.process.kill()
        self.process.wait()

        self.join()

    def process_line(self, line):
        pass

    def run(self):
        logging.info('Starting %s process in background: %s', self.name, ' '.join(self.command))

        self.process = subprocess.Popen(self.command,
                             env=self.env,
                             shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        for line in iter(self.process.stdout.readline, ''):
            sys.stdout.buffer.write(line)
            sys.stdout.flush()

            self.process_line(line)

            rc = self.process.poll()
            if rc is not None:
                break

        logging.info('Process %s has stopped: rc=%d', self.name, rc)


class Chisel(Process):

    def __init__(self, host, remotes, auth=None, fingerprint=None):
        command = [CHISEL_PATH, 'client']

        if auth:
            username = auth.get('username')
            password = auth.get('password')

            command += ['--auth', f'{username}:{password}']

        if fingerprint:
            command += ['--fingerprint', fingerprint]

        command += [host]+remotes

        super().__init__('chisel', command)

        self.connected = threading.Event()

    def process_line(self, line):
        if line.find(b'Connected'):
            self.connected.set()


class Jupyter(Process):

    def __init__(self, username, token):
        env={
            'JUPYTERHUB_API_TOKEN': token,
            'JUPYTERHUB_CLIENT_ID': f'jupyterhub-user-{username}',
            'JUPYTERHUB_API_URL': 'http://localhost:8081/hub/api',
            'JUPYTERHUB_ACTIVITY_URL': f'http://localhost:8081/hub/api/users/{username}/activity',
            'JUPYTERHUB_OAUTH_CALLBACK_URL': f'/user/{username}/oauth_callback',
            'JUPYTERHUB_USER': username
        }

        super().__init__('jupyter', [JUPYTER_PATH, '--base-url', f'/user/{username}', '--port', '8890', HOME_PATH], env=env)


def run(command):
    logging.info('Running command: %s', ' '.join(command))

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(process.stdout.readline, ''):
        sys.stdout.buffer.write(line)
        sys.stdout.flush()

        rc = process.poll()
        if rc is not None:
            break

    return rc


def install_sshfs():
    # Abort if executable already exists
    if shutil.which('sshfs'):
        logging.info('Tool sshfs already exists. Skipping installation')
        return

    logging.info('Install sshfs...')

    # Download an extract executable from RPM
    r = requests.get(SSHFS_URL)
    with tempfile.TemporaryFile() as tf:
        tf.write(r.content)
        tf.seek(0)
    
        with rpmfile.open(fileobj=tf) as f:
            with f.extractfile('./usr/bin/sshfs') as sf:
                with open(SSHFS_PATH, 'wb') as df:
                    df.write(sf.read())

    os.chmod(SSHFS_PATH, 0o744)


def install_chisel():
    # Abort if executable already exists
    if shutil.which('chisel'):
        logging.info('Tool chisel already exists. Skipping installation')
        return

    logging.info('Installing Chisel...')

    # Download an unzip Chisel
    r = requests.get(CHISEL_URL)
    with tempfile.TemporaryFile() as tf:
        tf.write(r.content)
        tf.seek(0)

        with gzip.open(tf) as sf:
            with open(CHISEL_PATH, '+wb') as df:
                df.write(sf.read())

    os.chmod(CHISEL_PATH, 0o744)


def jupyter_get_token():
    try:
        with open(TOKEN_PATH, 'r') as tf:
            logging.info('Found existing API token for JupyterHub')
            return tf.read()

    except OSError:
        # Fetch reflector token

        # Direct user to token reflector
        logging.info('')
        logging.info('Please visit the following link to generate an API token for RWTHjupyter:')
        logging.info('')
        logging.info('     %s/hub/token', JUPYTERHUB_URL)
        logging.info('')

        token = input('Token: ')

        with open(TOKEN_PATH, 'w+') as tf:
            tf.write(token)
            logging.info('Stored API token at %s', TOKEN_PATH)

        return token


def jupyter_spawn(token, username):
    logging.info('Spawning JupyterHub session')

    r = requests.post(JUPYTERHUB_URL+f'/hub/api/users/{username}/server',
        headers={
            'Authorization': f'token {token}'
        },
        json={
            'profile', 'hpc'
        })

    r.raise_for_status()

    return r.json().get('name')


def sshfs_mount():
    logging.info('Mounting RWTHjupyter home...')

    # Create mountpoint
    pathlib.Path(TMP_MOUNT_PATH).mkdir(parents=True, exist_ok=True)

    if not os.path.islink(USER_MOUNT_PATH):
        os.symlink(TMP_MOUNT_PATH, USER_MOUNT_PATH)

    if os.path.ismount(TMP_MOUNT_PATH):
        logging.warn('Already mounted')
        return

    options = {
        'StrictHostKeyChecking': 'no',
        # 'Port': '2222',
        'directport': '7777'
    }

    command = [SSHFS_PATH]

    for k, v in options.items():
        command += ['-o', f'{k}={v}']

    command += ['127.0.0.1:/home/jovyan', TMP_MOUNT_PATH]

    rc = run(command)
    if rc != 0:
        raise Exception('Failed to mount remote dir: rc=' + rc)


def sshfs_unmount():
    logging.info('Un-mounting RWTHjupyter home...')

    if os.path.ismount(TMP_MOUNT_PATH):
        run(['fusermount', '-u', TMP_MOUNT_PATH])


def stop():

    if jupyter:
        jupyter.stop()

    if chisel:
        chisel.stop()

    sshfs_unmount()

    logging.info('Goodbye')


def main():
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    logging.info('Starting JupyterLab')

    # Register signals for catching Ctrl-C
    atexit.register(stop)

    # Create dirs
    pathlib.Path(os.path.dirname(TOKEN_PATH)).mkdir(parents=True, exist_ok=True)
    pathlib.Path(LOCAL_BIN_PATH).mkdir(parents=True, exist_ok=True)
    os.environ['PATH'] += os.pathsep + LOCAL_BIN_PATH
    os.environ['PYTHONPATH'] += os.pathsep + site.USER_BASE + '/lib/python3.6/site-packages'

    # Install tools
    install_sshfs()
    install_chisel()

    jupyter_token = jupyter_get_token()

    # Check token and get username from hub API
    r = requests.get(JUPYTERHUB_URL+'/hub/api/user',
        headers={
            'Authorization': f'token {jupyter_token}'
        })
    r.raise_for_status()
    j = r.json()

    jupyter_username = j.get('name')

    logging.info('Found my RWTHjupyter username: %s', jupyter_username)

    # Check if proper server is running in JupyterHub
    # TODO

    # Start JupyterHub server for user
    # TODO

    # Get tunnel connection details
    r = requests.post(JUPYTERHUB_URL+f'/user/{jupyter_username}/api/v1',
        headers={
            'Authorization': f'token {jupyter_token}'
        },
        data={
            'stop': 'true'
        })
    r.raise_for_status()

    j = r.json()

    chisel_username = j.get('chisel').get('username')
    chisel_password = j.get('chisel').get('password')
    chisel_fingerprint = j.get('chisel').get('fingerprint')
    jupyter_token = j.get('jupyter').get('token')

    # Establish chisel tunnel
    chisel = Chisel(JUPYTERHUB_URL+f'/user/{jupyter_username}/', ['7777', 'hub.jhub:8081', 'R:8890'],
        auth={
            'username': chisel_username,
            'password': chisel_password
        },
        fingerprint=chisel_fingerprint)

    if not chisel.connected.wait(timeout=5):
        raise Exception('Failed to connect to chisel server')

    # Start jupyterhub-singleuser
    jupyter = Jupyter(jupyter_username, jupyter_token)

    # Mount RWTHjupyter home directory
    sshfs_mount()

    time.sleep(3) # Delay the notes a bit so that they arnt hidden by Jupyter logs
    logging.info('')
    logging.info('You can now access your RWTHjupyter session here:')
    logging.info('')
    logging.info('       %s/user/%s/', JUPYTERHUB_URL, jupyter_username)
    logging.info('')


if __name__ == '__main__':
    main()
