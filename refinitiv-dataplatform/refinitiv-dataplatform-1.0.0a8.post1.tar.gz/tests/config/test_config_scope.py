import pytest


def test_scope_module_get_default_config_file():
    try:
        import refinitiv.dataplatform.configure as config
        _ = config._get_filepath
    except AttributeError as e:
        pytest.fail(str(e))


def test_scope_module_get_config():
    try:
        from refinitiv.dataplatform.configure import config
    except AttributeError as e:
        pytest.fail(str(e))


def test_scope_module():
    try:
        import refinitiv.dataplatform.configure
    except AttributeError as e:
        pytest.fail(str(e))
