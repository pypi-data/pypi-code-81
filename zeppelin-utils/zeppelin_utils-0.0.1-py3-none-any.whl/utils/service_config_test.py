from . import service_config


def test_production_false(monkeypatch):
    monkeypatch.setenv('SL_ENVIRONMENT', 'test')
    assert service_config.is_production() is False


def test_production_true(monkeypatch):
    monkeypatch.setenv('SL_ENVIRONMENT', 'prod')
    assert service_config.is_production() is True


def test_stage_false(monkeypatch):
    monkeypatch.setenv('SL_ENVIRONMENT', 'test')
    assert service_config.is_stage() is False


def test_stage_true(monkeypatch):
    monkeypatch.setenv('SL_ENVIRONMENT', 'stage')
    assert service_config.is_stage() is True


def test_version(monkeypatch):
    monkeypatch.setenv('SL_VERSION', 'zeppelin-1912/dev:0.0.1')
    assert service_config.get_version() == 'zeppelin-1912/dev:0.0.1'


def test_version_short(monkeypatch):
    monkeypatch.setenv('SL_VERSION', 'zeppelin-1912/dev:0.0.1')
    assert service_config.get_version_short() == 'dev:0.0.1'


def test_version_short_none(monkeypatch):
    monkeypatch.delenv('SL_VERSION')
    assert service_config.get_version_short() is None


def test_get_info(monkeypatch):
    monkeypatch.setenv('SL_VERSION', 'zeppelin-1912/dev:0.0.1')
    monkeypatch.setenv('SL_ENVIRONMENT', 'test')
    assert service_config.get_info() == {'version': 'zeppelin-1912/dev:0.0.1', 'environment': 'test'}
