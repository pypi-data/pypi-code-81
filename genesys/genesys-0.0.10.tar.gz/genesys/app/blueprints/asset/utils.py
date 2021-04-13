import os
from configparser import ConfigParser, NoOptionError, NoSectionError
import shutil
from genesys.app.utils import config_helpers
from genesys.app.services import svn_service

def rename_asset_task_file(old_blend_file_url, new_blend_file_url, file_map_parser, task_type):
    try:
        print('renaming')
        task_type_map = file_map_parser.get('file_map', task_type).lower()
        if task_type_map == 'base':
            source = f'{old_blend_file_url}.blend'
            destination = f'{new_blend_file_url}.blend'
            if svn_service.is_svn_url(source):
                svn_service.svn_rename(source, destination, log_message='renamed')
        elif task_type_map == 'none':
            pass
        else:
            source = f'{old_blend_file_url}_{task_type_map}.blend'
            destination = f'{new_blend_file_url}_{task_type_map}.blend'
            if svn_service.is_svn_url(source):
                svn_service.svn_rename(source, destination, log_message='renamed')
    except NoOptionError:
        source = f'{old_blend_file_url}_{task_type}.blend'
        destination = f'{new_blend_file_url}_{task_type}.blend'
        if svn_service.is_svn_url(source):
            svn_service.svn_rename(source, destination, log_message='renamed')

def rename_section(parser, section_from, section_to):
    items = parser.items(section_from)
    parser.add_section(section_to)
    for item in items:
        parser.set(section_to, item[0], item[1])
    parser.remove_section(section_from)

def rename_task_acl_section(old_base_svn_directory, base_svn_directory, file_map_parser, acl_parser, task_type):
    try:
        task_type_map = file_map_parser.get('file_map', task_type).lower()
        if task_type_map == 'base':
            source = f'{old_base_svn_directory}.blend'
            destination = f'{base_svn_directory}.blend'
            rename_section(acl_parser, source, destination)
        elif task_type_map == 'none':
            pass
        else:
            source = f'{old_base_svn_directory}_{task_type_map}.blend'
            destination = f'{base_svn_directory}_{task_type_map}.blend'
            rename_section(acl_parser, source, destination)
    except NoOptionError:
        source = f'{old_base_svn_directory}_{task_type}.blend'
        destination = f'{base_svn_directory}_{task_type}.blend'
        rename_section(acl_parser, source, destination)
    except NoSectionError:
        # FIXME check if renamed version of file exist in acl
        # TODO skip task with same files
        pass