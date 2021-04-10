import pytest
import requests
import json

from multiprocessing import Process
from flask import request, make_response
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from .endpoints import TestGeneralApiEndpoints, TestSpecificApiEndpoints
from sweetspot.client import Client

@pytest.fixture(scope='module')
def server(app):

    class TestUnprotectedPostEndpoint(MethodView):

        def post(self):
            resp = make_response('', 201)
            return resp

    class TestUnprotectedPostEndpointWithID(MethodView):

        def post(self, id):
            resp = make_response('', 201)
            return resp

    class TestProtectedPostEndpoint(MethodView):

        @jwt_required()
        def post(self):
            resp = make_response('', 201)
            return resp

    class TestProtectedRefreshPostEndpoint(MethodView):

        @jwt_required(refresh=True)
        def post(self):
            resp = make_response('', 201)
            return resp

    app.add_url_rule('/api/authentication/change-password', view_func=TestProtectedPostEndpoint.as_view('change_password'))
    app.add_url_rule('/api/authentication/refresh-token', view_func=TestProtectedRefreshPostEndpoint.as_view('refresh'))
    app.add_url_rule('/api/authentication/verify-email-token', view_func=TestProtectedPostEndpoint.as_view('verify_email_token'))
    app.add_url_rule('/api/authentication/verify-email/<uuid:id>', view_func=TestUnprotectedPostEndpointWithID.as_view('verify_merchant_email'))
    app.add_url_rule('/api/authentication/login', view_func=TestUnprotectedPostEndpoint.as_view('login'))
    app.add_url_rule('/api/authentication/logout', view_func=TestUnprotectedPostEndpoint.as_view('logout'))


    server = Process(target=app.run)
    
    yield server.start()

    server.terminate()
    server.join()

def test_change_password(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.authentication.change_password(payload)
    assert result.is_success() == True 

def test_refresh_token(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.authentication.refresh_access()
    assert result.is_success() == True 

def test_verify_email_token(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.authentication.verify_email_token(payload)
    assert result.is_success() == True 

def test_send_verification_email(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.authentication.send_verification_email(sample_uuid)
    assert result.is_success() == True 

def test_login(server):
    client = Client(environment='test')
    payload = {'serialized':True}
    result = client.authentication.get_authentication_information(payload)
    assert result.is_success() == True 

def test_logout(server):
    client = Client(environment='test')
    result = client.authentication.unset_access()
    assert result.is_success() == True
