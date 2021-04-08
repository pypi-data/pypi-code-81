import pytest
from pytest_mock import MockerFixture
from jijcloud import JijSASampler, JijSQASampler
from jijmodeling import PlaceholderArray, BinaryArray, Sum
from tests.mock_jijcloud_api import mock_request_get, mock_request_post
from jijcloud.response import DimodResponse
import requests
import json

class TestOpenJijSolver:
    def test_jijmodeling_sa(self, mocker: MockerFixture):

        mock_solution = DimodResponse.from_samples([0,1,0], 'BINARY', 0).to_serializable()

        mocker.patch.object(requests, 'post', mock_request_post)
        mocker.patch.object(requests, 'get', lambda *args, **kwargs: mock_request_get(mock_solution, *args, **kwargs))

        sampler = JijSASampler(config='./tests/testconfig.toml')
        
        # make problem
        d = PlaceholderArray('d', dim=1)
        n = d.shape[0]
        x = BinaryArray('x', shape=(n,))
        model = (Sum({'i': n}, d['i']*x['i']) - 1)**2

        # instance
        data = {'d': [1,2,3]*10}
        result = sampler.sample_model(model, data, {})
        assert json.dumps(result.to_serializable()) == json.dumps(mock_solution)
        
        # async model
        result = sampler.sample_model(model, data, {}, sync=False)
        # result status is PENDING
        assert json.dumps(result.to_serializable()) != json.dumps(mock_solution)
        # return value of get_result has a solution
        assert json.dumps(result.get_result().to_serializable()) == json.dumps(mock_solution)
        # so is the original result
        assert json.dumps(result.to_serializable()) == json.dumps(mock_solution)


    def test_bqm_sa(self, mocker: MockerFixture):

        mock_solution = DimodResponse.from_samples([0,1,0], 'BINARY', 0).to_serializable()

        mocker.patch.object(requests, 'post', mock_request_post)
        mocker.patch.object(requests, 'get', lambda *args, **kwargs: mock_request_get(mock_solution, *args, **kwargs))

        sampler = JijSASampler(config='./tests/testconfig.toml')

        qubo = {(0, 1): -1, (0, 0): 1}
        result = sampler.sample_qubo(qubo)
        assert json.dumps(result.to_serializable()) == json.dumps(mock_solution)

        # async model
        result = sampler.sample_qubo(qubo, sync=False)
        # result status is PENDING
        assert json.dumps(result.to_serializable()) != json.dumps(mock_solution)
        # return value of get_result has a solution
        assert json.dumps(result.get_result().to_serializable()) == json.dumps(mock_solution)
        # so is the original result
        assert json.dumps(result.to_serializable()) == json.dumps(mock_solution)

    def test_jijmodeling_sqa(self, mocker: MockerFixture):

        mock_solution = DimodResponse.from_samples([0,1,0], 'BINARY', 0).to_serializable()

        mocker.patch.object(requests, 'post', mock_request_post)
        mocker.patch.object(requests, 'get', lambda *args, **kwargs: mock_request_get(mock_solution, *args, **kwargs))

        sampler = JijSQASampler(config='./tests/testconfig.toml')
        
        # make problem
        d = PlaceholderArray('d', dim=1)
        n = d.shape[0]
        x = BinaryArray('x', shape=(n,))
        model = (Sum({'i': n}, d['i']*x['i']) - 1)**2

        # instance
        data = {'d': [1,2,3]*10}
        result = sampler.sample_model(model, data, {})
        assert json.dumps(result.to_serializable()) == json.dumps(mock_solution)
        
        # async model
        result = sampler.sample_model(model, data, {}, sync=False)
        # result status is PENDING
        assert json.dumps(result.to_serializable()) != json.dumps(mock_solution)
        # return value of get_result has a solution
        assert json.dumps(result.get_result().to_serializable()) == json.dumps(mock_solution)
        # so is the original result
        assert json.dumps(result.to_serializable()) == json.dumps(mock_solution)


    def test_bqm_sqa(self, mocker: MockerFixture):

        mock_solution = DimodResponse.from_samples([0,1,0], 'BINARY', 0).to_serializable()

        mocker.patch.object(requests, 'post', mock_request_post)
        mocker.patch.object(requests, 'get', lambda *args, **kwargs: mock_request_get(mock_solution, *args, **kwargs))

        sampler = JijSQASampler(config='./tests/testconfig.toml')

        qubo = {(0, 1): -1, (0, 0): 1}
        result = sampler.sample_qubo(qubo)
        assert json.dumps(result.to_serializable()) == json.dumps(mock_solution)

        # async model
        result = sampler.sample_qubo(qubo, sync=False)
        # result status is PENDING
        assert json.dumps(result.to_serializable()) != json.dumps(mock_solution)
        # return value of get_result has a solution
        assert json.dumps(result.get_result().to_serializable()) == json.dumps(mock_solution)
        # so is the original result
        assert json.dumps(result.to_serializable()) == json.dumps(mock_solution)

