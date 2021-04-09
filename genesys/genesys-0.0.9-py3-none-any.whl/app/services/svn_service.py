import subprocess
import os
from configparser import ConfigParser, NoOptionError
from genesys.app.utils import config_helpers
from genesys.app.config import SVN_PARENT_PATH, SVN_PARENT_URL, PROJECTS_FOLDER, FILE_MAP

def create_svn_repo(project_svn_repo_path):
    subprocess.run(['svnadmin', 'create', project_svn_repo_path], stdout=None)

def svn_check_out(project_repo_url, project_folder):
    subprocess.run(['svn', 'co', project_repo_url, project_folder], stdout=subprocess.DEVNULL)

def svn_commit_all(project_folder, svn_commit_message):
    subprocess.run(['svn', 'cleanup', project_folder], stdout=subprocess.DEVNULL)
    subprocess.run(['svn', 'add', project_folder, '--force'], stdout=subprocess.DEVNULL)
    subprocess.run(['svn', 'cleanup', project_folder], stdout=subprocess.DEVNULL)
    subprocess.run(['svn', 'commit', project_folder, '-m', svn_commit_message], stdout=subprocess.DEVNULL)

def svn_relocate(new_url, working_path):
    subprocess.run(['svn', 'relocate', new_url, working_path], stdout=subprocess.DEVNULL)

def svn_delete(url, log_message):
    print('delet-------------------')
    subprocess.run(['svn', 'delete', '-m', log_message, url], stdout=subprocess.DEVNULL)
    url_dir_name = os.path.dirname(url)
    proc = subprocess.run(['svn', 'list', url_dir_name], stdout=subprocess.PIPE)
    if is_svn_url(url_dir_name) and not bool(proc.stdout.decode()):
        svn_delete(url_dir_name, log_message='deleted')
    print('delete end-------------------')

def is_svn_url(url):
    proc = subprocess.run(['svn', 'list', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return not bool(proc.returncode)

def svn_rename(old_url, new_url, log_message):
    subprocess.run(['svn', 'rename', '-m', log_message, '--parents', old_url, new_url], stdout=subprocess.DEVNULL)
    url_dir_name = os.path.dirname(old_url)
    proc = subprocess.run(['svn', 'list', url_dir_name], stdout=subprocess.PIPE)
    if is_svn_url(url_dir_name) and not bool(proc.stdout.decode()):
        svn_delete(url_dir_name, log_message='deleted')

def svn_mkdir(url, log_message):
    subprocess.run(['svn', 'mkdir', '-m', log_message, url], stdout=subprocess.DEVNULL)

def svn_make_dirs(url, log_message):
    subprocess.run(['svn', 'mkdir', '-m', '--parents', log_message, url], stdout=subprocess.DEVNULL)

def svn_import(path, repo_url, log_message):
    subprocess.run(['svn', 'import', '-m', log_message, path, repo_url], stdout=subprocess.DEVNULL)

def default_acl(project_name):
    svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name, 'conf/authz')
    acl_parser = ConfigParser()
    acl_parser['groups'] = {
                'admin':'suser',
                'maps':'',
                'edit':'',
            }
    acl_parser['/'] = {
                '*':'r',
                '@admin':'rw',
            }
    config_helpers.write_config(svn_authz_path, acl_parser)

def svn_update_acl(base_svn_directory, acl_parser, file_map_parser, task_type, person, permission):
    try:
        task_type_map = file_map_parser.get('file_map', task_type).lower()
        if task_type_map == 'base':
            svn_directory = f'{base_svn_directory}.blend'
            if permission == 'rw':
                acl_parser.set(svn_directory, person, permission)
            elif permission == 'r':
                if acl_parser.get(svn_directory, person) == '':
                    acl_parser.set(svn_directory, person, permission)
            elif permission == 'none':
                acl_parser.set(svn_directory, person, '')

        elif task_type_map == 'none':
            pass
        else:
            svn_directory = f'{base_svn_directory}_{task_type_map}.blend'
            if permission == 'rw':
                acl_parser.set(svn_directory, person, permission)
            elif permission == 'r':
                if acl_parser.get(svn_directory, person) == '':
                    acl_parser.set(svn_directory, person, permission)
            elif permission == 'none':
                acl_parser.set(svn_directory, person, '')
    except NoOptionError:
        svn_directory = f'{base_svn_directory}_{task_type}.blend'
        if permission == 'rw':
            acl_parser.set(svn_directory, person, permission)
        elif permission == 'r':
            if acl_parser.get(svn_directory, person) == '':
                acl_parser.set(svn_directory, person, permission)
        elif permission == 'none':
            acl_parser.set(svn_directory, person, '')

def svn_read_file(url):
    proc = subprocess.run(['svn', 'cat', url], stdout=subprocess.PIPE)
    file = proc.stdout.decode("utf-8")
    return file

