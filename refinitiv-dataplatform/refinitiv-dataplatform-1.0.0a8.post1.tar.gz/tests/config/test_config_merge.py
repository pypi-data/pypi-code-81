import json
from importlib import reload

import pytest

from refinitiv.dataplatform import configure


def test_merge_two_files_top_more_complex(tmp_path):
    p = tmp_path / "top.json"
    d = {
        "prop": {
            "foo": "rewritten",
            "inner_prop": {
                "inner_foo": "rewritten",
            }

        }
    }
    p.write_text(json.dumps(d))
    paths = [p]
    p = tmp_path / "bottom.json"
    d = {
        "prop": {
            "foo": "value",
            "buzz": "buzz_value",
            "inner_prop": {
                "inner_foo": "value",
                "inner_buzz": "buzz_value",
            }
        }
    }
    p.write_text(json.dumps(d))
    paths.append(p)

    reload(configure)
    cfg = configure._create_rdpconfig(paths)
    assert cfg['prop']['foo'] == 'rewritten'
    assert cfg['prop']['inner_prop']['inner_foo'] == 'rewritten'
    assert cfg['prop']['buzz'] == 'buzz_value'
    assert 'inner_buzz' in cfg.get('prop.inner_prop'), str(cfg)
    assert cfg.get('prop.inner_prop.inner_buzz') == 'buzz_value', str(cfg)


def test_merge_two_files_top_more_simple(tmp_path):
    p = tmp_path / "top.json"
    p.write_text('{"prop_1": "value_1", "prop_2": "value_2"}')
    paths = [p]
    p = tmp_path / "bottom.json"
    p.write_text('{"prop": "value"}')
    paths.append(p)

    reload(configure)
    cfg = configure._create_rdpconfig(paths)
    assert cfg.get('prop') == 'value'
    assert cfg.get('prop_2') == 'value_2'
    assert cfg.get('prop_1') == 'value_1'


def test_merge_two_files_bottom_more(tmp_path):
    p = tmp_path / "top.json"
    p.write_text('{"prop": "prop_value"}')
    paths = [p]
    p = tmp_path / "bottom.json"
    p.write_text('{"prop_1": "value_1", "prop_2": "value_2"}')
    paths.append(p)

    reload(configure)
    cfg = configure._create_rdpconfig(paths)
    assert cfg.get('prop_1') == 'value_1'
    assert cfg.get('prop_2') == 'value_2'
    assert cfg.get('prop') == 'prop_value'


def test_merge_two_files_equal(tmp_path):
    p = tmp_path / "top.json"
    p.write_text('{"prop": "value_2"}')
    paths = [p]
    p = tmp_path / "bottom.json"
    p.write_text('{"prop": "value_1"}')
    paths.append(p)

    reload(configure)
    cfg = configure._create_rdpconfig(paths)
    assert cfg.get('prop') == 'value_2'


def test_merge_three_files(tmp_path):
    p = tmp_path / "top.json"
    p.write_text('{"prop": "value_3"}')
    paths = [p]
    p = tmp_path / "middle.json"
    p.write_text('{"prop": "value_2"}')
    paths.append(p)
    p = tmp_path / "bottom.json"
    p.write_text('{"prop": "value_1"}')
    paths.append(p)

    reload(configure)
    cfg = configure._create_rdpconfig(paths)
    assert cfg.get('prop') == 'value_3'


def test_merge_config_with_config_from_file(tmp_path):
    p = tmp_path / "config.json"
    p.write_text('{"prop": "value_2"}')
    paths = [p]

    reload(configure)
    cfg = configure._create_rdpconfig(paths)
    cfg.update({
        "prop": "value_1",
        "prop_1": "value_11",
    })
    assert 'value_1' == cfg.get('prop')
    assert 'value_11' == cfg.get('prop_1')


def test_no_error_while_load_bad_json(tmp_path):
    p = tmp_path / f"bad.json"
    p.write_text('{"prop": fail}')

    reload(configure)
    configure._create_rdpconfig([p])


def test_no_error_while_no_file(tmp_path):
    d = tmp_path / f"simple_dir"
    d.mkdir()

    reload(configure)
    configure._create_rdpconfig([d])
