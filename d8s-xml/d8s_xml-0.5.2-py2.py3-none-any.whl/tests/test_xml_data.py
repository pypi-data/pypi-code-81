import xml

import pytest

from d8s_xml import (
    xml_read,
    xml_structure,
    xml_to_json,
    xml_as_string,
    is_xml,
    xml_text,
    stringify_first_arg_xml_element,
    xml_read_first_arg_string,
)
from d8s_xml.xml_data import _is_xml_element, _xml_iterate

TEST_XML_STRING_1 = '''<note>
<to>Tove</to>
<from>Jani</from>
<heading>Reminder</heading>
<body>Don't forget me this weekend!</body>
</note>'''

# more xml examples here: https://www.w3schools.com/xml/xml_examples.asp


def test_xml_text_1():
    result = xml_text(TEST_XML_STRING_1)
    assert (
        result
        == '''
 Tove 
 Jani 
 Reminder 
 Don't forget me this weekend! 
'''
    )

    result = xml_text(xml_read(TEST_XML_STRING_1))
    assert (
        result
        == '''
 Tove 
 Jani 
 Reminder 
 Don't forget me this weekend! 
'''
    )


def test__is_xml_element_1():
    assert _is_xml_element(xml_read(TEST_XML_STRING_1))
    assert not _is_xml_element('foo')
    assert not _is_xml_element(TEST_XML_STRING_1)


def test_is_xml_1():
    assert is_xml(TEST_XML_STRING_1)
    assert not is_xml('foo')


def test_xml_read_1():
    result = xml_read(TEST_XML_STRING_1)
    assert result
    assert isinstance(result, xml.etree.ElementTree.Element)


def test_xml_structure_1():
    result = xml_structure(TEST_XML_STRING_1)
    assert result == {"to": {}, "from": {}, "heading": {}, "body": {}}

    result = xml_structure(xml_read(TEST_XML_STRING_1))
    assert result == {"to": {}, "from": {}, "heading": {}, "body": {}}


def test_xml_structure_bad_input():
    with pytest.raises(TypeError):
        xml_structure(1)


def test_xml_to_json_1():
    result = xml_to_json(TEST_XML_STRING_1)
    assert result == {
        'note': [
            {
                'to': [{'_value': 'Tove'}],
                'from': [{'_value': 'Jani'}],
                'heading': [{'_value': 'Reminder'}],
                'body': [{'_value': "Don't forget me this weekend!"}],
            }
        ]
    }

    result = xml_to_json(xml_read(TEST_XML_STRING_1))
    assert result == {
        'note': [
            {
                'to': [{'_value': 'Tove'}],
                'from': [{'_value': 'Jani'}],
                'heading': [{'_value': 'Reminder'}],
                'body': [{'_value': "Don't forget me this weekend!"}],
            }
        ]
    }


def test__xml_iterate_1():
    result = _xml_iterate(TEST_XML_STRING_1)
    assert result == {'to': {}, 'from': {}, 'heading': {}, 'body': {}}


def test_xml_as_string_1():
    result = xml_as_string(xml_read(TEST_XML_STRING_1))
    assert (
        result
        == '''<note>
<to>Tove</to>
<from>Jani</from>
<heading>Reminder</heading>
<body>Don't forget me this weekend!</body>
</note>'''
    )


@stringify_first_arg_xml_element
def stringify_first_arg_xml_element_test_func_a(a):
    """."""
    return a


def test_stringify_first_arg_xml_element_1():
    xml_data = xml_read(TEST_XML_STRING_1)
    assert stringify_first_arg_xml_element_test_func_a(xml_data) == TEST_XML_STRING_1


@xml_read_first_arg_string
def xml_read_first_arg_string_test_func_a(a):
    """."""
    return a


def test_xml_read_first_arg_string_1():
    assert _is_xml_element(xml_read_first_arg_string_test_func_a(TEST_XML_STRING_1))
