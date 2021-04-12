from invenio_search import current_search

from oarepo_search.utils import replace_language_placeholder, get_mapping


def test_replace_language_placeholder():
    field = "title.*"
    languages = ["cs", "en"]
    assert replace_language_placeholder(field, languages) == ['title.cs', 'title.en']


def test_replace_language_placeholder_2():
    field = "note"
    languages = ["cs", "en"]
    assert replace_language_placeholder(field, languages) == ['note']


def test_get_mapping(app):
    current_search.register_mappings("records", "tests.mappings")
    mappings = get_mapping('records-record-v1.0.0')
    assert mappings == {
        'aliases': {'test-records-record': {}}, 'mappings': {
            'properties': {
                'title': {
                    'type': 'object', 'properties': {'cs': {'type': 'text'}, 'en': {'type': 'text'}}
                }
            }
        }
    }
