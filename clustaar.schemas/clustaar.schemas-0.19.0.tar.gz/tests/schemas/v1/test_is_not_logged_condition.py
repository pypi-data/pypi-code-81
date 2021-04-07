from clustaar.schemas.v1 import IS_NOT_LOGGED_CONDITION
from clustaar.schemas.models import IsNotLoggedCondition
import pytest


@pytest.fixture
def condition():
    return IsNotLoggedCondition()


@pytest.fixture
def data():
    return {"type": "is_not_logged"}


class TestDump(object):
    def test_returns_data(self, condition, data, mapper):
        result = mapper.dump(condition)
        assert data == result


class TestLoad(object):
    def test_returns_a_condition(self, condition, data, mapper):
        condition = mapper.load(data, IS_NOT_LOGGED_CONDITION)
        assert isinstance(condition, IsNotLoggedCondition)
