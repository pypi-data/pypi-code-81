import pytest
from luqum.parser import parser

from oarepo_search.query_parsers import luqum_query_parser

test_params = [
    (
        "title.cs:auto", {
            'match': {'title.cs': {'query': 'auto', 'zero_terms_query': 'none'}}
        }
    ),
    (
        "creator.title.cs:Švejk", {
            'nested': {
                'path': 'creator',
                'query': {
                    'match': {
                        'creator.title.cs': {
                            'query': 'Švejk',
                            'zero_terms_query': 'none'
                        }
                    }
                }
            }
        }
    )
]


@pytest.mark.parametrize("input,expected", test_params)
def test_luqum_query_parser(app, input, expected):
    mapping = {
        "aliases": {
            "test-records-record": {}
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "object",
                    "properties": {
                        "cs": {
                            "type": "text"
                        },
                        "en": {
                            "type": "text"
                        }
                    }
                },
                "creator": {
                    "type": "nested",
                    "properties": {
                        "role": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "object",
                                    "properties": {
                                        "cs": {
                                            "type": "text"
                                        },
                                        "en": {
                                            "type": "text"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    tree = parser.parse(input)
    assert luqum_query_parser(tree, mapping=mapping).to_dict() == expected


def test_luqum_query_parser_2(app):
    mapping = {
        "mappings": {}
    }
    tree = parser.parse("query")
    with pytest.raises(Exception, match="You cannot specify both index_name and mapping"):
        luqum_query_parser(tree, mapping=mapping, index_name="bla")
