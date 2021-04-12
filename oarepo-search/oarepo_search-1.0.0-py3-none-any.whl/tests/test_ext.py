from oarepo_search.proxies import current_oarepo_search


def test_ext(app):
    state = current_oarepo_search
    assert state.supported_languages == ["cs", "en"]
    assert state.search_fields == {}
    assert state.get_fields("bla") == []
