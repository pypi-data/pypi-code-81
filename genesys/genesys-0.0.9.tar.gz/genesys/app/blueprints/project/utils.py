import os
from configparser import ConfigParser
import shutil
from genesys.app.utils import config_helpers
from genesys.app.services import svn_service

def create_project_folders(project_repo):
    base_directories = ['.conf','edit', 'lib', 'refs', 'scenes', 'tools']
    lib_directories = ['chars', 'envs', 'maps', 'nodes', 'props']
    for directory in base_directories:
        url = os.path.join(project_repo, directory)
        svn_service.svn_mkdir(url=url, log_message=f'create {url}')
    for directory in lib_directories:
        url = os.path.join(project_repo, 'lib', directory)
        svn_service.svn_mkdir(url=url, log_message=f'create {url}')

def create_project_file_map(project_repo, file_map):
    file_map_parser = ConfigParser()
    file_map_url = os.path.join(project_repo, '.conf/file_map')
    file_map_parser['file_map'] = file_map
    config_helpers.write_file_map(file_map_url=file_map_url, file_map_parser=file_map_parser)