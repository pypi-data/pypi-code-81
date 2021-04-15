import pytest

from insnail_ai_tools.config import ApolloConfig, YamlConfig


def test_apollo_config():
    class Config(ApolloConfig):
        TEST_FLAG: int = 1

    config = Config(
        "ai-comm-center",
        "http://10.0.0.176:8080",
        "default",
    )
    config.fetch()
    print(config.TEST_FLAG)
    assert config.TEST_FLAG == 10


def test_yaml_config():
    class Config(YamlConfig):
        MONGO_URI: str = None

    config = Config("./tests/test_config.yaml")
    config.fetch()
    assert config.MONGO_URI == "mongo_uri"
