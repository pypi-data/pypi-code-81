# Copyright © 2021 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import Flask
from flask_restful import Resource, Api, reqparse
from deployz.utils import get_autotrainz

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {"Hello": "World"}


api.add_resource(HelloWorld, '/')


class Serve(Resource):
    def post(self, project_id, to_serve_packet):
        # executor = get_servz()
        # executor.run()
        return {"item_id": project_id, "packet": to_serve_packet}


api.add_resource(Serve, '/serve/')


training_parser = reqparse.RequestParser()
training_parser.add_argument('project_name', type=str)
training_parser.add_argument('version', type=str)

class Train(Resource):

    def post(self):
        args = training_parser.parse_args()
        executor = get_autotrainz()
        executor.run(artifact=args['project_name'],
                     version=args['version'])
        return {"packet": args}


api.add_resource(Train, '/train/')
