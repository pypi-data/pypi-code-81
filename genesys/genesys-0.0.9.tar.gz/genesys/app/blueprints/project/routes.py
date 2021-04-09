from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from genesys.app.config import SVN_PARENT_PATH, SVN_PARENT_URL, PROJECTS_FOLDER, FILE_MAP
from genesys.app.blueprints.project.utils import create_project_folders, create_project_file_map
from genesys.app.services import svn_service, project_service, files_service
import os
import shutil
# from rq import Queue
# import redis

# r = redis.Redis()
# q = Queue(connection=r)

project = Blueprint('project', __name__)
api = Api(project)

class Project(Resource):
    """
    Create, rename, and delete project folder and repositories
    
    """
    def post(self, project_name):
        project_name = files_service.format_file_name(project_name)
        self.create_project(project_name)
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        return jsonify(message=f'project created', project_name=project_name, svn_url=project_repo_url)

    def put(self, project_name):
        data = request.get_json()
        old_project_name = files_service.format_file_name(data['old_project_name'])
        new_project_name = files_service.format_file_name(data['new_project_name'])
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        self.rename_project(old_project_name, new_project_name)
        return jsonify(message=f'project created', project_name=project_name, svn_url=project_repo_url)

    def delete(self, project_name):
        project_name = files_service.format_file_name(project_name)
        self.archive_project(project_name)
        return jsonify(message=f'project archived', project_name=project_name)

    def create_project(self, project_name):
        project_svn_folder = os.path.join(SVN_PARENT_PATH, project_name)
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        project_folder = os.path.join(PROJECTS_FOLDER, project_name)
        # svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name, 'conf/authz')

        svn_service.create_svn_repo(project_svn_folder)
        #TODO remove checkout
        create_project_folders(project_repo_url)
        create_project_file_map(project_repo_url, file_map=FILE_MAP)
        # svn_service.svn_check_out(project_repo_url, project_folder)
        # svn_service.svn_commit_all(project_folder, 'event commit')
        svn_service.default_acl(project_name)

    def rename_project(self, old_project_name, new_project_name):
        """
        rename project folder and repository and also relocates svn repo
        """
        new_project_folder = os.path.join(PROJECTS_FOLDER, new_project_name)
        old_project_folder = os.path.join(PROJECTS_FOLDER, old_project_name)
        new_project_svn_folder = os.path.join(SVN_PARENT_PATH, new_project_name)
        old_project_svn_folder = os.path.join(SVN_PARENT_PATH, old_project_name)
        new_project_repo_url = os.path.join(SVN_PARENT_URL, new_project_name)
        # old_project_repo_url = os.path.join(svn_parent_url, old_project_name)
        shutil.move(old_project_svn_folder, new_project_svn_folder)
        shutil.move(old_project_folder, new_project_folder)
        svn_service.svn_relocate(new_project_repo_url, new_project_folder)

    def archive_project(self, project_name):
        project_svn_folder = os.path.join(SVN_PARENT_PATH, project_name)
        project_folder = os.path.join(PROJECTS_FOLDER, project_name)
        svn_archive_folder = os.path.join(SVN_PARENT_PATH, 'archive')

        if not os.path.exists(svn_archive_folder):
            os.makedirs(svn_archive_folder)

        shutil.make_archive(base_name=os.path.join(svn_archive_folder, project_name), format='zip',
                            root_dir= project_svn_folder)
        shutil.rmtree(project_svn_folder)
        # shutil.rmtree(project_folder)

api.add_resource(Project, '/project/<string:project_name>')

