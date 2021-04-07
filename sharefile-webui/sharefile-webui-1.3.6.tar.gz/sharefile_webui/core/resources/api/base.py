import os
from flask_restful import Resource, reqparse, abort
from ...config import Config


class BaseResource(Resource):
    def __init__(self):
        self.config: Config = Config
        self.root_path: str = self.config.SHARE_DIRECTORY
        self.parser: reqparse.RequestParser = reqparse.RequestParser()
        self.args: dict = None

    def add_argument(self, name: str, type_: type = None, help_: str = None):
        self.parser.add_argument(name, type=type_, help=help_)
        self.args = self.parser.parse_args()

    def _check_path_perms(self, path: str) -> bool:
        rpath = os.path.realpath(path)
        return rpath.startswith(self.root_path)

    def abort_error(self, message: str):
        abort(400, message=message, status=False)
