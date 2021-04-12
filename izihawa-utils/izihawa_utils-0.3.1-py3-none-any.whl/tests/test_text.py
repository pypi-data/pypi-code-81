from izihawa_utils.text import camel_to_snake


def test_camel_to_snake():
    assert camel_to_snake('CamelCase') == 'camel_case'
    assert camel_to_snake('camelCase') == 'camel_case'
    assert camel_to_snake('camelCase camel123Case') == 'camel_case camel123_case'
    assert camel_to_snake('camelCase\ncamelCase') == 'camel_case\ncamel_case'
