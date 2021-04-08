import pytest 

from multiprocessing import Process
from flask import request
from .endpoints import TestGeneralApiEndpoints, TestSpecificApiEndpoints
from sweetspot.client import Client

@pytest.fixture(scope='module')
def server(app):
    app.add_url_rule('/api/category', view_func=TestGeneralApiEndpoints.as_view('general'))
    app.add_url_rule('/api/category/<uuid:id>', view_func=TestSpecificApiEndpoints.as_view('specific'))

    server = Process(target=app.run)
    
    yield server.start()

    server.terminate()
    server.join()
    
def test_get_all_categories(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.category.get_all_categories()
    assert result.is_success() == True

def test_add_category(server, sample_cookie_resp):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.category.add_category(payload)
    assert result.is_success() == True

def test_get_category(server, sample_uuid): 
    client = Client(environment='test')
    result = client.category.get_category(sample_uuid)
    assert result.is_success() == True

def test_update_category(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.category.update_category(sample_uuid, payload)
    assert result.is_success() == True 

def test_replace_category(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    payload = {'serialized':True}
    result = client.category.replace_category(sample_uuid, payload)
    assert result.is_success() == True 

def test_delete_category(server, sample_cookie_resp, sample_uuid):
    client = Client(environment='test')
    client.update_config(**sample_cookie_resp)
    result = client.category.delete_category(sample_uuid)
    assert result.is_success() == True
    

            
            

            



