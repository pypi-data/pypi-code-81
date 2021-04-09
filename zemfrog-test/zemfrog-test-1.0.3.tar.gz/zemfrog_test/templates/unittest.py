"""
Unit Testing For (API {{ name }})
"""

from flask import url_for
from flask.testing import FlaskClient

{% for spec in specs %}
def test_{{spec["func"]}}(client: FlaskClient):
    paths = {{ spec["paths"] }}
    url = url_for("{{ spec["endpoint"] }}", **paths)
    query = {{ spec["data"].pop("query", {}) }}
    {% for data_type in spec["data"].keys() -%}
    data = {{ spec["data"][data_type] }}
    {% if data_type == 'json' -%}
    resp = client.{{ spec["method"] | lower}}(url, json=data, query_string=query)
    {% elif data_type == 'files' -%}
    headers = {
        "Content-Type": "multipart/form-data"
    }
    resp = client.{{ spec["method"] | lower}}(url, data=data, query_string=query, headers=headers)
    {%- else %}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    resp = client.{{ spec["method"] | lower}}(url, data=data, query_string=query, headers=headers)
    {%- endif -%}
    {% else -%}
    resp = client.{{ spec["method"] | lower}}(url, query_string=query)
    {%- endfor %}
    assert True
{% endfor %}
