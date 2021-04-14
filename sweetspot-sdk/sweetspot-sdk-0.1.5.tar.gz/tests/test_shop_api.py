import pytest

from multiprocessing import Process
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from .endpoints import TestSpecificApiEndpoints, TestGeneralApiEndpoints
from sweetspot.client import Client

@pytest.fixture(scope='module')
def server(app):
    
    app.add_url_rule('/api/shop', view_func=TestGeneralApiEndpoints.as_view('general'))
    app.add_url_rule('/api/shop/<uuid:id>', view_func=TestSpecificApiEndpoints.as_view('specific'))
    app.add_url_rule('/api/shop/<uuid:id>/category', view_func=TestSpecificApiEndpoints.as_view('category'))
    app.add_url_rule('/api/shop/<uuid:id>/item', view_func=TestSpecificApiEndpoints.as_view('item'))
    app.add_url_rule('/api/shop/<uuid:id>/modifier', view_func=TestSpecificApiEndpoints.as_view('modifier'))
    app.add_url_rule('/api/shop/<uuid:id>/option', view_func=TestSpecificApiEndpoints.as_view('option'))

    server = Process(target=app.run)

    yield server.start()

    server.terminate()
    server.join()

def test_get_all_shops(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.shop.get_all_shops()
    assert result.is_success() == True 

def test_add_shop(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.shop.add_shop(payload)
    assert result.is_success() == True 

def test_get_shop(server, sample_uuid):
    client = Client(environment='test')
    result = client.shop.get_shop(sample_uuid)
    assert result.is_success() == True 

def test_update_shop(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.shop.update_shop(sample_uuid, payload)
    assert result.is_success() == True 

def test_replace_shop(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.shop.replace_shop(sample_uuid, payload)
    assert result.is_success() == True 

def test_delete_shop(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.shop.delete_shop(sample_uuid)
    assert result.is_success() == True

def test_get_categories(server, sample_uuid):
    client = Client(environment='test')
    result = client.shop.get_categories(sample_uuid)
    assert result.is_success() == True 

def test_get_items(server, sample_uuid):
    client = Client(environment='test')
    result = client.shop.get_items(sample_uuid)
    assert result.is_success() == True 

def test_get_modifiers(server, sample_uuid):
    client = Client(environment='test')
    result = client.shop.get_modifiers(sample_uuid)
    assert result.is_success() == True 

def test_get_options(server, sample_uuid):
    client = Client(environment='test')
    result = client.shop.get_options(sample_uuid)
    assert result.is_success() == True




