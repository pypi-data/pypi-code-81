from flask.views import MethodView 
from flask import jsonify, make_response, request 
from flask_jwt_extended import jwt_required

class TestGeneralApiEndpoints(MethodView):

    @jwt_required()
    def get(self):
        data = {'success':True}
        resp = make_response(data, 200)
        return resp 

    @jwt_required()
    def post(self):
        data = request.get_json() 
        assert data.get('serialized') == True 
        data = {'success':True}
        resp = make_response(data, 201)
        return resp 

class TestSpecificApiEndpoints(MethodView):

    def get(self, id):
        data = {'success': True}
        resp = make_response(data, 200)
        return resp 

    @jwt_required()
    def patch(self, id):
        data = request.get_json()
        assert data.get('serialized') == True
        data = {'success': True}
        resp = make_response(data, 201)
        return resp 

    @jwt_required()
    def put(self, id):
        data = request.get_json()
        assert data.get('serialized') == True
        data = {'success': True}
        resp = make_response(data, 201)
        return resp  

    @jwt_required()
    def delete(self, id):
        resp = make_response('', 204)
        return resp 