from applipy import Config
from applipy.config.protocol import ConfigProtocol


class Upper(ConfigProtocol):

    def provide_for(self, protocol, key):
        if protocol in ('up', 'upper'):
            return key.upper()

        return None


class Capitalize(ConfigProtocol):

    def provide_for(self, protocol, key):
        if protocol == 'cap':
            return key.capitalize()

        return None


def test_config():

    raw_config = {
            'app': {'name': 'config-test', 'priority': 40},
            'app.type': 5,
            'db.password.value': 'up:seCret',
            'db.password.is_secret': True,
            'name': {'of': {'process': 'cap:foo'}},
            'name.of.file': 'upper:unknown',
            'private.files': [{'name': 'foo', 'meta': {'type': 'json'}}, {'name': 'bar', 'meta.type': 'yaml'}],
            'list.of.lists': [
                [{'a': 1}, {'b': 2}],
                [{'c': {'d': 3}}],
            ],
            'indirect.list.recursion': [{'foo': [{'bar': [{'z': {'w': 'upper:waves'}}]}]}]
    }
    config = Config(raw_config, [Capitalize()])
    config.addProtocol(Upper())

    assert config.keys() == {'app.name', 'app.priority', 'app.type', 'db.password.value', 'db.password.is_secret',
                             'name.of.process', 'name.of.file', 'private.files', 'list.of.lists',
                             'indirect.list.recursion'}
    assert config.get('private.files')[0].keys() == {'name', 'meta.type'}
    assert config.get('private.files')[1].keys() == {'name', 'meta.type'}

    assert config['app.name'] == 'config-test'
    assert config.get('app.priority') == 40
    assert config.get('app.type') == 5
    assert config.get('db.password.value') == 'SECRET'
    assert config.get('db.password.is_secret') is True
    assert config['name'].get('of.process') == 'Foo'
    assert config['name']['of.file'] == 'UNKNOWN'
    assert config.get('app.not-there', 69) == 69
    assert config['private.files'][0].get('name') == 'foo'
    assert config['private.files'][0]['meta.type'] == 'json'
    assert config['private.files'][1]['meta']['type'] == 'yaml'
    assert config['list.of.lists'][1][0]['c.d'] == 3
    assert config['indirect.list.recursion'][0]['foo'][0]['bar'][0]['z.w'] == 'WAVES'


def test_protocols():

    upper = Upper()
    capitalize = Capitalize()
    config = Config({}, [upper])

    assert len(config.protocols) == 1
    assert config.protocols[0] is upper

    config.addProtocol(capitalize)

    assert len(config.protocols) == 2
    assert config.protocols[0] is upper
    assert config.protocols[1] is capitalize
