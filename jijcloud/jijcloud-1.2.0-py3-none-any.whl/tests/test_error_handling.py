import pytest
from pytest_mock import MockerFixture
from jijcloud import JijSASampler, JijSQASampler
from jijmodeling import PlaceholderArray, BinaryArray, Sum
from tests.mock_jijcloud_api import *
from jijcloud.response import DimodResponse, APIStatus
from requests.exceptions import HTTPError
import requests
import json

class TestErrorHandling:
    def test_error_bad_request(self, mocker: MockerFixture):

        error_dict = {'detail': 'hoge'}
        mock_solution = DimodResponse.from_samples([0,1,0], 'BINARY', 0).to_serializable()

        mocker.patch.object(requests, 'post', lambda *args, **kwargs: mock_request_post_query_err_bad_request(error_dict, *args, **kwargs))
        mocker.patch.object(requests, 'get', lambda *args, **kwargs: mock_request_get(mock_solution, *args, **kwargs))

        with pytest.raises(HTTPError) as e:
            sampler = JijSASampler(config='./tests/testconfig.toml')
            
            # make problem
            d = PlaceholderArray('d', dim=1)
            n = d.shape[0]
            x = BinaryArray('x', shape=(n,))
            model = (Sum({'i': n}, d['i']*x['i']) - 1)**2

            # instance
            data = {'d': [1,2,3]*10}
            result = sampler.sample_model(model, data, {})

        # check if the data passed correctly
        assert(json.dumps(e.value.args[1]) == json.dumps(error_dict))


    def test_error_internal_server_error(self, mocker: MockerFixture):

        error_dict = {'detail': 'hoge'}
        mock_solution = DimodResponse.from_samples([0,1,0], 'BINARY', 0).to_serializable()

        mocker.patch.object(requests, 'post', lambda *args, **kwargs: mock_request_post_query_err_internal_server_error(error_dict, *args, **kwargs))
        mocker.patch.object(requests, 'get', lambda *args, **kwargs: mock_request_get(mock_solution, *args, **kwargs))

        with pytest.raises(HTTPError) as e:
            sampler = JijSASampler(config='./tests/testconfig.toml')
            
            # make problem
            d = PlaceholderArray('d', dim=1)
            n = d.shape[0]
            x = BinaryArray('x', shape=(n,))
            model = (Sum({'i': n}, d['i']*x['i']) - 1)**2

            # instance
            data = {'d': [1,2,3]*10}
            result = sampler.sample_model(model, data, {})

        # check if the data passed correctly
        assert(json.dumps(e.value.args[1]) == json.dumps(error_dict))

    def test_error_internal_server_error_without_dict(self, mocker: MockerFixture):

        error_dict = None
        mock_solution = DimodResponse.from_samples([0,1,0], 'BINARY', 0).to_serializable()

        mocker.patch.object(requests, 'post', lambda *args, **kwargs: mock_request_post_query_err_internal_server_error(error_dict, *args, **kwargs))
        mocker.patch.object(requests, 'get', lambda *args, **kwargs: mock_request_get(mock_solution, *args, **kwargs))

        with pytest.raises(HTTPError) as e:
            sampler = JijSASampler(config='./tests/testconfig.toml')
            
            # make problem
            d = PlaceholderArray('d', dim=1)
            n = d.shape[0]
            x = BinaryArray('x', shape=(n,))
            model = (Sum({'i': n}, d['i']*x['i']) - 1)**2

            # instance
            data = {'d': [1,2,3]*10}
            result = sampler.sample_model(model, data, {})

        # check if the HTTPError is thrown.


    def test_error_get_invalid_id(self, mocker: MockerFixture):

        error_dict = {'detail': 'invalid_id'}

        mocker.patch.object(requests, 'post', mock_request_post)
        mocker.patch.object(requests, 'get', mock_request_get_invalid_id)

        with pytest.raises(HTTPError) as e:
            sampler = JijSASampler(config='./tests/testconfig.toml')
            
            # make problem
            d = PlaceholderArray('d', dim=1)
            n = d.shape[0]
            x = BinaryArray('x', shape=(n,))
            model = (Sum({'i': n}, d['i']*x['i']) - 1)**2

            # instance
            data = {'d': [1,2,3]*10}
            result = sampler.sample_model(model, data, {})

        # check if the data passed correctly
        assert(json.dumps(e.value.args[1]) == json.dumps(error_dict))

    def test_error_get_failed(self, mocker: MockerFixture):

        error_dict = {'message': 'invalid dim param in solver'}

        mocker.patch.object(requests, 'post', mock_request_post)
        mocker.patch.object(requests, 'get', lambda *args, **kwargs: mock_request_get_failed(error_dict, *args, **kwargs))

        sampler = JijSASampler(config='./tests/testconfig.toml')
        
        # make problem
        d = PlaceholderArray('d', dim=1)
        n = d.shape[0]
        x = BinaryArray('x', shape=(n,))
        model = (Sum({'i': n}, d['i']*x['i']) - 1)**2

        # instance
        data = {'d': [1,2,3]*10}
        result = sampler.sample_model(model, data, {})

        assert result.status == APIStatus.FAILED
        assert(json.dumps(result.error_message) == json.dumps(error_dict))

    def test_error_get_unknownerror(self, mocker: MockerFixture):

        mocker.patch.object(requests, 'post', mock_request_post)
        mocker.patch.object(requests, 'get', mock_request_get_unknownerror)

        sampler = JijSASampler(config='./tests/testconfig.toml')
        
        # make problem
        d = PlaceholderArray('d', dim=1)
        n = d.shape[0]
        x = BinaryArray('x', shape=(n,))
        model = (Sum({'i': n}, d['i']*x['i']) - 1)**2

        # instance
        data = {'d': [1,2,3]*10}
        result = sampler.sample_model(model, data, {})

        assert result.status == APIStatus.UNKNOWNERROR

