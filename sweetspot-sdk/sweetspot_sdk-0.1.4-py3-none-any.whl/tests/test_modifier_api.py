import pytest

from multiprocessing import Process
from flask import request
from .endpoints import TestGeneralApiEndpoints, TestSpecificApiEndpoints
from sweetspot.client import Client

@pytest.fixture(scope='module')
def server(app):
    app.add_url_rule('/api/modifier', view_func=TestGeneralApiEndpoints.as_view('general'))
    app.add_url_rule('/api/modifier/<uuid:id>', view_func=TestSpecificApiEndpoints.as_view('specific'))

    server = Process(target=app.run)
    
    yield server.start()

    server.terminate()
    server.join()

def test_get_all_modifiers(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.modifier.get_all_modifiers()
    assert result.is_success() == True 

def test_add_modifier(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.modifier.add_modifier(payload)
    assert result.is_success() == True 

def test_get_modifier(server, sample_uuid):
    client = Client(environment='test')
    result = client.modifier.get_modifier(sample_uuid)
    assert result.is_success() == True 

def test_update_modifier(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.modifier.update_modifier(sample_uuid, payload)
    assert result.is_success() == True 

def test_replace_modifier(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.modifier.replace_modifier(sample_uuid, payload)
    assert result.is_success() == True 

def test_delete_modifier(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.modifier.delete_modifier(sample_uuid)
    assert result.is_success() == True

