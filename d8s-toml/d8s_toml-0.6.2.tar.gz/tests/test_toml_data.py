from d8s_toml import is_toml, toml_read, toml_write

TEST_TOML_DATA = '''title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00

[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
connection_max = 5000
enabled = true

[servers]

[servers.alpha]
ip = "10.0.0.1"
dc = "eqdc10"

[servers.beta]
ip = "10.0.0.2"
dc = "eqdc10"

[clients]
data = [ ["gamma", "delta"], [1, 2] ]

hosts = [
  "alpha",
  "omega"
]'''


def test_toml_read_1():
    result = toml_read(TEST_TOML_DATA)
    print(result)
    assert result['title'] == 'TOML Example'
    assert result['owner']['name'] == 'Tom Preston-Werner'


def test_toml_write_1():
    d = {'a': 'Easy!', 'b': {'c': 2, 'd': [3, 4]}}
    result = toml_write(d)
    print(result)
    assert result == 'a = "Easy!"\n\n[b]\nc = 2\nd = [ 3, 4,]\n'

    result = toml_write(toml_read(TEST_TOML_DATA))
    assert (
        result
        == '''title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00

[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002,]
connection_max = 5000
enabled = true

[clients]
data = [ [ "gamma", "delta",], [ 1, 2,],]
hosts = [ "alpha", "omega",]

[servers.alpha]
ip = "10.0.0.1"
dc = "eqdc10"

[servers.beta]
ip = "10.0.0.2"
dc = "eqdc10"
'''
    )


def test_is_toml_1():
    assert is_toml(TEST_TOML_DATA)

    s = '''sunday: 10
monday: 11'''
    assert not is_toml(s)
