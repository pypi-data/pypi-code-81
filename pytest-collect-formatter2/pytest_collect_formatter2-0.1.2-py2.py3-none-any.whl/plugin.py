import inspect
import json
import os
import xml.dom.minidom

import dicttoxml
import yaml


def pytest_addoption(parser):
    group = parser.getgroup('collect-formatter2')
    group.addoption("--collect-output-file", action="store", default=False,
                    help="Saves collected test items to the file", )
    group.addoption("--collect-format", action="store", default='json',
                    help="Saves collected test items specified format [xml, yaml, json], default JSON", )
    group.addoption("--collect-type", action="store", default='classic',
                    help="Format output results in classic pytest view or in 'path' view [classic, path], default classic", )
    group.addoption("--with-remark", action="store", default=True,
                    help="collect method remark,priority: 1st-allure.title 2nd-method python doc 3rd-method comment")


def get_item_remark(item):
    obj = getattr(item, "obj", None)
    # 1st: support allure.title
    remark = getattr(obj, "__allure_display_name__", None)
    if remark:
        return remark
    # 2nd: python method doc
    remark = inspect.getdoc(obj)
    if remark:
        return remark
    # 3rd: python method comment
    remark = inspect.getcomments(obj)
    return remark


def check_parent(item, item_data):
    if type(item).__name__ not in ["Session", "Instance"]:
        item_data = {hash(type(item).__name__ + item.name): {
            "type": type(item).__name__,
            "title": item.name,
            "remark": get_item_remark(item),
            "children": item_data
        }}
    if item.parent is not None:
        item_data = check_parent(item.parent, item_data)
    return item_data


def check_children(hierarchy, l):
    for data in l:
        if data in hierarchy:
            hierarchy[data]['children'] = check_children(hierarchy[data].get('children', {}),
                                                         l[data].get('children', {}))
        else:
            return {**hierarchy, **l}
    return hierarchy


def remove_keys_and_make_lists(hierarchy, is_with_remark):
    array = []
    for k, v in hierarchy.items():
        node = {'type': v['type'], 'title': v['title']}
        array.append(node)
        if is_with_remark:
            node["remark"] = v['remark']
        v['children'] = remove_keys_and_make_lists(v['children'], is_with_remark)
        if v['type'] != "Function":  # since Function is the minimal unit in pytest
            node['children'] = v['children']
    return array


def classic_collection(session):
    hierarchy = {}
    for item in session.items:
        l = check_parent(item, {})
        if hierarchy:
            hierarchy = check_children(hierarchy, l)
        else:
            hierarchy = l
    return hierarchy


def path_collection(session):
    hierarchy = {}
    for item in session.items:
        l = {}
        cur_h = {}
        parameterized = item.nodeid.find('[')
        if parameterized < 0:
            path = item.nodeid.split('/')
        else:
            path = item.nodeid[0: parameterized].split('/')
            path[-1] = path[-1] + item.nodeid[parameterized:]
        pytest_items = path[-1].split('::')
        path[-1] = pytest_items[0]
        pytest_items = pytest_items[1:]
        pytest_items.reverse()
        path.reverse()
        for p in pytest_items:
            l = {"pytest_unit" + p: {"type": "pytest_unit", "title": p, "children": cur_h}}
            cur_h = l
        for p in path:
            l = {"path" + p: {"type": "path", "title": p, "children": cur_h}}
            cur_h = l

        if hierarchy:
            hierarchy = check_children(hierarchy, l)
        else:
            hierarchy = l

    return hierarchy


def pytest_collection_finish(session):
    output_file = session.config.getoption('--collect-output-file')
    collect_format = session.config.getoption('--collect-format')
    collect_type = session.config.getoption('--collect-type')
    is_with_remark = session.config.getoption('--with-remark')
    hierarchy = {}
    if output_file:
        if collect_type == 'classic':
            hierarchy = classic_collection(session)
        elif collect_type == 'path':
            hierarchy = path_collection(session)

        hierarchy = remove_keys_and_make_lists(hierarchy, is_with_remark)
        abspath = os.path.abspath(output_file)
        dirname = os.path.dirname(abspath)
        os.makedirs(name=dirname, exist_ok=True)
        with open(output_file, "w+") as f:
            if collect_format == 'json':
                f.write(json.dumps(hierarchy, indent=4))
            elif collect_format == 'yaml':
                f.write(yaml.dump(hierarchy))
            elif collect_format == 'xml':
                dom = xml.dom.minidom.parseString(dicttoxml.dicttoxml(hierarchy, attr_type=False).decode("utf-8"))
                f.write(dom.toprettyxml())
