import pytest

from multiprocessing import Process
from flask import request, make_response
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from .endpoints import TestGeneralApiEndpoints, TestSpecificApiEndpoints
from sweetspot.client import Client

@pytest.fixture(scope='module')
def server(app):
    class TestMerchantApiEndpoints(MethodView):

        @jwt_required()
        def get(self):
            data = {'success':True}
            resp = make_response(data, 200)
            return resp 

        def post(self):
            data = request.get_json()
            assert data.get('serialized') == True 
            data = {'success':True}
            resp = make_response(data, 201)
            return resp

    app.add_url_rule('/api/merchant', view_func=TestMerchantApiEndpoints.as_view('general'))
    app.add_url_rule('/api/merchant/<uuid:id>', view_func=TestSpecificApiEndpoints.as_view('specific'))

    server = Process(target=app.run)
    
    yield server.start()

    server.terminate()
    server.join()

def test_get_all_merchants(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.merchant.get_all_merchants()
    assert result.is_success() == True 

def test_add_merchant(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.merchant.add_merchant(payload)
    assert result.is_success() == True 

def test_get_merchant(server, sample_uuid):
    client = Client(environment='test')
    result = client.merchant.get_merchant(sample_uuid)
    assert result.is_success() == True 

def test_update_merchant(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.merchant.update_merchant(sample_uuid, payload)
    assert result.is_success() == True 

def test_replace_merchant(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.merchant.replace_merchant(sample_uuid, payload)
    assert result.is_success() == True 

def test_delete_merchant(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.merchant.delete_merchant(sample_uuid)
    assert result.is_success() == True

