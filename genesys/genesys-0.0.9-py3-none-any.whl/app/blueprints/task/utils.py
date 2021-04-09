import os
from genesys.app.services import files_service, svn_service
from genesys.app.config import SVN_PARENT_PATH, SVN_PARENT_URL, PROJECTS_FOLDER, TEMPLATE_FILES_DIR
from configparser import NoOptionError
from genesys.app.utils import config_helpers

def create_task_file(blend_file_url, file_map_parser, task_type):
    file_folder_url = os.path.dirname(blend_file_url)
    try:
        task_type_map = file_map_parser.get('file_map', task_type).lower()
        if task_type_map == 'base':
            if not svn_service.is_svn_url(file_folder_url):
                svn_service.svn_make_dirs(file_folder_url, log_message=f'created {file_folder_url}')
            if not svn_service.is_svn_url(f'{blend_file_url}.blend'):
                svn_service.svn_import(path=os.path.join(TEMPLATE_FILES_DIR,'blender.blend'),
                                        repo_url=f'{blend_file_url}.blend',
                                        log_message=f'create {blend_file_url}.blend')
        elif task_type_map == 'none':
            pass
        else:
            if not svn_service.is_svn_url(file_folder_url):
                svn_service.svn_make_dirs(file_folder_url, log_message=f'created {file_folder_url}')
            if not svn_service.is_svn_url(f'{blend_file_url}_{task_type_map}.blend'):
                svn_service.svn_import(path=os.path.join(TEMPLATE_FILES_DIR,'blender.blend'),
                                        repo_url=f'{blend_file_url}_{task_type_map}.blend',
                                        log_message=f'create {blend_file_url}.blend')
    except NoOptionError:
        if not svn_service.is_svn_url(file_folder_url):
            svn_service.svn_make_dirs(file_folder_url, log_message=f'created {file_folder_url}')
        if not svn_service.is_svn_url(f'{blend_file_url}_{task_type}.blend'):
            svn_service.svn_import(path=os.path.join(TEMPLATE_FILES_DIR,'blender.blend'),
                                        repo_url=f'{blend_file_url}_{task_type}.blend',
                                        log_message=f'create {blend_file_url}.blend')
        file_map_parser.set('file_map', task_type, task_type)

def create_new_task_acl(all_users, base_svn_directory, acl_parser, file_map_parser, task_type):
    try:
        task_type_map = file_map_parser.get('file_map', task_type).lower()
        if task_type_map == 'base':
            svn_directory = f'{base_svn_directory}.blend'
            if svn_directory in acl_parser:
                pass
            else:
                for user in all_users:
                    if svn_directory in acl_parser:
                        acl_parser.set(svn_directory, user, '')
                    else:
                        acl_parser[svn_directory] = {
                            '@admin':'rw',
                            user:''
                        }
        elif task_type_map == 'none':
            pass
        else:
            svn_directory = f'{base_svn_directory}_{task_type_map}.blend'
            if svn_directory in acl_parser:
                pass
            else:
                for user in all_users:
                    if svn_directory in acl_parser:
                        acl_parser.set(svn_directory, user, '')
                    else:
                        acl_parser[svn_directory] = {
                            '@admin':'rw',
                            user:''
                        }
    except NoOptionError:
        svn_directory = f'{base_svn_directory}_{task_type}.blend'
        if svn_directory in acl_parser:
            pass
        else:
            for user in all_users:
                if svn_directory in acl_parser:
                    acl_parser.set(svn_directory, user, '')
                else:
                    acl_parser[svn_directory] = {
                        '@admin':'rw',
                        user:''
                    }

def delete_task_file(blend_file_url, file_map_parser, task_type):
    try:
        task_type_map = file_map_parser.get('file_map', task_type).lower()
        if task_type_map == 'base':
            if svn_service.is_svn_url(f'{blend_file_url}.blend'):
                svn_service.svn_delete(f'{blend_file_url}.blend', log_message=f'created {blend_file_url}.blend')
        elif task_type_map == 'none':
            pass
        else:
            if svn_service.is_svn_url(f'{blend_file_url}_{task_type_map}.blend'):
                svn_service.svn_delete(f'{blend_file_url}_{task_type_map}.blend', log_message=f'created {blend_file_url}_{task_type_map}.blend')
    except NoOptionError:
        if svn_service.is_svn_url(f'{blend_file_url}_{task_type}.blend'):
            svn_service.svn_delete(f'{blend_file_url}_{task_type}.blend', log_message=f'created {blend_file_url}_{task_type}.blend')
        # file_map_parser.set('file_map', task_type, task_type)