# -*- coding: utf-8 -*-
import os
import pytest
from pyramid.testing import DummyRequest, testConfig
from pyramid.httpexceptions import HTTPOk, HTTPFound, HTTPInternalServerError
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.idp_metadata_parser import OneLogin_Saml2_IdPMetadataParser
from pyramid_saml import SAML, SAML_ERROR, SAML_NAME_ID, SAML_SESSION_INDEX, \
    SAML_USER_DATA, _load_settings, _load_settings_from_file, \
    _load_settings_from_url


def __get_request():
    request = DummyRequest()
    request.scheme = 'https'
    request.server_port = 80
    return request


@pytest.mark.parametrize('settings,lowercase,scheme,https', [
    (
        {
            'index_route_name': 'index',
            'saml_path': os.path.dirname(__file__)
        },
        False,
        'https',
        'on'
    ),
    (
        {
            'index_route_name': 'index',
            'saml_path': os.path.dirname(__file__),
            'lowercase_urlencoding': True
        },
        True,
        'http',
        'off'
    )
])
def test_init(settings, lowercase, scheme, https):
    with testConfig(settings={'pyramid_saml': settings}) as config:
        _load_settings(config)
        config.add_route('index', '/')
        request = __get_request()
        request.scheme = scheme
        saml = SAML(request)

        assert isinstance(saml, SAML)
        assert saml._request == request
        assert saml._settings == settings
        assert saml._saml_request['lowercase_urlencoding'] == lowercase
        assert saml._saml_request['https'] == https
        assert isinstance(saml.auth, OneLogin_Saml2_Auth)


def test_metadata():

    def validate_metadata(metadata):
        return []

    settings = {
        'index_route_name': 'index',
        'saml_path': os.path.dirname(__file__)
    }
    with testConfig(settings={'pyramid_saml': settings}) as config:
        _load_settings(config)
        config.add_route('index', '/')
        request = __get_request()
        saml = SAML(request)
        settings = saml.auth.get_settings()
        settings.validate_metadata = validate_metadata
        response = saml.metadata()

        assert isinstance(response, HTTPOk)
        assert response.headers['Content-Type'] == 'text/xml'


def test_metadata_error():

    def validate_metadata(metadata):
        return ['error1']

    settings = {
        'index_route_name': 'index',
        'saml_path': os.path.dirname(__file__)
    }
    with testConfig(settings={'pyramid_saml': settings}) as config:
        _load_settings(config)
        config.add_route('index', '/')
        request = __get_request()
        saml = SAML(request)
        settings = saml.auth.get_settings()
        settings.validate_metadata = validate_metadata

        with pytest.raises(HTTPInternalServerError) as e:
            saml.metadata()
            assert '{}'.format(e) == 'error1'


@pytest.mark.parametrize('redirect', [
    None,
    'https://example.com/foo'
])
def test_sso(redirect):

    def login(return_to=None):
        return return_to

    settings = {
        'index_route_name': 'index',
        'saml_path': os.path.dirname(__file__)
    }
    with testConfig(settings={'pyramid_saml': settings}) as config:
        _load_settings(config)
        config.add_route('index', '/')
        request = __get_request()
        if redirect is not None:
            request.params['redirect'] = redirect
        saml = SAML(request)
        saml.auth.login = login
        response = saml.sso()

        assert isinstance(response, HTTPFound)
        if redirect is not None:
            assert response.location == redirect
        else:
            assert response.location == 'http://example.com/'


def test_slo():

    def logout(name_id=None, session_index=None):
        assert name_id == 'foo'
        assert session_index == 'bar'
        return 'http://example.com/'

    settings = {
        'index_route_name': 'index',
        'saml_path': os.path.dirname(__file__)
    }
    with testConfig(settings={'pyramid_saml': settings}) as config:
        _load_settings(config)
        config.add_route('index', '/')
        request = __get_request()
        request.session[SAML_NAME_ID] = 'foo'
        request.session[SAML_SESSION_INDEX] = 'bar'
        saml = SAML(request)
        saml.auth.logout = logout
        response = saml.slo()

        assert isinstance(response, HTTPFound)
        assert response.location == 'http://example.com/'


@pytest.mark.parametrize('errors,relay_state', [
    (['error1'], None),
    ([], None),
    ([], 'http://example.com/foo')
])
def test_acs(errors, relay_state):

    def process_response():
        pass

    def get_errors():
        return errors

    def get_last_error_reason():
        if len(errors) > 0:
            return errors[-1]
        return None

    def get_attributes():
        return {
            'foo': 'bar'
        }

    def get_nameid():
        return 'NameId'

    def get_session_index():
        return 'SessionIndex'

    def redirect_to(url):
        return url

    settings = {
        'index_route_name': 'index',
        'saml_path': os.path.dirname(__file__)
    }
    with testConfig(settings={'pyramid_saml': settings}) as config:
        _load_settings(config)
        config.add_route('index', '/')
        request = __get_request()
        if relay_state is not None:
            request.POST['RelayState'] = relay_state
        saml = SAML(request)
        saml.auth.process_response = process_response
        saml.auth.get_errors = get_errors
        saml.auth.get_last_error_reason = get_last_error_reason
        saml.auth.get_attributes = get_attributes
        saml.auth.get_nameid = get_nameid
        saml.auth.get_session_index = get_session_index
        saml.auth.redirect_to = redirect_to
        response = saml.acs()

        assert isinstance(response, HTTPFound)
        if len(errors) > 0:
            assert saml._session[SAML_ERROR] == errors[-1]
            assert SAML_USER_DATA not in saml._session
            assert SAML_NAME_ID not in saml._session
            assert SAML_SESSION_INDEX not in saml._session
        else:
            assert saml._session[SAML_ERROR] is None
            assert saml._session[SAML_USER_DATA] == {
                'foo': 'bar'
            }
            assert saml._session[SAML_NAME_ID] == 'NameId'
            assert saml._session[SAML_SESSION_INDEX] == 'SessionIndex'
        if relay_state is None:
            assert response.location == 'http://example.com/'
        else:
            assert response.location == relay_state


@pytest.mark.parametrize('url,errors',  [
    (None, ['error1']),
    ('https://example.com/foo', [])
])
def test_sls(url, errors):

    def process_slo(delete_session_cb=None):
        delete_session_cb()
        return url

    def get_errors():
        return errors

    def get_last_error_reason():
        if len(errors) > 0:
            return errors[-1]
        return None

    settings = {
        'index_route_name': 'index',
        'saml_path': os.path.dirname(__file__)
    }
    with testConfig(settings={'pyramid_saml': settings}) as config:
        _load_settings(config)
        config.add_route('index', '/')
        request = __get_request()
        saml = SAML(request)
        saml.auth.process_slo = process_slo
        saml.auth.get_errors = get_errors
        saml.auth.get_last_error_reason = get_last_error_reason
        saml._session[SAML_NAME_ID] = 'foo'
        response = saml.sls()

        assert isinstance(response, HTTPFound)
        if url is None:
            assert response.location == 'http://example.com/'
        else:
            assert response.location == url
        if len(errors) > 0:
            assert saml._session[SAML_ERROR] == errors[-1]
        else:
            assert SAML_ERROR not in saml._session
        assert SAML_NAME_ID not in saml._session


def test_load_settings_from_file():
    settings = {
        'saml_path': os.path.dirname(__file__)
    }
    with testConfig(settings={'pyramid_saml': settings}) as config:
        _load_settings_from_file(config)
        cfg = config.get_settings()['pyramid_saml']
        assert cfg['debug']
        assert cfg['sp']['entityId'] == 'https://example.com/metadata/'
        assert cfg['idp']['entityId'] == \
            'https://app.onelogin.com/saml/metadata/0'
        assert cfg['organization']['en-US']['name'] == 'sp_test'


@pytest.mark.parametrize('settings,env_url,env_id,num', [
    ({
        'idp': {
            'entityId': 'initial'
        }
    }, None, None, 1),
    ({
        'metadata_url': 'http://example.com/metadata2'
    }, None, None, 2),
    ({
        'idp': {
            'entityId': 'initial'
        }
    }, 'http://example.com/metadata3', None, 3),
    ({
        'idp': {
            'entityId': 'initial'
        }
    }, 'http://example.com/metadata4', 'from_env', 4)
])
def test_load_settings_from_url(settings, env_url, env_id, num):

    def parse_remote(metadata_url, entity_id=None):
        result = {
            'idp': {
                'url': metadata_url
            }
        }
        if entity_id is not None:
            result['idp']['entityId'] = entity_id
        return result

    OneLogin_Saml2_IdPMetadataParser.parse_remote = parse_remote

    if env_url is not None:
        os.environ['PYRAMID_SAML_METADATA_URL'] = env_url

    if env_id is not None:
        os.environ['PYRAMID_SAML_IDP_ENTITY_ID'] = env_id

    with testConfig(settings={'pyramid_saml': settings}) as config:
        _load_settings_from_url(config)
        idp = config.get_settings()['pyramid_saml']['idp']
        if num == 1:
            assert idp['entityId'] == 'initial'
            assert 'url' not in idp
        elif num == 2:
            assert 'entityId' not in idp
            assert idp['url'] == 'http://example.com/metadata2'
        elif num == 3:
            assert idp['entityId'] == 'initial'
            assert idp['url'] == 'http://example.com/metadata3'
        elif num == 4:
            assert idp['entityId'] == 'from_env'
            assert idp['url'] == 'http://example.com/metadata4'


@pytest.mark.parametrize('settings', [
    {},
    {
        'pyramid_saml': {}
    }
])
def test_load_settings_fail(settings):
    with testConfig(settings=settings) as config:
        with pytest.raises(AssertionError):
            _load_settings(config)


@pytest.mark.parametrize('settings,env', [
    ({}, {
        'PYRAMID_SAML_PATH': os.path.dirname(__file__)
    }),
    ({
        'pyramd_saml': {}
    }, {
        'PYRAMID_SAML_PATH': os.path.dirname(__file__)
    }),
    ({
        'pyramd_saml': {
            'saml_path': os.path.dirname(__file__)
        }
    }, {})
])
def test_load_settings(settings, env):
    os.environ.update(env)
    with testConfig(settings=settings) as config:
        _load_settings(config)
        cfg = config.get_settings()['pyramid_saml']
        assert cfg['debug']
        assert cfg['sp']['entityId'] == 'https://example.com/metadata/'
