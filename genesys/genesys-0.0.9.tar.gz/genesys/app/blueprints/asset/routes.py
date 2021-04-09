from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from genesys.app.config import SVN_PARENT_PATH, SVN_PARENT_URL, PROJECTS_FOLDER, FILE_MAP
from genesys.app.blueprints.project.utils import create_project_folders, create_project_file_map
from genesys.app.services import svn_service, project_service, files_service
import os
import shutil
from genesys.app.utils import config_helpers
from genesys.app.blueprints.asset.utils import rename_asset_task_file, rename_task_acl_section
from configparser import ConfigParser
# from rq import Queue
# import redis

# r = redis.Redis()
# q = Queue(connection=r)

asset = Blueprint('asset', __name__)
api = Api(asset)

class Asset(Resource):
    def put(self, project_name):
        data = request.get_json()
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        self.rename_asset(data, project_name)
        return jsonify(message=f'project created', project_name=project_name, svn_url=project_repo_url)

    def rename_asset(self, data, project_name):
        for asset_task in data:
            file_map_parser = ConfigParser()
            acl_parser = ConfigParser()
            task_type = asset_task['task_type']
            project = asset_task['project']
            root = os.path.join(project['file_tree']['working']['mountpoint'], project['file_tree']['working']['root'], '')
            # replacing file tree mount point with genesys config mount point
            print(asset_task['working_file_path'])
            #TODO rename shot folder
            base_file_directory = asset_task['working_file_path'].split(root,1)[1]
            base_svn_directory = asset_task['base_svn_directory']

            projects_folder_mount_point = os.path.dirname(PROJECTS_FOLDER)

            blend_file_url = os.path.join(SVN_PARENT_URL, base_file_directory)
            if asset_task['entity_type'] == 'asset':
                new_blend_file_url = os.path.join(os.path.dirname(blend_file_url), asset_task['new_file_name'])
            elif asset_task['entity_type'] == 'shot':
                shot_folder = os.path.join(os.path.dirname(os.path.dirname(blend_file_url)), \
                    asset_task['new_file_name'].rsplit('_', 1)[1])
                new_blend_file_url = os.path.join(shot_folder, asset_task['new_file_name'])
                print('shot', new_blend_file_url)
                print(shot_folder)
            new_base_svn_directory = os.path.join(os.path.dirname(base_svn_directory), asset_task['new_file_name'])
            project_folder = os.path.join(PROJECTS_FOLDER, project_name)
            svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name, 'conf/authz')
            file_map_url = os.path.join(SVN_PARENT_URL, project_name, '.conf/file_map')

            config_helpers.load_file_map(file_map_url, file_map_parser)
            config_helpers.load_config(svn_authz_path, acl_parser)
            print(blend_file_url)
            print(new_blend_file_url)
            rename_asset_task_file(
                old_blend_file_url=blend_file_url,
                new_blend_file_url=new_blend_file_url, 
                file_map_parser=file_map_parser, 
                task_type=task_type)
            rename_task_acl_section(
                old_base_svn_directory= base_svn_directory,
                base_svn_directory= new_base_svn_directory,
                file_map_parser= file_map_parser,
                acl_parser= acl_parser,
                task_type= task_type
                )
            config_helpers.write_file_map(file_map_url=file_map_url, file_map_parser=file_map_parser)
            config_helpers.write_config(svn_authz_path, acl_parser)

        # svn_commit_message = 'renamed asset'
        # svn_service.svn_commit_all(project_folder, svn_commit_message)


api.add_resource(Asset, '/asset/<string:project_name>')

