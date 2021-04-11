from __future__ import print_function
import pickle
import argparse
import logging
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime


from . import gconfig
config = gconfig.config()


def auth(service):
    SCOPES = [
        'https://www.googleapis.com/auth/calendar.events',
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/calendar.readonly',
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive.readonly'
    ]
    creds = None
    ftoken = os.path.expanduser(config['google']['token'])
    fcreds = os.path.expanduser(config['google']['creds'])
    if os.path.exists(ftoken):
        with open(ftoken, 'rb') as token:
            creds = pickle.load(token, encoding='latin1')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                fcreds, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(ftoken, 'wb') as token:
            pickle.dump(creds, token, protocol=2)
    return build(service, 'v3', credentials=creds, cache_discovery=False)
