import click
import urllib3
import threading
import os
from typing import Optional
from covid_cloud.constants import *
from requests import Response
from requests.exceptions import HTTPError
from covid_cloud.client.utils import get_drs_client
from covid_cloud.client.auth import login
import gzip
import re
import io
import pandas as pd

#since our downloads are multi-threaded, we use a lock to avoid race conditions
output_lock = threading.Lock()

def get_host(url):
    return re.search(r'(?<=https://)([^/])+(?=/.*)',url).group(0)

def handle_file_response(download_file,data):
    #decode if fasta
    if re.search(r'\.fa',download_file):
        data = data.decode('utf-8')
        
    return data


def file_to_dataframe(download_file,data):
    #turn into dataframe for FASTA/FASTQ files, otherwise just return raw data
    if re.search(r'\.fa',download_file):
        data = data.split('\n',maxsplit=1)

        meta = data[0]
        sequence = data[1].replace('\n','') #remove newlines
        
        return pd.DataFrame({
            "meta": [meta],
            "sequence": [sequence]
            })
    
    return data


def is_drs_url(url):
    return url[:3] == 'drs'


def get_object_info_url_from_drs(url):
    drs_host = re.search(r'(?<=drs://)([^/])+(?=/.*)',url).group(0)
    object_url = f'https://{drs_host}/ga4gh/drs/v1/'
    return object_url, drs_host


def download_file(url, output_dir, oauth_token: Optional[dict] = None, 
                email: Optional[str] = None, 
                personal_access_token: Optional[str] = None, 
                auth_params: Optional[dict] = None, 
                out: Optional[list] = None):
    drs_server, drs_host = get_object_info_url_from_drs(url)
    
    
    
    drs_client = get_drs_client(drs_server)

    http = urllib3.PoolManager()
    chunk_size = 1024
    download_url = url
    download_file = ""
    signed_access_ids = ['az-blobstore-signed']
    
    object_id = url.split('/')[-1]
    if is_drs_url(url):
        # parse the drs url to the resource url
        try:
            object_info = drs_client.get_object_info(object_id)
        except HTTPError as e:
            if e.response.status_code == 401:
                #if their PAT and email is set, try to log into the appropriate DRS server an retry getting the object
                if email and personal_access_token:
                    try:
                        if drs_host not in oauth_token.keys():
                            oauth_token[drs_host] = login(email,personal_access_token,auth_params=auth_params,drs_url=drs_server)
                        #create a new client with token and get object info with the new client
                        drs_client = get_drs_client(drs_server,oauth_token[drs_host])
                        object_info = drs_client.get_object_info(object_id)
                    except:
                        click.secho("Access Denied", fg='red')
                else:
                    click.secho(f"Authorization required for {drs_server}. Please login or configure your email and personal access token", fg='red')
                    return
            elif e.response.status_code == 404:
                click.secho(f"DRS object with id {object_id} does not exist", fg='red')
                return
            elif e.response.status_code == 403:
                click.secho("Access Denied", fg='red')
                return
            else:
                click.secho("There was an error getting object info from the DRS Client", fg='red')
                return
        except Exception as e:
            return
            

        if "access_methods" in object_info.keys():
            for access_method in object_info["access_methods"][0]:
                if access_method.get('access_id', None):
                    if access_method['access_id'] in signed_access_ids:
                        click.echo("found signed access_id @ access_method level")
                        try:
                            object_access = drs_client.get_object_access(object_id, access_method['access_id'])
                        except HTTPError as e:
                            click.echo(e)
                            return
                        download_url = object_access['url']
                        break

                # if we have an https, use that
                if access_method['type'] == 'https':
                    download_url = access_method['access_url']['url']
                    download_file = download_url.split('/')[-1]
                    break
        else:
            return  # next page token, just return
    
    try:
        download_stream = http.request('GET', download_url, preload_content=False)
    except:
        click.secho("There was an error downloading " + download_url, fg='red')
        return

    data = handle_file_response(download_file,download_stream.read())
    
    if out is not None: 
        output_lock.acquire()
        out = out.append(file_to_dataframe(download_file,data))
        output_lock.release()

    else:
        with open(f"{output_dir}/{download_file}", 'wb+') as dest:
            while True:
                data = download_stream.read(chunk_size)
                if not data:
                    break
                dest.write(data)


def download_files(urls, output_dir=downloads_directory, oauth_token: Optional[str] = None, email: Optional[str] = None, personal_access_token: Optional[str] = None, auth_params: Optional[dict] = None, out=None):
    download_threads = []
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for url in urls:
        download = threading.Thread(target=download_file(url, output_dir, 
                                    oauth_token=oauth_token, 
                                    email=email,
                                    personal_access_token=personal_access_token,
                                    auth_params=auth_params,
                                    out=out), name=url)
        download.daemon = True
        download_threads.append(download)
        download.start()

    for thread in download_threads:
        thread.join()

    if out is None:
        click.secho("Download Complete into " + output_dir, fg='green')