from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from genesys.app.config import (SVN_PARENT_PATH,
                                SVN_PARENT_URL,
                                PROJECTS_FOLDER,
                                FILE_MAP,
                                LOGIN_NAME)
from genesys.app.blueprints.task.utils import create_task_file, create_new_task_acl, delete_task_file
from genesys.app.services import svn_service, project_service
from genesys.app.utils import config_helpers
import os
import shutil
from configparser import ConfigParser

task = Blueprint('task', __name__)
api = Api(task)

class Task(Resource):
    def post(self, project_name):
        data = request.get_json()
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        project = (data['project'])
        root = os.path.join(project['file_tree']['working']['mountpoint'], project['file_tree']['working']['root'],'')
        # replacing file tree mount point with genesys config mount point
        base_file_directory = data['base_file_directory'].split(root,1)[1]
        self.create_task_file(project_name=project_name,
                                base_file_directory=base_file_directory,
                                base_svn_directory=data['base_svn_directory'],
                                all_persons=data['all_persons'],
                                task_type=data['task_type'],
                                )
        return jsonify(message=f'project created')

    def delete(self, project_name):
        data = request.get_json()
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        project = (data['project'])
        root = os.path.join(project['file_tree']['working']['mountpoint'], project['file_tree']['working']['root'],'')
        # replacing file tree mount point with genesys config mount point
        base_file_directory = data['base_file_directory'].split(root,1)[1]
        self.delete_task_file(project_name, base_file_directory, task_type=data['task_type'])

    def create_task_file(self, project_name, base_file_directory, base_svn_directory, all_persons, task_type):
        file_map_parser = ConfigParser()
        acl_parser = ConfigParser()
        svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name, 'conf/authz')
        blend_file_url = os.path.join(SVN_PARENT_URL, base_file_directory)
        all_users = [person[LOGIN_NAME] for person in all_persons]
        project_folder = os.path.join(PROJECTS_FOLDER, project_name)
        file_map_url = os.path.join(SVN_PARENT_URL, project_name, '.conf/file_map')

        config_helpers.load_file_map(file_map_url, file_map_parser)
        config_helpers.load_config(svn_authz_path, acl_parser)

        create_task_file(blend_file_url=blend_file_url,
                        file_map_parser=file_map_parser,
                        task_type=task_type)
        
        create_new_task_acl(all_users=all_users,
                            base_svn_directory=base_svn_directory,
                            acl_parser=acl_parser,
                            file_map_parser=file_map_parser,
                            task_type=task_type)

        config_helpers.write_file_map(file_map_url, file_map_parser)
        config_helpers.write_config(svn_authz_path, acl_parser)
        
        # svn_commit_message = f'genesys added and commit {base_file_directory}'
        # svn_service.svn_commit_all(project_folder, svn_commit_message)

    def delete_task_file(self, project_name, base_file_directory, task_type):
        file_map_parser = ConfigParser()
        acl_parser = ConfigParser()
        svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name, 'conf/authz')
        # if asset_task['entity_type'] == 'asset':
        #     new_blend_file_url = os.path.join(os.path.dirname(blend_file_url), asset_task['new_file_name'])
        # elif asset_task['entity_type'] == 'shot':
        #     shot_folder = os.path.join(os.path.dirname(os.path.dirname(blend_file_url)), \
        #         asset_task['new_file_name'].rsplit('_', 1)[1])
        #     new_blend_file_url = os.path.join(shot_folder, asset_task['new_file_name'])
        #     print('shot', new_blend_file_url)
        #     print(shot_folder)
        blend_file_url = os.path.join(SVN_PARENT_URL, base_file_directory)
        print(blend_file_url)
        file_map_url = os.path.join(SVN_PARENT_URL, project_name, '.conf/file_map')

        config_helpers.load_file_map(file_map_url, file_map_parser)
        # config_helpers.load_config(svn_authz_path, acl_parser)
        delete_task_file(blend_file_url=blend_file_url, file_map_parser=file_map_parser, task_type=task_type)

        # config_helpers.write_file_map(file_map_url, file_map_parser)
        # config_helpers.write_config(svn_authz_path, acl_parser)

class Task_File_Access_Control(Resource):
    def put(self, project_name):
        data = request.get_json()
        self.update_svn_acl(data, project_name)
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        return jsonify(message=f'project created', project_name=project_name, svn_url=project_repo_url)

    def update_svn_acl(self, data, project_name):
        file_map_parser = ConfigParser()
        acl_parser = ConfigParser()

        svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name, 'conf/authz')
        project_folder = os.path.join(PROJECTS_FOLDER, project_name)
        file_map_dir = os.path.join(project_folder, '.conf/file_map')
        config_helpers.load_config(file_map_dir, file_map_parser)
        config_helpers.load_config(svn_authz_path, acl_parser)

        svn_service.svn_update_acl(
            base_svn_directory=data['base_svn_directory'],
            acl_parser=acl_parser,
            file_map_parser=file_map_parser,
            task_type=data['task_type'],
            person=data['person'][LOGIN_NAME],
            permission='rw'
        )

        config_helpers.write_config(file_map_dir, file_map_parser)
        config_helpers.write_config(svn_authz_path, acl_parser)


api.add_resource(Task, '/task/<string:project_name>')
api.add_resource(Task_File_Access_Control, '/task_acl/<string:project_name>')