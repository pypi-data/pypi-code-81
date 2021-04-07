from clustaar.schemas.v1 import FLOW_CONNECTION_USER_PREDICATE
from clustaar.schemas.models import ConnectionUserPredicate, IsLoggedCondition
import pytest


@pytest.fixture
def data():
    return {"type": "connection_user_predicate", "condition": {"type": "is_logged"}}


@pytest.fixture
def predicate():
    return ConnectionUserPredicate(condition=IsLoggedCondition())


class TestLoad(object):
    def test_returns_a_predicate(self, data, mapper):
        result = mapper.load(data, FLOW_CONNECTION_USER_PREDICATE)
        assert isinstance(result, ConnectionUserPredicate)
        assert isinstance(result.condition, IsLoggedCondition)


class TestDump(object):
    def test_returns_a_dict(self, data, mapper, predicate):
        result = mapper.dump(predicate, FLOW_CONNECTION_USER_PREDICATE)
        assert result == data
