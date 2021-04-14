import pytest

from flask import Flask, jsonify, make_response, request, Blueprint
from flask.views import MethodView
from flask_jwt_extended import JWTManager, set_refresh_cookies, set_access_cookies, create_access_token, create_refresh_token, get_csrf_token

from sweetspot.client import Client

@pytest.fixture(scope='module')
def app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'secretkey'
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    JWTManager(app)

    yield app

@pytest.fixture 
def sample_uuid():
    return '59cb4747-0761-4612-9783-43c91ce14594'

@pytest.fixture(scope='function')
def sample_cookie_resp():
    access_token = create_access_token('test')
    refresh_token =  create_refresh_token('refresh')
    sample_cookie_resp = {
        'access_token_cookie': access_token,
        'refresh_token_cookie': refresh_token, 
        'csrf_access_token': get_csrf_token(access_token),
        'csrf_refresh_token': get_csrf_token(refresh_token)
    }
    return sample_cookie_resp





    

