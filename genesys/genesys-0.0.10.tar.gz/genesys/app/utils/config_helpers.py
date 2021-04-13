import os
from genesys.app.services import svn_service

def write_config(file_directory, config_parser):
    '''
        write data from a configuration parser
        to file
    '''
    with open(file_directory, 'w') as f:
        config_parser.write(f)

def load_config(file_directory, config_parser):
    '''
        load data from a configuration file 
        into a configuration parser instance
    '''
    with open(file_directory, 'r') as f:
        data = f.read()
    config_parser.read_string(data)

def write_file_map(file_map_url, file_map_parser):
    '''
        write file map from a configuration parser
        to file
    '''
    temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.temp')
    if not os.path.isdir(temp_dir):
        os.mkdir(temp_dir)
    file_name = os.path.basename(file_map_url)
    temp_file = os.path.join(temp_dir, file_name)
    with open(temp_file, 'w') as f:
        file_map_parser.write(f)
    if not svn_service.is_svn_url(file_map_url):
        svn_service.svn_import(path=temp_file, repo_url=file_map_url, log_message='add config')
    else:
        svn_service.svn_delete(url=file_map_url, log_message='deleted file_map_temporaly')
        svn_service.svn_import(path=temp_file, repo_url=file_map_url, log_message='add config')

def load_file_map(file_map_url, file_map_parser):
    '''
        load data from a configuration file 
        into a configuration parser instance
    '''
    file = svn_service.svn_read_file(file_map_url)
    file_map_parser.read_string(file)