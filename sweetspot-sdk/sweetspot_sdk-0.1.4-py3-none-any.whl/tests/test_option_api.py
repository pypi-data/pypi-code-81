import pytest

from multiprocessing import Process
from flask import request
from .endpoints import TestGeneralApiEndpoints, TestSpecificApiEndpoints
from sweetspot.client import Client

@pytest.fixture(scope='module')
def server(app):
    app.add_url_rule('/api/option', view_func=TestGeneralApiEndpoints.as_view('general'))
    app.add_url_rule('/api/option/<uuid:id>', view_func=TestSpecificApiEndpoints.as_view('specific'))

    server = Process(target=app.run)
    
    yield server.start()

    server.terminate()
    server.join()

def test_get_all_options(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.option.get_all_options()
    assert result.is_success() == True 

def test_add_option(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.option.add_option(payload)
    assert result.is_success() == True 

def test_get_option(server, sample_uuid):
    client = Client(environment='test')
    result = client.option.get_option(sample_uuid)
    assert result.is_success() == True 

def test_update_option(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.option.update_option(sample_uuid, payload)
    assert result.is_success() == True 

def test_replace_option(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.option.replace_option(sample_uuid, payload)
    assert result.is_success() == True 

def test_delete_option(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.option.delete_option(sample_uuid)
    assert result.is_success() == True

