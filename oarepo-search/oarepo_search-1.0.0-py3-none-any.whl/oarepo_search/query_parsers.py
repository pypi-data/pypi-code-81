from elasticsearch_dsl import Q
from luqum.elasticsearch import SchemaAnalyzer, ElasticsearchQueryBuilder
from luqum.parser import parser
from luqum.tree import Word

from oarepo_search.proxies import current_oarepo_search
from oarepo_search.utils import get_mapping, replace_language_placeholder


def query_parser(qstr: str = None, index_name: str = None, endpoint_name: str = None):
    if not qstr:
        return Q()
    tree = parser.parse(qstr)
    if isinstance(tree, Word):
        return simple_query_parser(qstr, endpoint_name)
    return luqum_query_parser(tree, index_name)


def simple_query_parser(qstr: str = None, endpoint_name: str = None):
    """Docs for query_string: https://www.elastic.co/guide/en/elasticsearch/reference/current
    /query-dsl-query-string-query.html"""
    languages = current_oarepo_search.supported_languages
    fields = current_oarepo_search.get_fields(endpoint_name)
    new_fields = []
    for field in fields:
        expanded = replace_language_placeholder(field, languages)
        new_fields.extend(expanded)
    fields = new_fields
    assert isinstance(fields, list), f"NR_SEARCH_FIELDS must be list, not {type(fields)}"
    if fields:
        return Q('query_string', query=qstr, fields=fields)
    else:
        return Q('query_string', query=qstr)


def luqum_query_parser(tree, index_name=None, mapping=None):
    if index_name and mapping:
        raise Exception("You cannot specify both index_name and mapping")
    if not mapping:  # pragma: no cover
        mapping = get_mapping(index_name)
    schema_analyzer = SchemaAnalyzer(mapping)
    q_builder_opt = schema_analyzer.query_builder_options()
    es_builder = ElasticsearchQueryBuilder(**q_builder_opt)
    query = es_builder(tree)
    return Q(query)
