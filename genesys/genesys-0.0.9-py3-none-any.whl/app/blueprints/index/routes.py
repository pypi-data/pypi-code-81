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
from configparser import ConfigParser
from genesys import __version__

index = Blueprint('index', __name__)
api = Api(index)

class Index(Resource):
    def get(self):
        return {"api": "eaxum_zou", "version": __version__}


api.add_resource(Index, '/')