import pytest

import refinitiv.dataplatform as rdp


def test_get_last_result_not_exists():
    with pytest.raises(AttributeError):
        rdp.get_last_result


def test_get_chain_async_not_exists():
    with pytest.raises(AttributeError):
        rdp.get_chain_async


def test_get_last_error_status_not_exists():
    with pytest.raises(AttributeError):
        rdp.get_last_error_status


def test_get_news_headlines_async_not_exists():
    with pytest.raises(AttributeError):
        rdp.get_news_headlines_async


def test_get_news_story_async_not_exists():
    with pytest.raises(AttributeError):
        rdp.get_news_story_async


def test_get_prev_headlines_not_exists():
    with pytest.raises(AttributeError):
        rdp.get_prev_headlines


def test_get_next_headlines_not_exists():
    with pytest.raises(AttributeError):
        rdp.get_next_headlines


def test_set_app_key_not_exists():
    with pytest.raises(AttributeError):
        rdp.set_app_key
