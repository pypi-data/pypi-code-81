import copy
import json
import os

from NamedAtomicLock import NamedAtomicLock
from deepmerge import conservative_merger

from oarepo_mapping_includes import Mapping

inherited_merger = conservative_merger


def process_type(prop, field, includes, add_field=True, root=None, content_pointer=None, processed_types=None):
    # get the type - it can be a simple type or an array (think of multiple inheritance)
    mapping_types = prop.pop(field, None)
    if not mapping_types:
        return prop, False  # strange, should never happen

    if not isinstance(mapping_types, list):
        mapping_types = [mapping_types]

    # will contain merged parent types
    modified = False
    if processed_types is None:
        processed_types = set()

    orig_mapping_types = [*mapping_types]

    while mapping_types:
        mpt = mapping_types.pop(0)
        # for each of the mapping type
        if mpt in processed_types:
            continue

        processed_types.add(mpt)

        # try to load the type
        mapping = includes.load_type(mpt, content=prop, root=root, content_pointer=content_pointer)

        if not mapping:
            continue
        modified = True

        # if it is an instance of loaded mapping and it already took care of extra data in original,
        # just replace the original
        if isinstance(mapping, Mapping) and not mapping.merge:
            prop.clear()
            prop.update(copy.deepcopy(mapping.mapping))
        else:
            # otherwise merge with the original
            if isinstance(mapping, Mapping):
                mapping = mapping.mapping

            # merge into mpt_res, overwriting any previously existing values
            inherited_merger.merge(prop, mapping)

        # oarepo:type is a special construct to use the type but break recursion
        new_type = prop.pop('oarepo:type', None)
        if new_type:
            prop[field] = new_type
            continue

        # extract the new type
        new_type = prop.get(field, None)
        if not new_type:
            continue

        mpt = new_type
        if not isinstance(mpt, (tuple, list)):
            mpt = [mpt]
        mapping_types = mpt + mapping_types

    # if included mappings do not add type, use the first one in the original type
    if add_field and field not in prop and not modified:
        prop[field] = orig_mapping_types[0]

    return prop, modified  # prop is for tests


def convert_props(includes, properties, root, content_pointer):
    # for each property, update its type and definition if needed
    if 'oarepo:extends' in properties:
        for i in range(100):
            modified = process_type(properties, 'oarepo:extends', includes, False,
                         root=root, content_pointer=content_pointer)[1]
            if not modified:
                break

    for name, prop in properties.items():
        prop_pointer = content_pointer + '/' + name
        if isinstance(prop, str):
            continue

        for i in range(100):
            modified = process_type(prop, 'oarepo:extends', includes, False, root=root, content_pointer=prop_pointer)[1]
            modified = process_type(prop, 'type', includes, True, root, prop_pointer)[1] or modified
            if not modified:
                break
        else:
            raise Exception('Infinite recursion in mapping type at path %s' % content_pointer)

        # and go recursively
        convert_props(includes, prop.get('properties', {}), root, prop_pointer + '/properties')
        convert_props(includes, prop.get('fields', {}), root, prop_pointer + '/fields')


def convert_extends(includes, el, root, content_pointer):
    for name, prop in el.items():
        if not isinstance(prop, dict):
            continue
        prop_pointer = content_pointer + '/' + name

        process_type(prop, 'oarepo:extends', includes, False, root=root, content_pointer=prop_pointer)
        prop.pop('oarepo:extends', None)
        # no need to go recursively as it is called in convert_props as well
        # convert_extends(includes, prop, root, prop_pointer)


def process(includes, base_dir, filename):
    # load the file, convert its types and write it back into cache directory
    dest_file = os.path.join(base_dir, os.path.basename(filename))
    with open(filename) as f:
        mapping = json.load(f)
    convert_extends(includes, mapping, root=mapping, content_pointer='')
    convert_props(includes, mapping['mappings']['properties'], mapping, '/mappings/properties')
    mapping_to_save = json.dumps(mapping, ensure_ascii=False, indent=4)
    if os.path.exists(dest_file):
        with open(dest_file, 'r') as f:
            existing = f.read()
            if existing == mapping_to_save:
                # do not save again the same data
                return dest_file
    with open(dest_file, 'w') as f:
        f.write(mapping_to_save)

    return dest_file


def mapping_transformer(source, app=None, **kwargs):
    includes = app.extensions['oarepo-mapping-includes']
    mappings = app.extensions['invenio-search'].mappings

    lock = NamedAtomicLock('oarepo-mapping-includes')
    lock.acquire()
    try:
        # create cache directory
        transformed_mappings_dir = os.path.join(app.instance_path, 'mappings')
        if not os.path.exists(transformed_mappings_dir):
            os.makedirs(transformed_mappings_dir)

        # and transform each mapping
        for k, v in list(mappings.items()):
            mappings[k] = process(includes, transformed_mappings_dir, v)
    finally:
        lock.release()
