import pytest 

from multiprocessing import Process
from flask import request, make_response
from flask.views import MethodView
from .endpoints import TestGeneralApiEndpoints, TestSpecificApiEndpoints
from sweetspot.client import Client

@pytest.fixture(scope='module')
def server(app):

    class TestUnprotectedPostEndpoint(TestGeneralApiEndpoints):

        def post(self):
            data = request.get_json()
            assert data.get('serialized') == True 
            data = {'success':True}
            resp = make_response(data, 201)
            return resp 

    app.add_url_rule('/api/beta-user', view_func=TestUnprotectedPostEndpoint.as_view('general'))
    app.add_url_rule('/api/beta-user/<uuid:id>', view_func=TestSpecificApiEndpoints.as_view('specific'))

    server = Process(target=app.run)
    
    yield server.start()

    server.terminate()
    server.join()

def test_add_beta_user(server):
    client = Client(environment='test')
    payload = {'serialized':True}
    result = client.beta_user.add_beta_user(payload)
    assert result.is_success() == True 

def test_get_beta_user(server, sample_uuid):
    client = Client(environment='test')
    result = client.beta_user.get_beta_user(sample_uuid)
    assert result.is_success() == True 

def test_get_all_beta_users(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.beta_user.get_all_beta_users()
    assert result.is_success() == True