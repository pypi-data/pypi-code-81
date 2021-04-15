# coding=utf-8
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import marshal_with
from rest_server.resource.models.helper import resource_fields
from tool.git.git import Git
from test_framework.state import State


PARSER = reqparse.RequestParser()
PARSER.add_argument('user')
PARSER.add_argument('key')

class GitResource(Resource):

    def __init__(self):
        pass

    @marshal_with(resource_fields, envelope='resource')
    def post(self):
        args = PARSER.parse_args()
        user = args["user"]
        key = args["key"]
        git = Git(user, key)
        msg, ret = git.update_latest_code()
        state = State.PASS if ret==0 else State.FAIL
        result = {"msg": msg, "state": state}
        return result
